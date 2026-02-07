# Secrets and ConfigMaps Specification

## Kubernetes Secrets

### Secret Manifest (Template)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
  namespace: todo-app
type: Opaque
data:
  # Base64 encoded values
  database-url: <BASE64_ENCODED_DATABASE_URL>
  cohere-api-key: <BASE64_ENCODED_COHERE_API_KEY>
  jwt-secret: <BASE64_ENCODED_JWT_SECRET>
```

### Creating Secrets via kubectl

```bash
# Create namespace first
kubectl create namespace todo-app

# Create secret from literal values
kubectl create secret generic todo-secrets \
  --from-literal=database-url="$DATABASE_URL" \
  --from-literal=cohere-api-key="$COHERE_API_KEY" \
  --from-literal=jwt-secret="$JWT_SECRET" \
  -n todo-app

# Or create from .env file
kubectl create secret generic todo-secrets \
  --from-env-file=.env.production \
  -n todo-app
```

### Helm Secret Template

```yaml
{{- if .Values.secrets.databaseUrl }}
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
  namespace: {{ .Values.namespace }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
type: Opaque
data:
  database-url: {{ .Values.secrets.databaseUrl | b64enc | quote }}
  cohere-api-key: {{ .Values.secrets.cohereApiKey | b64enc | quote }}
  jwt-secret: {{ .Values.secrets.jwtSecret | b64enc | quote }}
{{- end }}
```

## ConfigMaps

### ConfigMap Manifest

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-config
  namespace: todo-app
data:
  api-url: "http://todo-backend:8000"
  cors-origins: "*"
  environment: "production"
  log-level: "INFO"
```

### Helm ConfigMap Template

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-config
  namespace: {{ .Values.namespace }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
data:
  api-url: {{ .Values.config.apiUrl | quote }}
  cors-origins: {{ .Values.config.corsOrigins | quote }}
  environment: "production"
  log-level: "INFO"
```

## Security Best Practices

### 1. Never Commit Secrets
```gitignore
# .gitignore
*.secret.yaml
secrets.yaml
.env
.env.*
!.env.template
```

### 2. Use External Secret Management
```yaml
# For production, consider:
# - Kubernetes External Secrets Operator
# - HashiCorp Vault
# - AWS Secrets Manager
# - Azure Key Vault
```

### 3. Rotate Secrets Regularly
```bash
# Update secret
kubectl create secret generic todo-secrets \
  --from-literal=database-url="$NEW_DATABASE_URL" \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart deployments to pick up new secrets
kubectl rollout restart deployment/todo-backend -n todo-app
```

## Verification Commands

```bash
# View secrets (names only)
kubectl get secrets -n todo-app

# Describe secret
kubectl describe secret todo-secrets -n todo-app

# Decode secret value
kubectl get secret todo-secrets -n todo-app -o jsonpath='{.data.database-url}' | base64 -d

# View configmap
kubectl get configmap todo-config -n todo-app -o yaml
```

## Environment Variable Reference

| Secret Key | Env Variable | Used By |
|------------|--------------|---------|
| database-url | DATABASE_URL | Backend |
| cohere-api-key | COHERE_API_KEY | Backend |
| jwt-secret | JWT_SECRET | Backend |

| ConfigMap Key | Env Variable | Used By |
|---------------|--------------|---------|
| api-url | NEXT_PUBLIC_API_URL | Frontend |
| cors-origins | CORS_ORIGINS | Backend |
