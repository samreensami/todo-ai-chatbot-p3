# Kubernetes Deployment Overview

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      MINIKUBE CLUSTER                        │
│                                                              │
│  ┌─────────────────┐         ┌─────────────────┐            │
│  │   Frontend Pod  │         │   Backend Pod   │            │
│  │   (Next.js)     │────────▶│   (FastAPI)     │            │
│  │   Port: 3000    │         │   Port: 8000    │            │
│  └────────┬────────┘         └────────┬────────┘            │
│           │                           │                      │
│  ┌────────▼────────┐         ┌────────▼────────┐            │
│  │ Frontend Service│         │ Backend Service │            │
│  │ NodePort: 30000 │         │ NodePort: 30080 │            │
│  └─────────────────┘         └─────────────────┘            │
│                                       │                      │
│                              ┌────────▼────────┐            │
│                              │  K8s Secrets    │            │
│                              │  - DATABASE_URL │            │
│                              │  - COHERE_API   │            │
│                              └─────────────────┘            │
│                                       │                      │
└───────────────────────────────────────┼──────────────────────┘
                                        │
                               ┌────────▼────────┐
                               │    Neon DB      │
                               │   (External)    │
                               └─────────────────┘
```

## Components

### 1. Frontend Deployment
- **Image**: todo-frontend:latest (built locally)
- **Replicas**: 1
- **Port**: 3000
- **Environment**: NEXT_PUBLIC_API_URL from ConfigMap

### 2. Backend Deployment
- **Image**: todo-backend:latest (built locally)
- **Replicas**: 1
- **Port**: 8000
- **Environment**: Secrets for DATABASE_URL, COHERE_API_KEY

### 3. Services
- Frontend: NodePort service exposing port 30000
- Backend: NodePort service exposing port 30080

### 4. Secrets
- `todo-secrets`: Contains DATABASE_URL, COHERE_API_KEY, JWT_SECRET

### 5. ConfigMaps
- `todo-config`: Contains non-sensitive configuration

## Deployment Flow

1. Start Minikube: `minikube start`
2. Set Docker env: `eval $(minikube docker-env)`
3. Build images locally
4. Apply Helm chart or raw manifests
5. Access via `minikube service`

## Directory Structure

```
k8s/
├── helm/
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── secrets.yaml
│           └── configmap.yaml
└── manifests/
    ├── namespace.yaml
    ├── secrets.yaml
    ├── configmap.yaml
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── frontend-deployment.yaml
    └── frontend-service.yaml
```
