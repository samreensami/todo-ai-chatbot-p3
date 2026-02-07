#!/bin/bash
# Deploy Todo App to Minikube using Helm
# Usage: ./deploy-helm.sh [DATABASE_URL] [COHERE_API_KEY] [JWT_SECRET]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K8S_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
HELM_CHART="$K8S_DIR/helm/todo-app"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Deploying Todo App with Helm${NC}"

# Check prerequisites
if ! command -v helm &> /dev/null; then
    echo -e "${RED}❌ helm not found. Please install helm.${NC}"
    exit 1
fi

if ! minikube status &> /dev/null; then
    echo -e "${YELLOW}⚠️  Minikube not running. Starting...${NC}"
    minikube start --cpus=2 --memory=4096
fi

# Get secrets from environment or arguments
DATABASE_URL="${1:-$DATABASE_URL}"
COHERE_API_KEY="${2:-$COHERE_API_KEY}"
JWT_SECRET="${3:-$JWT_SECRET:-supersecretjwtkey123}"

if [ -z "$DATABASE_URL" ] || [ -z "$COHERE_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  Missing required secrets!${NC}"
    echo "Usage: ./deploy-helm.sh [DATABASE_URL] [COHERE_API_KEY] [JWT_SECRET]"
    echo "Or set environment variables: DATABASE_URL, COHERE_API_KEY, JWT_SECRET"
    exit 1
fi

echo ""
echo "📦 Installing/Upgrading Helm chart..."
helm upgrade --install todo-app "$HELM_CHART" \
    --namespace todo-app \
    --create-namespace \
    --set secrets.databaseUrl="$DATABASE_URL" \
    --set secrets.cohereApiKey="$COHERE_API_KEY" \
    --set secrets.jwtSecret="$JWT_SECRET" \
    --wait \
    --timeout 5m

echo ""
echo -e "${GREEN}✅ Helm deployment complete!${NC}"
echo ""
echo "📊 Release Status:"
helm status todo-app -n todo-app
echo ""
echo "🌍 Service URLs:"
MINIKUBE_IP=$(minikube ip)
echo "   Frontend: http://${MINIKUBE_IP}:30000"
echo "   Backend:  http://${MINIKUBE_IP}:30080"
echo ""
echo "Open frontend: minikube service todo-frontend -n todo-app"
