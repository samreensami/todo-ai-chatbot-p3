# Backend Deployment Specification

## Dockerfile (Multi-stage Build)

```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app/ ./app/
COPY main.py .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Kubernetes Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  namespace: todo-app
  labels:
    app: todo-backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
    spec:
      containers:
        - name: todo-backend
          image: todo-backend:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 8000
              protocol: TCP
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: todo-secrets
                  key: database-url
            - name: COHERE_API_KEY
              valueFrom:
                secretKeyRef:
                  name: todo-secrets
                  key: cohere-api-key
            - name: JWT_SECRET
              valueFrom:
                secretKeyRef:
                  name: todo-secrets
                  key: jwt-secret
            - name: CORS_ORIGINS
              valueFrom:
                configMapKeyRef:
                  name: todo-config
                  key: cors-origins
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
```

## Service Manifest

```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
  namespace: todo-app
  labels:
    app: todo-backend
spec:
  type: NodePort
  selector:
    app: todo-backend
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
      nodePort: 30080
```

## Build Commands

```bash
# Set Minikube Docker environment
eval $(minikube docker-env)

# Build backend image
cd backend
docker build -t todo-backend:latest .

# Verify image exists in Minikube
minikube image ls | grep todo-backend
```

## Environment Variables

| Variable | Source | Description |
|----------|--------|-------------|
| DATABASE_URL | Secret | Neon PostgreSQL connection string |
| COHERE_API_KEY | Secret | Cohere API key for AI |
| JWT_SECRET | Secret | JWT signing secret |
| CORS_ORIGINS | ConfigMap | Allowed CORS origins |
| ENVIRONMENT | ConfigMap | Runtime environment |
