# Kubernetes Deployment Quickstart

## Prerequisites

- Docker Desktop or Docker Engine
- Minikube installed
- kubectl installed
- Helm installed (optional)

## Step 1: Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start --cpus=2 --memory=4096

# Verify cluster is running
kubectl cluster-info
minikube status
```

## Step 2: Configure Docker Environment

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Verify (should show Minikube's images)
docker images
```

## Step 3: Build Docker Images

```bash
# Navigate to project root
cd /path/to/Hackkhathon2p3

# Build backend image
cd backend
docker build -t todo-backend:latest .

# Build frontend image
cd ../frontend
docker build \
  --build-arg NEXT_PUBLIC_API_URL=http://$(minikube ip):30080 \
  -t todo-frontend:latest .

# Verify images
docker images | grep todo
```

## Step 4: Create Kubernetes Resources

### Option A: Using kubectl (Raw Manifests)

```bash
# Create namespace
kubectl create namespace todo-app

# Create secrets (replace with your values)
kubectl create secret generic todo-secrets \
  --from-literal=database-url="postgresql://..." \
  --from-literal=cohere-api-key="your-key" \
  --from-literal=jwt-secret="your-secret" \
  -n todo-app

# Create configmap
kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-config
  namespace: todo-app
data:
  api-url: "http://todo-backend:8000"
  cors-origins: "*"
EOF

# Apply deployments and services
kubectl apply -f k8s/manifests/ -n todo-app
```

### Option B: Using Helm

```bash
# Install with Helm
helm install todo-app ./k8s/helm/todo-app \
  --set secrets.databaseUrl="$DATABASE_URL" \
  --set secrets.cohereApiKey="$COHERE_API_KEY" \
  --set secrets.jwtSecret="$JWT_SECRET" \
  -n todo-app --create-namespace
```

## Step 5: Verify Deployment

```bash
# Check pods are running
kubectl get pods -n todo-app

# Expected output:
# NAME                            READY   STATUS    RESTARTS   AGE
# todo-backend-xxx                1/1     Running   0          1m
# todo-frontend-xxx               1/1     Running   0          1m

# Check services
kubectl get svc -n todo-app

# View logs
kubectl logs -l app=todo-backend -n todo-app
kubectl logs -l app=todo-frontend -n todo-app
```

## Step 6: Access Application

```bash
# Open frontend in browser
minikube service todo-frontend -n todo-app

# Or get URLs manually
echo "Frontend: http://$(minikube ip):30000"
echo "Backend:  http://$(minikube ip):30080"

# Test backend health
curl http://$(minikube ip):30080/health
```

## Common Commands

```bash
# View all resources
kubectl get all -n todo-app

# Restart deployments
kubectl rollout restart deployment -n todo-app

# Scale replicas
kubectl scale deployment todo-backend --replicas=2 -n todo-app

# Delete everything
kubectl delete namespace todo-app

# Stop Minikube
minikube stop
```

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

### Image pull errors
```bash
# Ensure you're using Minikube's Docker
eval $(minikube docker-env)
docker images | grep todo
```

### Service not accessible
```bash
kubectl get endpoints -n todo-app
minikube service list
```

### Reset everything
```bash
minikube delete
minikube start
```
