# AIOps Commands Reference

## Docker AI Agent (Gordon)

Gordon is Docker's AI assistant for container operations.

### Enable Gordon
1. Install Docker Desktop 4.53+
2. Go to Settings > Beta features
3. Toggle on "Docker AI"

### Commands

```bash
# Get help
docker ai "What can you do?"

# Build optimization
docker ai "build a multi-stage dockerfile for python fastapi app"
docker ai "optimize my Dockerfile for smaller image size"
docker ai "analyze my Dockerfile for security issues"

# Container debugging
docker ai "why is my container crashing?"
docker ai "show me the logs for todo-backend"
docker ai "list all running containers with their ports"

# Image management
docker ai "clean up unused images"
docker ai "tag and push todo-backend to registry"
```

### For this project
```bash
# Build backend
docker ai "build the backend folder as todo-backend:latest"

# Build frontend
docker ai "build frontend with NEXT_PUBLIC_API_URL build arg"

# Debug
docker ai "check if todo-backend container is healthy"
```

---

## kubectl-ai

AI-powered kubectl for natural language Kubernetes operations.

### Installation
```bash
# Using Homebrew
brew install kubectl-ai

# Or download from GitHub releases
# https://github.com/sozercan/kubectl-ai
```

### Commands

```bash
# Namespace operations
kubectl-ai "create namespace todo-app"
kubectl-ai "list all namespaces"

# Deployment operations
kubectl-ai "deploy todo-backend with image todo-backend:latest"
kubectl-ai "scale todo-frontend to 3 replicas"
kubectl-ai "update backend image to todo-backend:v2"

# Service operations
kubectl-ai "expose todo-backend on nodeport 30080"
kubectl-ai "create a loadbalancer for frontend"

# Debugging
kubectl-ai "why are pods failing in todo-app namespace?"
kubectl-ai "show logs for todo-backend pod"
kubectl-ai "describe the failing pod"

# Resource management
kubectl-ai "show resource usage in todo-app"
kubectl-ai "set memory limit to 512Mi for backend"
```

### For this project
```bash
# Full deployment
kubectl-ai "create namespace todo-app"
kubectl-ai "create secret with database-url and cohere-api-key"
kubectl-ai "deploy backend from local image todo-backend:latest"
kubectl-ai "deploy frontend from local image todo-frontend:latest"
kubectl-ai "expose both on NodePort services"

# Verification
kubectl-ai "show all resources in todo-app namespace"
kubectl-ai "check pod health in todo-app"
```

---

## Kagent

Advanced AI agent for Kubernetes cluster management.

### Installation
```bash
# Install kagent CLI
pip install kagent

# Or via npm
npm install -g kagent
```

### Commands

```bash
# Cluster health
kagent "analyze cluster health"
kagent "check for issues in my cluster"
kagent "show cluster resource utilization"

# Optimization
kagent "optimize resource allocation"
kagent "suggest HPA settings for todo-backend"
kagent "recommend pod anti-affinity rules"

# Security
kagent "scan for security vulnerabilities"
kagent "check RBAC configuration"
kagent "analyze network policies"

# Troubleshooting
kagent "diagnose slow pod startup"
kagent "find root cause of OOMKilled pods"
kagent "analyze pod scheduling issues"
```

### For this project
```bash
# Pre-deployment
kagent "check if cluster is ready for deployment"
kagent "verify minikube has enough resources"

# Post-deployment
kagent "verify todo-app deployment is healthy"
kagent "check connectivity between frontend and backend"
kagent "analyze todo-app resource usage"
```

---

## Combined Workflow

### 1. Build Phase (Gordon)
```bash
eval $(minikube docker-env)
docker ai "build backend with multi-stage dockerfile"
docker ai "build frontend with production optimizations"
```

### 2. Deploy Phase (kubectl-ai)
```bash
kubectl-ai "create namespace and deploy todo-app"
kubectl-ai "create secrets from environment variables"
kubectl-ai "verify all pods are running"
```

### 3. Verify Phase (kagent)
```bash
kagent "analyze todo-app deployment health"
kagent "check service connectivity"
kagent "report any issues or warnings"
```

---

## Fallback: Standard Commands

If AI tools are unavailable:

```bash
# Build
docker build -f backend/Dockerfile.k8s -t todo-backend:latest backend/
docker build -f frontend/Dockerfile.k8s -t todo-frontend:latest frontend/

# Deploy
kubectl apply -f k8s/manifests/namespace.yaml
kubectl create secret generic todo-secrets \
  --from-literal=database-url="$DATABASE_URL" \
  --from-literal=cohere-api-key="$COHERE_API_KEY" \
  -n todo-app
kubectl apply -f k8s/manifests/

# Verify
kubectl get pods -n todo-app
kubectl logs -l app=todo-backend -n todo-app
curl http://$(minikube ip):30080/health
```
