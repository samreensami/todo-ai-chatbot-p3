# Phase 4: Kubernetes Deployment

Cloud-Native deployment of Todo AI Chatbot using Minikube, Helm, and AIOps tools.

## Directory Structure

```
k8s/
├── README.md                 # This file
├── QUICKSTART.md            # Step-by-step deployment guide
├── aiops-commands.md        # Gordon, kubectl-ai, kagent reference
├── helm/
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── _helpers.tpl
│           ├── NOTES.txt
│           ├── namespace.yaml
│           ├── secrets.yaml
│           ├── configmap.yaml
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── frontend-deployment.yaml
│           └── frontend-service.yaml
├── manifests/
│   ├── kustomization.yaml
│   ├── namespace.yaml
│   ├── secrets.yaml
│   ├── configmap.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   └── frontend-service.yaml
└── scripts/
    ├── build-images.sh      # Build Docker images (Linux/Mac)
    ├── build-images.bat     # Build Docker images (Windows)
    ├── deploy.sh            # Deploy with kubectl (Linux/Mac)
    ├── deploy.bat           # Deploy with kubectl (Windows)
    ├── deploy-helm.sh       # Deploy with Helm
    ├── cleanup.sh           # Remove deployment
    └── status.sh            # Check deployment status
```

## Quick Start

### Prerequisites
- Minikube installed
- kubectl installed
- Docker installed

### 1. Start Minikube

```bash
minikube start --cpus=2 --memory=4096
eval $(minikube docker-env)
```

### 2. Build Docker Images

```bash
# Backend
cd backend
docker build -t todo-backend:latest .

# Frontend
cd ../frontend
docker build --build-arg NEXT_PUBLIC_API_URL=http://$(minikube ip):30080 -t todo-frontend:latest .
```

### 3. Deploy

#### Option A: Raw Manifests

```bash
# Create secrets first
kubectl create namespace todo-app
kubectl create secret generic todo-secrets \
  --from-literal=database-url="$DATABASE_URL" \
  --from-literal=cohere-api-key="$COHERE_API_KEY" \
  --from-literal=jwt-secret="$JWT_SECRET" \
  -n todo-app

# Apply manifests
kubectl apply -k k8s/manifests/
```

#### Option B: Helm

```bash
helm install todo-app ./k8s/helm/todo-app \
  --set secrets.databaseUrl="$DATABASE_URL" \
  --set secrets.cohereApiKey="$COHERE_API_KEY" \
  --set secrets.jwtSecret="$JWT_SECRET" \
  -n todo-app --create-namespace
```

### 4. Access Application

```bash
# Get URLs
echo "Frontend: http://$(minikube ip):30000"
echo "Backend:  http://$(minikube ip):30080"

# Or open directly
minikube service todo-frontend -n todo-app
```

## Useful Commands

```bash
# Check pods
kubectl get pods -n todo-app

# View logs
kubectl logs -l app=todo-backend -n todo-app
kubectl logs -l app=todo-frontend -n todo-app

# Restart deployments
kubectl rollout restart deployment -n todo-app

# Delete everything
kubectl delete namespace todo-app
# Or with Helm
helm uninstall todo-app -n todo-app
```

## Services

| Service | Internal Port | NodePort | URL |
|---------|---------------|----------|-----|
| Frontend | 3000 | 30000 | http://$(minikube ip):30000 |
| Backend | 8000 | 30080 | http://$(minikube ip):30080 |
