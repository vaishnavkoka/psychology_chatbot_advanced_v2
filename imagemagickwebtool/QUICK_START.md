# Image Mutation Tool - Quick Start Guide

## 🚀 Getting Started

This guide will help you set up and run the Image Mutation Tool locally in under 30 minutes.

---

## 📋 Prerequisites

### Required
- **Python 3.8+** (for backend)
- **Node.js 14+** (for frontend)
- **ImageMagick 7.0+** (for image processing)
- **Git** (for version control)

### Optional
- **Docker** (for containerized deployment)
- **PostgreSQL** (for production database)
- **Redis** (for task queueing)

---

## 🔧 Installation Steps

### **Step 1: Clone Repository & Setup**

```bash
# Clone the project
git clone https://github.com/yourusername/image-mutation-tool.git
cd image-mutation-tool

# Create directories
mkdir -p uploads outputs logs
```

### **Step 2: Install ImageMagick**

#### **On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install imagemagick libmagickwand-dev

# Verify installation
convert --version
magick --version
```

#### **On macOS:**
```bash
# Using Homebrew
brew install imagemagick

# Verify
magick --version
```

#### **On Windows:**
```powershell
# Using Chocolatey
choco install imagemagick

# Or download from: https://imagemagick.org/script/download.php
```

### **Step 3: Backend Setup**

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
FLASK_ENV=development
DEBUG=True
UPLOAD_FOLDER=../uploads
OUTPUT_FOLDER=../outputs
MAX_FILE_SIZE=52428800
LOG_LEVEL=INFO
EOF

# Test backend
python -c "from mutations.registry import mutation_registry; print(mutation_registry.list_all())"
```

### **Step 4: Frontend Setup**

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:5000/api" > .env

# Verify installation
npm list react react-dom react-router-dom
```

### **Step 5: Verify Installation**

```bash
# Test Python imports
python -c "
from flask import Flask
from PIL import Image
from wand.image import Image as WandImage
print('✓ All Python dependencies OK')
"

# Test Node modules
node -e "
const fs = require('fs');
const pkgJson = require('./frontend/package.json');
console.log('✓ All Node dependencies OK');
console.log('  React:', pkgJson.dependencies.react);
console.log('  React Router:', pkgJson.dependencies['react-router-dom']);
"
```

---

## ▶️ Running the Application

### **Option A: Separate Terminals (Recommended for Development)**

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or: venv\Scripts\activate on Windows
python app.py
# Server running at: http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
# App running at: http://localhost:3000
```

### **Option B: Docker (Recommended for Production)**

```bash
# Build and run with Docker Compose
docker-compose up --build

# This will start:
# - Backend on http://localhost:5000
# - Frontend on http://localhost:3000
# - Optional: PostgreSQL on localhost:5432
```

---

## 🧪 Testing the Tool

### **1. Test Backend API**

```bash
# Check available mutations
curl http://localhost:5000/api/mutations

# Sample response:
{
  "all": {
    "blur": {...},
    "brightness": {...},
    ...
  },
  "continuous": {...},
  "discrete": {...}
}
```

### **2. Test with Sample Image**

```bash
# Create a test image
python << 'EOF'
from PIL import Image
import os

# Create 100x100 test image
img = Image.new('RGB', (100, 100), color='red')
img.save('test_image.jpg')
print("✓ Test image created: test_image.jpg")
EOF

# Upload image via API
curl -X POST \
  -F "files=@test_image.jpg" \
  http://localhost:5000/api/upload

# Sample response:
{
  "job_id": "abc-123-def",
  "uploaded_files": 1,
  "files": [{...}]
}
```

### **3. Apply a Mutation**

```bash
# Apply blur mutation
curl -X POST http://localhost:5000/api/mutate \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "abc-123-def",
    "mutation": "blur",
    "parameters": {"sigma": 5},
    "image_paths": ["uploads/abc-123-def/test_image.jpg"]
  }'
```

### **4. Frontend Testing**

1. Open http://localhost:3000
2. Upload test_image.jpg
3. Select "Blur" from mutations
4. Set Sigma = 5
5. Click "Apply Mutation"
6. View results and download

---

## 📁 Project Structure

```
image-mutation-tool/
├── backend/
│   ├── app.py                      # Flask entry point
│   ├── config.py                   # Configuration
│   ├── mutations/
│   │   ├── base.py                 # Base mutation class
│   │   ├── continuous.py           # Blur, brightness, etc.
│   │   ├── discrete.py             # Color reduction, etc.
│   │   └── registry.py             # Mutation registry
│   ├── core/
│   │   ├── mutation_executor.py
│   │   └── image_handler.py
│   ├── storage/
│   │   ├── local_storage.py
│   │   └── manifest.py
│   ├── api/
│   │   └── routes.py
│   ├── tests/
│   │   ├── test_mutations.py
│   │   └── test_api.py
│   ├── requirements.txt
│   ├── wsgi.py
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageUpload.jsx
│   │   │   ├── MutationSelector.jsx
│   │   │   ├── ParamterControls.jsx
│   │   │   ├── PreviewWindow.jsx
│   │   │   ├── BeforeAfterSlider.jsx
│   │   │   └── ResultsPanel.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── MutationPage.jsx
│   │   │   └── DocumentationPage.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── hooks/
│   │   ├── App.jsx
│   │   └── index.js
│   ├── public/
│   ├── package.json
│   └── .env
│
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
├── docs/
│   ├── TOOL_DESIGN_PLAN.md
│   ├── BACKEND_IMPLEMENTATION.md
│   ├── FRONTEND_IMPLEMENTATION.md
│   ├── QUICK_START.md              # ← You are here
│   └── API_REFERENCE.md
│
└── Master File - Magick Image filters[...].csv
```

