# Phase 4: Kubernetes Deployment Quickstart

## Prerequisites

- [x] Docker Desktop installed
- [x] Minikube installed
- [x] kubectl installed
- [x] Helm installed (optional)
- [x] Phase 3 Todo Chatbot working locally

## Step 1: Start Minikube

```bash
# Start with sufficient resources
minikube start --cpus=2 --memory=4096 --driver=docker

# Verify
minikube status
kubectl cluster-info
```

## Step 2: Configure Docker Environment

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Windows PowerShell:
# minikube docker-env | Invoke-Expression

# Verify (should show Minikube's images)
docker images
```

## Step 3: Build Images

### Option A: Using Gordon (Docker AI)
```bash
docker ai "build backend/Dockerfile.k8s as todo-backend:latest"
docker ai "build frontend/Dockerfile.k8s as todo-frontend:latest with NEXT_PUBLIC_API_URL"
```

### Option B: Standard Docker
```bash
# Build backend
cd backend
docker build -f Dockerfile.k8s -t todo-backend:latest .

# Build frontend
cd ../frontend
docker build -f Dockerfile.k8s \
  --build-arg NEXT_PUBLIC_API_URL=http://$(minikube ip):30080 \
  -t todo-frontend:latest .

# Verify
docker images | grep todo
```

## Step 4: Set Environment Variables

```bash
# Linux/Mac
export DATABASE_URL="postgresql://user:pass@host/db"
export COHERE_API_KEY="your-cohere-key"
export JWT_SECRET="your-jwt-secret"

# Windows CMD
set DATABASE_URL=postgresql://user:pass@host/db
set COHERE_API_KEY=your-cohere-key
set JWT_SECRET=your-jwt-secret

# Windows PowerShell
$env:DATABASE_URL="postgresql://user:pass@host/db"
$env:COHERE_API_KEY="your-cohere-key"
$env:JWT_SECRET="your-jwt-secret"
```

## Step 5: Deploy

### Option A: Using kubectl-ai
```bash
kubectl-ai "create namespace todo-app"
kubectl-ai "create secret todo-secrets with database-url, cohere-api-key, jwt-secret in todo-app"
kubectl-ai "apply all manifests from k8s/manifests directory"
```

### Option B: Using Helm
```bash
helm install todo-app ./k8s/helm/todo-app \
  --set secrets.databaseUrl="$DATABASE_URL" \
  --set secrets.cohereApiKey="$COHERE_API_KEY" \
  --set secrets.jwtSecret="$JWT_SECRET" \
  -n todo-app --create-namespace
```

### Option C: Using Scripts
```bash
# Linux/Mac
chmod +x k8s/scripts/*.sh
./k8s/scripts/deploy.sh

# Windows
k8s\scripts\deploy.bat
```

### Option D: Manual kubectl
```bash
kubectl create namespace todo-app

kubectl create secret generic todo-secrets \
  --from-literal=database-url="$DATABASE_URL" \
  --from-literal=cohere-api-key="$COHERE_API_KEY" \
  --from-literal=jwt-secret="$JWT_SECRET" \
  -n todo-app

kubectl apply -f k8s/manifests/configmap.yaml
kubectl apply -f k8s/manifests/backend-deployment.yaml
kubectl apply -f k8s/manifests/backend-service.yaml
kubectl apply -f k8s/manifests/frontend-deployment.yaml
kubectl apply -f k8s/manifests/frontend-service.yaml
```

## Step 6: Verify Deployment

### Using kagent
```bash
kagent "check health of todo-app deployment"
kagent "verify all pods are running in todo-app namespace"
```

### Using kubectl
```bash
# Check pods
kubectl get pods -n todo-app

# Expected output:
# NAME                            READY   STATUS    RESTARTS   AGE
# todo-backend-xxx                1/1     Running   0          1m
# todo-frontend-xxx               1/1     Running   0          1m

# View logs
kubectl logs -l app=todo-backend -n todo-app
kubectl logs -l app=todo-frontend -n todo-app
```

## Step 7: Access Application

```bash
# Get Minikube IP
minikube ip

# Access URLs
echo "Frontend: http://$(minikube ip):30000"
echo "Backend:  http://$(minikube ip):30080"

# Or open directly in browser
minikube service todo-frontend -n todo-app

# Test backend health
curl http://$(minikube ip):30080/health
```

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

### Image pull errors
```bash
# Ensure using Minikube's Docker
eval $(minikube docker-env)
docker images | grep todo
```

### Service not accessible
```bash
kubectl get endpoints -n todo-app
minikube service list
```

### Database connection issues
```bash
# Check if DATABASE_URL is correct in secret
kubectl get secret todo-secrets -n todo-app -o jsonpath='{.data.database-url}' | base64 -d
```

## Cleanup

```bash
# Remove deployment
kubectl delete namespace todo-app

# Or with Helm
helm uninstall todo-app -n todo-app

# Stop Minikube
minikube stop

# Delete cluster
minikube delete
```

## Success Criteria

- [x] Pods are 'Running' on Minikube
- [x] Backend health check returns 200
- [x] Frontend is accessible via browser
- [x] Chatbot can add/list/complete tasks
- [x] Data persists in Neon DB
