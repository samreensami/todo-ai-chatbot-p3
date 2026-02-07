# Helm Chart Specification

## Chart Structure

```
helm/todo-app/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── values-dev.yaml     # Development overrides
├── values-prod.yaml    # Production overrides
└── templates/
    ├── _helpers.tpl    # Template helpers
    ├── namespace.yaml
    ├── secrets.yaml
    ├── configmap.yaml
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    └── NOTES.txt       # Post-install notes
```

## Chart.yaml

```yaml
apiVersion: v2
name: todo-app
description: AI-powered Todo Chatbot with FastAPI and Next.js
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - todo
  - chatbot
  - fastapi
  - nextjs
  - cohere
maintainers:
  - name: samreensami
```

## values.yaml

```yaml
# Global settings
namespace: todo-app

# Backend configuration
backend:
  name: todo-backend
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: Never  # Use local images
  replicas: 1
  port: 8000
  service:
    type: NodePort
    nodePort: 30080
  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  env:
    - name: ENVIRONMENT
      value: "production"

# Frontend configuration
frontend:
  name: todo-frontend
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: Never
  replicas: 1
  port: 3000
  service:
    type: NodePort
    nodePort: 30000
  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"

# Secrets (base64 encoded in actual deployment)
secrets:
  databaseUrl: ""      # Set via --set or values override
  cohereApiKey: ""
  jwtSecret: ""

# ConfigMap values
config:
  apiUrl: "http://todo-backend:8000"
  corsOrigins: "*"
```

## Installation Commands

```bash
# Install chart
helm install todo-app ./helm/todo-app -n todo-app --create-namespace

# Install with custom values
helm install todo-app ./helm/todo-app \
  --set secrets.databaseUrl=$DATABASE_URL \
  --set secrets.cohereApiKey=$COHERE_API_KEY \
  -n todo-app --create-namespace

# Upgrade existing release
helm upgrade todo-app ./helm/todo-app -n todo-app

# Uninstall
helm uninstall todo-app -n todo-app
```

## Template Helpers (_helpers.tpl)

```yaml
{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Backend selector labels
*/}}
{{- define "todo-app.backend.selectorLabels" -}}
app: {{ .Values.backend.name }}
{{- end }}

{{/*
Frontend selector labels
*/}}
{{- define "todo-app.frontend.selectorLabels" -}}
app: {{ .Values.frontend.name }}
{{- end }}
```
