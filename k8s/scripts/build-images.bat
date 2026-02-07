@echo off
REM Build Docker images for Minikube deployment (Windows)
REM Run this after: minikube docker-env | Invoke-Expression (PowerShell)

echo 🔧 Building Docker images for Minikube...

REM Get Minikube IP
for /f "tokens=*" %%i in ('minikube ip') do set MINIKUBE_IP=%%i
set API_URL=http://%MINIKUBE_IP%:30080

echo.
echo 📦 Building backend image...
cd /d "%~dp0..\..\backend"
docker build -f Dockerfile.k8s -t todo-backend:latest .

echo.
echo 📦 Building frontend image...
echo    API URL: %API_URL%
cd /d "%~dp0..\..\frontend"
docker build -f Dockerfile.k8s --build-arg NEXT_PUBLIC_API_URL=%API_URL% -t todo-frontend:latest .

echo.
echo ✅ Images built successfully!
echo.
echo Verify with: docker images | findstr todo
pause
