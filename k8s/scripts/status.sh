#!/bin/bash
# Check status of Todo App deployment

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📊 Todo App Deployment Status${NC}"
echo "================================"

# Check Minikube status
echo ""
echo -e "${YELLOW}Minikube Status:${NC}"
minikube status 2>/dev/null || echo "Minikube not running"

# Check namespace
echo ""
echo -e "${YELLOW}Namespace:${NC}"
kubectl get namespace todo-app 2>/dev/null || echo "Namespace not found"

# Check pods
echo ""
echo -e "${YELLOW}Pods:${NC}"
kubectl get pods -n todo-app 2>/dev/null || echo "No pods found"

# Check services
echo ""
echo -e "${YELLOW}Services:${NC}"
kubectl get svc -n todo-app 2>/dev/null || echo "No services found"

# Check deployments
echo ""
echo -e "${YELLOW}Deployments:${NC}"
kubectl get deployments -n todo-app 2>/dev/null || echo "No deployments found"

# Get URLs
echo ""
echo -e "${YELLOW}Access URLs:${NC}"
MINIKUBE_IP=$(minikube ip 2>/dev/null || echo "unknown")
echo "   Frontend: http://${MINIKUBE_IP}:30000"
echo "   Backend:  http://${MINIKUBE_IP}:30080"

# Health check
echo ""
echo -e "${YELLOW}Health Check:${NC}"
if curl -s "http://${MINIKUBE_IP}:30080/health" > /dev/null 2>&1; then
    echo -e "   Backend:  ${GREEN}✅ Healthy${NC}"
else
    echo -e "   Backend:  ${RED}❌ Unhealthy${NC}"
fi

if curl -s "http://${MINIKUBE_IP}:30000" > /dev/null 2>&1; then
    echo -e "   Frontend: ${GREEN}✅ Healthy${NC}"
else
    echo -e "   Frontend: ${RED}❌ Unhealthy${NC}"
fi
