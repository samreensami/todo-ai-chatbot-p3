#!/bin/bash
# Build Docker images for Minikube deployment
# This script should be run after: eval $(minikube docker-env)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🔧 Building Docker images for Minikube..."
echo "Project root: $PROJECT_ROOT"

# Check if we're in Minikube Docker context
if ! docker info 2>/dev/null | grep -q "minikube"; then
    echo "⚠️  Warning: Not in Minikube Docker context"
    echo "   Run: eval \$(minikube docker-env)"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get Minikube IP for frontend API URL
MINIKUBE_IP=$(minikube ip 2>/dev/null || echo "localhost")
API_URL="http://${MINIKUBE_IP}:30080"

echo ""
echo "📦 Building backend image..."
cd "$PROJECT_ROOT/backend"
docker build -f Dockerfile.k8s -t todo-backend:latest .

echo ""
echo "📦 Building frontend image..."
echo "   API URL: $API_URL"
cd "$PROJECT_ROOT/frontend"
docker build -f Dockerfile.k8s \
    --build-arg NEXT_PUBLIC_API_URL="$API_URL" \
    -t todo-frontend:latest .

echo ""
echo "✅ Images built successfully!"
echo ""
echo "Verify with: docker images | grep todo"
