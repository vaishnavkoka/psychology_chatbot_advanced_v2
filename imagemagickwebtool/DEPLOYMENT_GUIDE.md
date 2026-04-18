# 🚀 ImageMagick Web Tool - Deployment & Network Access Guide

## Overview
The ImageMagick Web Tool is now fully configured for multi-system access. You can run it on any machine and access it from other devices on your network or over the internet.

## Architecture

```
┌─────────────────────────────────────────┐
│  Your Browser/Client Machine            │
│  (any device on network)                │
│  http://server-ip:3000                  │
└──────────────┬──────────────────────────┘
               │
               │ HTTP (port 3000)
               ▼
┌─────────────────────────────────────────┐
│  Frontend Server (advanced-index.html)  │
│  Port: 3000                             │
│  Server: frontend_server.py             │
└──────────────┬──────────────────────────┘
               │
               │ HTTP (port 5000, API calls)
               ▼
┌─────────────────────────────────────────┐
│  Backend API (Flask)                    │
│  Port: 5000                             │
│  Server: backend/app.py                 │
│  ImageMagick Processing                 │
└─────────────────────────────────────────┘
```

---

## Quick Start - Local Network

### Step 1: Start the Backend API

```bash
cd ~/RE4BDD/imagemagickwebtool/backend
source venv/bin/activate  # or use Python venv of your choice
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Running on http://0.0.0.0:5000
 ✅ Server running on 0.0.0.0:5000
```

**Important:** The backend listens on port 5000 on all interfaces (0.0.0.0)

### Step 2: Start the Frontend Server

In a new terminal window:

```bash
cd ~/RE4BDD/imagemagickwebtool
python frontend_server.py
```

Expected output:
```
======================================================================
  🎨 Image Mutation Tool - Frontend Server
======================================================================

📍 Frontend Server Access:
   Local:        http://localhost:3000
   Local IP:     http://192.168.1.100:3000
   Network:      http://yourcomputer.local:3000

📁 Root directory: /home/vaishnavkoka/RE4BDD/imagemagickwebtool

✅ Recommended: Use one of the above URLs in your browser

⚙️  Backend API Configuration:
   The app will automatically detect the API endpoint
   Backend should be running on port 5000
   Ensure backend is accessible from: http://192.168.1.100:5000

⚠️  Press Ctrl+C to stop the server

======================================================================
✅ Server running on all interfaces (0.0.0.0:3000)
✅ Waiting for connections...
```

### Step 3: Access from Another Device

From any device on your network:

```
http://192.168.1.100:3000   (replace with your server's IP)
or
http://yourcomputer.local:3000
```

---

## Find Your Server IP Address

### On Linux/Mac:
```bash
# Simple way
hostname -I

# Alternative
ifconfig | grep "inet "
```

### On Windows:
```cmd
ipconfig
```

Look for "IPv4 Address" in the output, typically like `192.168.x.x` or `10.0.0.x`

---

## Using the Automated Startup Script

Create a file: `startup.sh`

```bash
#!/bin/bash

# ImageMagick Web Tool - Combined Startup Script

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

echo "==============================================="
echo "  🎨 ImageMagick Web Tool - Starting..."
echo "==============================================="

# Get local IP
LOCAL_IP=$(hostname -I | awk '{print $1}')
HOSTNAME=$(hostname)

# Start backend in background
echo "📌 Starting Backend API on port 5000..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

# Wait a moment for backend to start
sleep 2

# Start frontend in new session
echo "📌 Starting Frontend Server on port 3000..."
cd ..
python frontend_server.py &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "==============================================="
echo "  🚀 Services Running!"
echo "==============================================="
echo ""
echo "📍 Access the application:"
echo "   Local:    http://localhost:3000"
echo "   Network:  http://$LOCAL_IP:3000"
echo "   Hostname: http://$HOSTNAME:3000"
echo ""
echo "📊 Backend API:"
echo "   http://$LOCAL_IP:5000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait and handle Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; echo ''; echo 'Services stopped'; exit" INT

wait
```

Make it executable:
```bash
chmod +x startup.sh
```

Run it:
```bash
./startup.sh
```

---

## Remote Access (Over Internet)

For accessing from outside your local network:

### Option 1: Use SSH Tunneling

```bash
# On your local machine:
ssh -L 3000:localhost:3000 -L 5000:localhost:5000 user@remote-server.com

# Then access:
# http://localhost:3000
```

### Option 2: Configure Port Forwarding

