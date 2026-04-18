# 🚀 Quick Start Guide - ImageMagick Web Tool

## For Linux/Mac Users

### Simplest Method - One Command

```bash
cd ~/RE4BDD/imagemagickwebtool
chmod +x startup.sh
./startup.sh
```

Then open your browser to:
- **Local**: `http://localhost:3000`
- **Network**: `http://<your-ip>:3000` (get IP with `hostname -I`)

**That's it!** The script will:
- ✅ Start the backend API (port 5000)
- ✅ Start the frontend server (port 3000)  
- ✅ Show you the access URLs
- ✅ Clean up when you press Ctrl+C

---

## For Windows Users

### Option 1: Using Command Prompt

**Terminal 1 - Backend:**
```cmd
cd C:\path\to\RE4BDD\imagemagickwebtool\backend
venv\Scripts\activate
python app.py
```

Expected output:
```
 * Running on http://0.0.0.0:5000
```

**Terminal 2 - Frontend:**
```cmd
cd C:\path\to\RE4BDD\imagemagickwebtool
python frontend_server.py
```

Expected output:
```
✅ Server running on all interfaces (0.0.0.0:3000)
```

### Option 2: Create a BAT Script

Create file: `startup.bat`

```batch
@echo off
echo Starting ImageMagick Web Tool...
echo.

REM Get local IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set LOCAL_IP=%%a
    set LOCAL_IP=!LOCAL_IP: =!
    goto :got_ip
)

:got_ip
echo.
echo ===============================================
echo  Imagemagick Web Tool - Starting...
echo ===============================================
echo.

REM Start Backend
echo Starting Backend API on port 5000...
start "Backend" cmd /k "cd backend && venv\Scripts\activate && python app.py"
timeout /t 2

REM Start Frontend  
echo Starting Frontend Server on port 3000...
start "Frontend" cmd /k "python frontend_server.py"
timeout /t 1

echo.
echo ===============================================
echo  Services Running!
echo ===============================================
echo.
echo Access the application:
echo   Local:    http://localhost:3000
echo   Network:  http://%LOCAL_IP%:3000
echo.
echo Backend API: http://%LOCAL_IP%:5000
echo.
```

Save and run: `startup.bat`

---

## Find Your Local IP Address

### Windows:
```cmd
ipconfig
```
Look for "IPv4 Address" (usually 192.168.x.x or 10.0.0.x)

### Mac/Linux:
```bash
hostname -I
```

### macOS (Alternative):
```bash
ifconfig | grep "inet "
```

---

## Sharing with Others

Once running, share this URL with anyone on your network:
```
http://<your-ip>:3000
```

Example:
```
http://192.168.1.100:3000
http://mycomputer.local:3000
```

---

## Stopping the Application

- **Linux/Mac**: Press `Ctrl+C` in the terminal
- **Windows**: Close the terminal windows or press `Ctrl+C`

---

## Troubleshooting

### ❌ "Port already in use"

**Linux/Mac:**
```bash
lsof -i :3000   # Check what's using port 3000
kill -9 <PID>   # Kill the process
```

**Windows:**
```cmd
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### ❌ Cannot connect from another device

1. Verify both servers are running
2. Use the **Network URL** (not localhost)
3. Check your firewall allows ports 3000 and 5000
4. Test: `curl http://your-ip:5000/` (or use Postman)

### ❌ "Module not found" errors

```bash
# Install dependencies
cd backend
pip install -r requirements.txt
```

---

## What Each Component Does

| Component | Port | Purpose |
|-----------|------|---------|
| **Frontend** | 3000 | Web UI (HTML/CSS/JS) |
| **Backend** | 5000 | Image processing API |
| **ImageMagick** | N/A | Image processing engine |

**Data Flow:**
1. You upload image in browser (port 3000)
2. Browser sends to API (port 5000)
3. API processes with ImageMagick
4. API returns result to browser
5. Browser displays result

---

## Performance Tips

✅ **DO:**
- Use local IP for better speed
- Keep both services running
- Close browser tabs you're not using

❌ **DON'T:**
- Use localhost from different machines
- Stop and start repeatedly
- Process very large files (>50MB default)

---

## Next Steps

1. ✅ Start the application using startup script/commands
2. ✅ Open browser to `http://localhost:3000` or your network IP
3. ✅ Upload an image
4. ✅ Select a filter
5. ✅ Click "Apply Filter"
6. ✅ Download result

---

**Happy Image Processing! 🎨**

For detailed configuration, see: `DEPLOYMENT_GUIDE.md`
