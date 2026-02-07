#!/bin/bash
# Deploy Todo App to Minikube using raw manifests
# Usage: ./deploy.sh [DATABASE_URL] [COHERE_API_KEY] [JWT_SECRET]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K8S_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Deploying Todo App to Minikube${NC}"

# Check prerequisites
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found. Please install kubectl.${NC}"
    exit 1
fi

if ! minikube status &> /dev/null; then
    echo -e "${YELLOW}⚠️  Minikube not running. Starting...${NC}"
    minikube start --cpus=2 --memory=4096
fi

# Get secrets from environment or arguments
DATABASE_URL="${1:-$DATABASE_URL}"
COHERE_API_KEY="${2:-$COHERE_API_KEY}"
JWT_SECRET="${3:-$JWT_SECRET}"

if [ -z "$DATABASE_URL" ] || [ -z "$COHERE_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  Missing required secrets!${NC}"
    echo "Usage: ./deploy.sh [DATABASE_URL] [COHERE_API_KEY] [JWT_SECRET]"
    echo "Or set environment variables: DATABASE_URL, COHERE_API_KEY, JWT_SECRET"
    exit 1
fi

# Default JWT secret if not provided
JWT_SECRET="${JWT_SECRET:-supersecretjwtkey123}"

echo ""
echo "📁 Creating namespace..."
kubectl apply -f "$K8S_DIR/manifests/namespace.yaml"

echo ""
echo "🔐 Creating secrets..."
kubectl delete secret todo-secrets -n todo-app --ignore-not-found
kubectl create secret generic todo-secrets \
    --from-literal=database-url="$DATABASE_URL" \
    --from-literal=cohere-api-key="$COHERE_API_KEY" \
    --from-literal=jwt-secret="$JWT_SECRET" \
    -n todo-app

echo ""
echo "⚙️  Creating configmap..."
kubectl apply -f "$K8S_DIR/manifests/configmap.yaml"

echo ""
echo "🐳 Deploying backend..."
kubectl apply -f "$K8S_DIR/manifests/backend-deployment.yaml"
kubectl apply -f "$K8S_DIR/manifests/backend-service.yaml"

echo ""
echo "🌐 Deploying frontend..."
kubectl apply -f "$K8S_DIR/manifests/frontend-deployment.yaml"
kubectl apply -f "$K8S_DIR/manifests/frontend-service.yaml"

echo ""
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-backend -n todo-app --timeout=120s || true
kubectl wait --for=condition=ready pod -l app=todo-frontend -n todo-app --timeout=120s || true

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📊 Pod Status:"
kubectl get pods -n todo-app
echo ""
echo "🌍 Service URLs:"
MINIKUBE_IP=$(minikube ip)
echo "   Frontend: http://${MINIKUBE_IP}:30000"
echo "   Backend:  http://${MINIKUBE_IP}:30080"
echo ""
echo "Open frontend: minikube service todo-frontend -n todo-app"