Configure your router's port forwarding settings:
- External Port 3000 → Internal IP:3000
- External Port 5000 → Internal IP:5000

Then access from anywhere:
```
http://your-public-ip:3000
```

### Option 3: Use Ngrok (Easy for Testing)

```bash
# Install ngrok from https://ngrok.com

# Expose frontend
ngrok http 3000

# In another terminal, expose backend
ngrok http 5000
```

This gives you public URLs like:
- Frontend: `https://xxxxx.ngrok.io`
- Backend: `https://yyyyy.ngrok.io`

Update your browser console to verify:
```javascript
console.log(API_ENDPOINT)  // Check current API endpoint
```

---

## Troubleshooting

### ❌ Cannot connect from another device

1. **Check if both servers are running:**
   ```bash
   lsof -i :3000   # Frontend
   lsof -i :5000   # Backend
   ```

2. **Check firewall:**
   ```bash
   # Linux
   sudo ufw allow 3000
   sudo ufw allow 5000
   
   # macOS
   sudo lsof -i :3000
   ```

3. **Verify backend is accessible:**
   ```bash
   curl http://192.168.1.100:5000/
   ```

4. **Check browser console for errors:**
   - Press F12 → Console tab
   - Look for error messages
   - Check the API endpoint being used

### ❌ Port already in use

```bash
# Kill process using port 3000
lsof -ti :3000 | xargs kill -9

# Or use a different port - edit frontend_server.py:
# PORT = 3001  (instead of 3000)
```

### ❌ CORS errors (Cross-Origin)

This usually means the frontend and backend are on different hosts and CORS is not properly configured.

**The app should handle this automatically**, but if you see CORS errors:

1. Check browser console (F12)
2. Verify both servers are running
3. Ensure API endpoint is correct (should be `http://server-ip:5000/api`)

---

## Configuration

### Change Ports

**Frontend (frontend_server.py):**
```python
PORT = 3000  # Change this number
```

**Backend (.env file or backend/app.py):**
```
FLASK_PORT=5000  # Change this number
```

### Environment Variables

Create a `.env` file in the backend directory:
```
FLASK_PORT=5000
FLASK_DEBUG=False
MAX_FILE_SIZE=52428800  # 50MB in bytes
```

---

## Performance Tips

1. **Use local IP instead of hostname** - More reliable
   - Good: `http://192.168.1.100:3000`
   - Works: `http://computer.local:3000`
   - Slower: `http://localhost:3000` (only on same machine)

2. **Test API connectivity:**
   ```bash
   curl http://192.168.1.100:5000/
   ```

3. **Monitor resource usage:**
   ```bash
   # Check running processes
   ps aux | grep python
   
   # Check memory/CPU
   top
   ```

---

## Security Notes

⚠️ **For Production Use:**

1. **Use HTTPS instead of HTTP:**
   - Deploy behind an NGINX reverse proxy
   - Use SSL certificates (Let's Encrypt)

2. **Restrict access:**
   ```python
   # In backend/app.py, restrict CORS origins:
   CORS(app, resources={r"/api/*": {"origins": ["https://mydomain.com"]}})
   ```

3. **Add authentication:**
   - Implement user login/authentication
   - Add API key validation

4. **Use strong firewall rules:**
   ```bash
   sudo ufw allow from 192.168.1.0/24 to any port 3000
   sudo ufw allow from 192.168.1.0/24 to any port 5000
   ```

---

## Automated Startup Using Systemd (Linux)

Create `/etc/systemd/system/imagemagick-web.service`:

```ini
[Unit]
Description=ImageMagick Web Tool
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=vaishnavkoka
WorkingDirectory=/home/vaishnavkoka/RE4BDD/imagemagickwebtool
ExecStart=/home/vaishnavkoka/RE4BDD/imagemagickwebtool/startup.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable imagemagick-web
sudo systemctl start imagemagick-web
sudo systemctl status imagemagick-web
```

---

## Testing API Connection

```javascript
// Test from browser console:
fetch('http://192.168.1.100:5000/')
  .then(r => r.json())
  .then(d => console.log('API OK:', d))
  .catch(e => console.error('API ERROR:', e))
```

---

## Support

For issues:
1. Check browser console (F12)
2. Check server terminal output
3. Verify both services are running
4. Check firewall/network settings
5. Review this guide's troubleshooting section

---

**Version:** 1.0  
**Last Updated:** March 2025  
**Status:** ✅ Production Ready
