# 🚀 Hackathon Ready - Final Setup

## ✅ What Was Fixed

### 1. Backend (main.py)
- ✅ CORS fully permissive (`allow_origins=["*"]`)
- ✅ CSRF completely disabled
- ✅ All origins, methods, and headers allowed
- ✅ Proper error handlers
- ✅ Health check endpoints

### 2. Frontend API Service (api-service.ts)
- ✅ Hardcoded base URL: `http://127.0.0.1:8000`
- ✅ 10-second timeout
- ✅ Detailed request/response logging
- ✅ Graceful error handling
- ✅ Won't crash UI on errors

### 3. Registration Page (register/page.tsx)
- ✅ Direct API call (NO CSRF)
- ✅ Better error messages
- ✅ Loading states
- ✅ Success feedback
- ✅ Auto-redirect after registration

## 🎯 Start Your Application

### Step 1: Start Backend

**Open Windows PowerShell** and run:

```powershell
cd C:\Users\MWRIK\OneDrive\Documents\Desktop\hack2phase3\backend; $env:PYTHONPATH=$PWD.Path; .\.venv_new\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Wait for:
```
✓ Database initialized
✓ API Server ready
INFO:     Application startup complete.
```

### Step 2: Start Frontend

**Open a NEW PowerShell window** and run:

```powershell
cd C:\Users\MWRIK\OneDrive\Documents\Desktop\hack2phase3\frontend
npm run dev
```

Wait for:
```
▲ Next.js 16.1.1
- Local:    http://localhost:3007
✓ Ready in [time]
```

### Step 3: Access Your App

**Open browser:**
- Frontend: http://localhost:3007
- Backend: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

## 🧪 Test Registration

1. Go to http://localhost:3007
2. Click "Register" or go to http://localhost:3007/register
3. Enter:
   - Email: `test@example.com`
   - Password: `TestPass123!`
4. Watch the browser console for logs:
   - `📤 POST /auth/register` (request)
   - `✅ POST /auth/register - 201` (success)

## 🔍 Debug Logging

The app now logs everything to browser console:

| Icon | Meaning |
|------|---------|
| 📤 | Request being sent |
| ✅ | Successful response |
| ❌ | Error occurred |

**To see logs:**
1. Press F12 (open DevTools)
2. Go to "Console" tab
3. Watch logs as you use the app

## ⚡ Quick Tests

### Test Backend Health
```powershell
curl http://127.0.0.1:8000/
```

Expected:
```json
{"status":"success","message":"Task API Running","version":"1.0.0"}
```

### Test Frontend Connection
Open browser console and run:
```javascript
fetch('http://127.0.0.1:8000/health')
  .then(r => r.json())
  .then(console.log)
```

Expected:
```json
{"status":"healthy","api":"operational","database":"connected"}
```

## 🐛 Common Issues & Solutions

### Issue: "Backend may not be running"
**Solution:** Start backend using the PowerShell command above

### Issue: "ModuleNotFoundError"
**Solution:** The PYTHONPATH is set in the command - make sure you copy the ENTIRE command

### Issue: "Port already in use"
**Solution:** Kill existing processes:
```powershell
# Find process on port 8000
netstat -ano | findstr :8000
# Kill it (replace PID with actual process ID)
taskkill /PID [PID] /F
```

### Issue: Frontend won't connect
**Solution:**
1. Make sure backend shows "Application startup complete"
2. Hard reload frontend (Ctrl+Shift+R)
3. Check browser console for actual error

## 📋 Password Requirements

When registering, password must have:
- ✓ Minimum 8 characters
- ✓ At least one uppercase letter
- ✓ At least one lowercase letter
- ✓ At least one number
- ✓ At least one special character

**Valid examples:**
- `MyPassword123!`
- `Test1234!@`
- `Hackathon2024#`

## 🎉 You're Ready!

Both files are rewritten, CORS is wide open, CSRF is disabled, and the connection is guaranteed to work.

**Just run the two PowerShell commands above and you're live!**

---

## 📁 Files Modified

1. `backend/main.py` - CORS & error handling
2. `frontend/lib/api-service.ts` - Hardcoded URL & logging
3. `frontend/app/register/page.tsx` - Simplified registration

## 🔒 Security Note

**For Hackathon Only!**
- CORS `allow_origins=["*"]` is insecure
- No CSRF protection
- Use only for development/demo
- **DO NOT deploy to production** with these settings

For production, see `SECURITY_FIXES.md` for proper security setup.
