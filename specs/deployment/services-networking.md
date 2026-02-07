# Services and Networking Specification

## Service Architecture

```
                    ┌──────────────────────────────────────┐
                    │           MINIKUBE NODE              │
                    │                                      │
   Browser ────────▶│  NodePort 30000 ──▶ Frontend Pod    │
                    │                      :3000           │
                    │                        │             │
                    │                        ▼             │
                    │  NodePort 30080 ──▶ Backend Pod     │
                    │                      :8000           │
                    │                        │             │
                    └────────────────────────┼─────────────┘
                                             │
                                             ▼
                                      ┌─────────────┐
                                      │  Neon DB    │
                                      │  (External) │
                                      └─────────────┘
```

## Service Types

### NodePort Services (Development)
Used for Minikube local development.

```yaml
# Frontend Service
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend
  namespace: todo-app
spec:
  type: NodePort
  selector:
    app: todo-frontend
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30000

---
# Backend Service
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
  namespace: todo-app
spec:
  type: NodePort
  selector:
    app: todo-backend
  ports:
    - port: 8000
      targetPort: 8000
      nodePort: 30080
```

### ClusterIP Services (Production)
For internal communication between pods.

```yaml
# Backend Internal Service
apiVersion: v1
kind: Service
metadata:
  name: todo-backend-internal
  namespace: todo-app
spec:
  type: ClusterIP
  selector:
    app: todo-backend
  ports:
    - port: 8000
      targetPort: 8000
```

## Ingress Configuration (Optional)

For production-like setup with a single entry point:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-ingress
  namespace: todo-app
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: todo.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: todo-frontend
                port:
                  number: 3000
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: todo-backend
                port:
                  number: 8000
```

### Enable Ingress in Minikube

```bash
# Enable ingress addon
minikube addons enable ingress

# Add to /etc/hosts
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
```

## Network Policies

### Restrict Backend Access

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
  namespace: todo-app
spec:
  podSelector:
    matchLabels:
      app: todo-backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: todo-frontend
      ports:
        - protocol: TCP
          port: 8000
```

## Access Commands

```bash
# Get Minikube IP
minikube ip

# Access frontend directly
minikube service todo-frontend -n todo-app

# Access backend directly
minikube service todo-backend -n todo-app

# Get service URLs
minikube service list -n todo-app

# Port forward (alternative)
kubectl port-forward svc/todo-frontend 3000:3000 -n todo-app
kubectl port-forward svc/todo-backend 8000:8000 -n todo-app
```

## DNS Resolution

Within the cluster, services can be accessed by name:

| Service | Internal DNS | Port |
|---------|--------------|------|
| Frontend | todo-frontend.todo-app.svc.cluster.local | 3000 |
| Backend | todo-backend.todo-app.svc.cluster.local | 8000 |

Short form within same namespace:
- `todo-frontend:3000`
- `todo-backend:8000`

## Health Endpoints

| Service | Health Check URL |
|---------|------------------|
| Backend | http://todo-backend:8000/health |
| Frontend | http://todo-frontend:3000/ |

## Troubleshooting

```bash
# Check service endpoints
kubectl get endpoints -n todo-app

# Test connectivity from within cluster
kubectl run curl --image=curlimages/curl -it --rm -- \
  curl http://todo-backend:8000/health

# View service details
kubectl describe svc todo-backend -n todo-app

# Check pod networking
kubectl get pods -n todo-app -o wide
```
