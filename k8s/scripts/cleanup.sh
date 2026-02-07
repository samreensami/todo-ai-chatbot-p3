#!/bin/bash
# Cleanup Todo App from Minikube

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🧹 Cleaning up Todo App from Minikube${NC}"

# Check if helm release exists
if helm status todo-app -n todo-app &> /dev/null; then
    echo "📦 Removing Helm release..."
    helm uninstall todo-app -n todo-app
fi

# Delete namespace (removes all resources)
echo "📁 Deleting namespace..."
kubectl delete namespace todo-app --ignore-not-found

echo ""
echo -e "${GREEN}✅ Cleanup complete!${NC}"
echo ""

# Optional: Remove Docker images
read -p "Remove Docker images? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🐳 Removing Docker images..."
    docker rmi todo-backend:latest 2>/dev/null || true
    docker rmi todo-frontend:latest 2>/dev/null || true
    echo "Done!"
fi