---

## 🎨 Available Mutations (Quick Reference)

### **Continuous (Numeric Parameters)**
| Mutation | Default | Range | Example |
|----------|---------|-------|---------|
| **blur** | 5 | 0.1-50 | Sigma=10 for heavy blur |
| **brightness** | 0 | -100 to 100 | 50 for brighter image |
| **rotation** | 0 | 0-360 | 45 degrees |
| **border** | 10 | 0-200 | 20px border |
| **charcoal** | 5 | 0.1-20 | 10 for sketch effect |

### **Discrete (Fixed Options)**
| Mutation | Options | Use Case |
|----------|---------|----------|
| **color_reduce** | 2,4,8,16,32,64,128,256 | Posterization effect |
| **colorize** | red,green,blue,yellow,cyan,magenta,grayscale | Color tinting |
| Other coming soon... | | |

---

## 📊 API Endpoints

```
GET    /api/mutations              # List all mutations
POST   /api/upload                 # Upload images
POST   /api/mutate                 # Apply mutation
GET    /api/download/<job>/<file>  # Download result
GET    /api/manifest/<job>         # Get metadata
GET    /health                     # Health check
```

---

## 🐛 Troubleshooting

### **Issue: ImageMagick not found**
```bash
# Verify ImageMagick installation
which magick
which convert

# If not found, install again:
# Ubuntu: sudo apt-get install imagemagick
# macOS: brew install imagemagick
```

### **Issue: Port 5000 already in use**
```bash
# Find and kill process using port 5000
lsof -i :5000
kill -9 <PID>

# Or use different port:
# Modify backend: app.run(port=5001)
# Update frontend .env: REACT_APP_API_URL=http://localhost:5001/api
```

### **Issue: CORS errors**
```python
# Already handled in app.py with:
from flask_cors import CORS
CORS(app)

# But if still issues, add to config:
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:3001"]
```

### **Issue: Upload file size errors**
```bash
# Increase max file size in backend/.env:
MAX_FILE_SIZE=104857600  # 100MB instead of 50MB

# Also check Nginx/server config if deployed
```

### **Issue: Slow mutations on large images**
```bash
# Options:
# 1. Reduce image dimensions before upload
# 2. Increase timeout in backend/app.py (currently 30s)
# 3. Use Celery task queue for async processing (Phase 3)
```

---

## 📚 Next Steps

### **After Basic Setup:**

1. **Run Tests** (to ensure everything works)
   ```bash
   cd backend
   pytest tests/
   ```

2. **Explore the UI**
   - Upload sample images
   - Try different mutations
   - Download results
   - Review metadata

3. **Read Documentation**
   - [TOOL_DESIGN_PLAN.md](TOOL_DESIGN_PLAN.md) - Complete feature overview
   - [BACKEND_IMPLEMENTATION.md](BACKEND_IMPLEMENTATION.md) - Backend architecture
   - [FRONTEND_IMPLEMENTATION.md](FRONTEND_IMPLEMENTATION.md) - React components

4. **Customize**
   - Add your mutations to `mutations/` folder
   - Create presets in `MutationPresets.jsx`
   - Modify branding in `Header.jsx`
   - Add your research paper citation

5. **Deploy**
   - Follow deployment instructions in docs/
   - Choose: Heroku, AWS, Azure, or DigitalOcean
   - Setup CI/CD pipeline

---

## 🎓 Research Integration

### **Add Your Paper**

1. Create `docs/RESEARCH_PAPER.md`:
   ```markdown
   # Research Paper Integration
   
   **Title:** Evaluation of the Impact of Image Mutations on the Origin Classification of Digital Images
   
   **Abstract:** [Your abstract]
   
   **DOI:** [Your DOI]
   
   **Key Findings:**
   - [Finding 1]
   - [Finding 2]
   
   **Mutations Studied:**
   - Blur
   - Color reduction
   - Rotation
   ...
   ```

2. Add citation to UI footer

3. Create "About Research" page

---

## 📞 Support

### **Getting Help**

- **Documentation**: See `docs/` folder
- **Issue Tracker**: GitHub Issues
- **Stack**: Flask, React, ImageMagick, Python 3.8+

### **Common Questions**

**Q: Can I use my own ImageMagick installation?**
A: Yes! The tool uses system ImageMagick via subprocess.

**Q: Can I add custom mutations?**
A: Yes! Create a new class in `mutations/` inheriting from `MutationBase`.

**Q: Can I deploy to production?**
A: Yes! See deployment guides. Recommended: Docker + Heroku/AWS.

**Q: Can I use GPU acceleration?**
A: Not yet, but CUDA support can be added in Phase 3.

---

## ✅ Verification Checklist

- [ ] ImageMagick installed and working
- [ ] Python venv created and activated
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend running on http://localhost:5000
- [ ] Frontend running on http://localhost:3000
- [ ] Can upload test image
- [ ] Can apply blur mutation
- [ ] Can download result
- [ ] Backend tests passing

---

## 🎉 You're Ready!

Once you complete the checklist above, your Image Mutation Tool is ready to use!

**Next: Customize and add your mutations based on your research.**

```
       Welcome to Image Mutation Tool! 🎨
       
       Backend: http://localhost:5000/api
       Frontend: http://localhost:3000
       
       Start mutating images now!
```

