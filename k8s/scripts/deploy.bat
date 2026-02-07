@echo off
REM Deploy Todo App to Minikube (Windows)
REM Usage: deploy.bat

setlocal

echo 🚀 Deploying Todo App to Minikube

REM Check if secrets are set
if "%DATABASE_URL%"=="" (
    echo ⚠️  DATABASE_URL not set!
    echo Set it with: set DATABASE_URL=your_connection_string
    exit /b 1
)

if "%COHERE_API_KEY%"=="" (
    echo ⚠️  COHERE_API_KEY not set!
    echo Set it with: set COHERE_API_KEY=your_api_key
    exit /b 1
)

if "%JWT_SECRET%"=="" (
    set JWT_SECRET=supersecretjwtkey123
)

cd /d "%~dp0.."

echo.
echo 📁 Creating namespace...
kubectl apply -f manifests\namespace.yaml

echo.
echo 🔐 Creating secrets...
kubectl delete secret todo-secrets -n todo-app --ignore-not-found
kubectl create secret generic todo-secrets --from-literal=database-url="%DATABASE_URL%" --from-literal=cohere-api-key="%COHERE_API_KEY%" --from-literal=jwt-secret="%JWT_SECRET%" -n todo-app

echo.
echo ⚙️  Creating configmap...
kubectl apply -f manifests\configmap.yaml

echo.
echo 🐳 Deploying backend...
kubectl apply -f manifests\backend-deployment.yaml
kubectl apply -f manifests\backend-service.yaml

echo.
echo 🌐 Deploying frontend...
kubectl apply -f manifests\frontend-deployment.yaml
kubectl apply -f manifests\frontend-service.yaml

echo.
echo ⏳ Waiting for pods...
timeout /t 30 /nobreak

echo.
echo ✅ Deployment complete!
echo.
echo 📊 Pod Status:
kubectl get pods -n todo-app

for /f "tokens=*" %%i in ('minikube ip') do set MINIKUBE_IP=%%i
echo.
echo 🌍 Service URLs:
echo    Frontend: http://%MINIKUBE_IP%:30000
echo    Backend:  http://%MINIKUBE_IP%:30080
echo.
echo Open frontend: minikube service todo-frontend -n todo-app
pause
