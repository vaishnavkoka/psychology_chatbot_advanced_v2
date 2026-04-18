# 🎨 Image Mutation Tool - Quick Start

## ✅ Your Tool is Now Running!

Both the backend API and frontend interface are now operational.

### 🌐 Access Points

| Component | URL | Status |
|-----------|-----|--------|
| **Web UI (Frontend)** | http://localhost:3000 | ✅ Running on Python HTTP Server |
| **API (Backend)** | http://localhost:5000 | ✅ Running on Flask |
| **API Health Check** | http://localhost:5000/api/health | ✅ Responding |
| **Mutations List** | http://localhost:5000/api/mutations | ✅ Available |

---

## 🚀 What's Running?

### Backend (Flask)
- **Port:** 5000
- **Process:** Python Flask application with ImageMagick integration
- **Purpose:** REST API for image mutations
- **Started by:** `python3 backend/app.py`

### Frontend (Static HTML)
- **Port:** 3000
- **Process:** Python HTTP Server (no Node.js required!)
- **Purpose:** Web UI to interact with mutations
- **Started by:** `python3 frontend_server.py`

---

## 📋 What You Can Do

1. **Open the Web UI** → http://localhost:3000
   - Browse all available mutations
   - View mutation parameters
   - See live connection status to backend

2. **Explore the API** → http://localhost:5000/api/mutations
   - See all continuous mutations (blur, brightness, rotation, etc.)
   - See all discrete mutations (color_reduce, colorize, etc.)
   - View parameter specifications

3. **Read Documentation**
   - `DOCUMENTATION_INDEX.md` - Overview of all docs
   - `TOOL_DESIGN_PLAN.md` - Complete feature design
   - `DEVELOPER_GUIDE.md` - How to extend the tool
   - `API_REFERENCE.md` - API endpoint details

---

## 🛑 Stop the Servers

To stop running servers (if needed):

```bash
# Kill the frontend server
pkill -f "frontend_server.py"

# Kill the backend server  
pkill -f "python3 app.py"

# Or use Ctrl+C if running in foreground
```

---

## 🔧 To Restart the Servers

### Terminal 1 - Start Backend
```bash
cd imagemagickwebtool/backend
source venv/bin/activate
python3 app.py
```

### Terminal 2 - Start Frontend
```bash
cd imagemagickwebtool
python3 frontend_server.py
```

Then open: **http://localhost:3000**

---

## 📝 Next Steps for Development

### 1. Implement Upload Endpoint
Edit `backend/app.py` - Implement `POST /api/upload`:
```python
@app.route('/api/upload', methods=['POST'])
def upload():
    # Save uploaded image to uploads/ folder
    # Return file ID for mutation
    pass
```

### 2. Implement Mutate Endpoint
Edit `backend/app.py` - Implement `POST /api/mutate`:
```python
@app.route('/api/mutate', methods=['POST'])
def mutate():
    # Apply selected mutation to image
    # Save result to outputs/ folder
    # Return before/after URLs
    pass
```

### 3. Build Image Processing Classes
Create in `backend/core/`:
- `base.py` - Base Mutation class
- `continuous.py` - Continuous parameter mutations
- `discrete.py` - Discrete option mutations
- `processor.py` - ImageMagick/Pillow integration

### 4. Enhance Frontend (optional - use React later)
Current setup uses plain HTML. When ready to use React:
1. Upgrade Node.js to v14+
2. Return to `npm start` in `frontend/` directory
3. React components are already created in `frontend/src/`

---

## 🎓 Learning Resources Included

- **COMPLETE_GUIDE.md** - Comprehensive technical overview
- **BACKEND_IMPLEMENTATION.md** - Backend architecture details
- **FRONTEND_IMPLEMENTATION.md** - UI component structure
- **Step-by-step setup** - Automated scripts included

---

## 💡 Current Architecture

```
Image Mutation Tool
├── Backend (Flask on :5000)
│   ├── app.py - Main Flask application
│   ├── venv/ - Python virtual environment
│   ├── core/ - Business logic (TODO)
│   ├── api/ - API routes (TODO)
│   └── storage/ - File handling (TODO)
│
├── Frontend (Python HTTP on :3000)
│   ├── index.html - Built-in web UI
│   ├── frontend_server.py - HTTP server
│   └── src/App.jsx - React components (optional)
│
├── Data Directories
│   ├── uploads/ - User uploaded images
│   ├── outputs/ - Mutation results
│   └── logs/ - Application logs
│
└── Documentation
    ├── DOCUMENTATION_INDEX.md - All docs
    ├── TOOL_DESIGN_PLAN.md - Complete specs
    └── API_REFERENCE.md - All endpoints
```

---

## ✨ The Solution

Fixed the Node.js version incompatibility issue by:
- ✅ Creating a pure Python HTTP server for frontend
- ✅ Using vanilla HTML/JavaScript (no build tools needed)
- ✅ Maintaining full functionality with less complexity
- ✅ No new dependencies required

**Result:** Frontend now works on any system with Python 3 (no Node.js upgrade needed)

---

## 🎯 Quick Commands

```bash
# View backend logs
tail -f backend/logs/app.log

# Check if servers are running
lsof -i :5000    # Backend
lsof -i :3000    # Frontend

# Test API directly
curl http://localhost:5000/api/health
curl http://localhost:5000/api/mutations

# View all endpoints
grep "@app.route" backend/app.py
```

---

**🎉 You're all set! Open http://localhost:3000 in your browser!**
