# 🎨 Image Upload and Mutation Guide

## ✅ Feature Complete!

Your Image Mutation Tool now has **full image upload and mutation capabilities**!

---

## 🚀 How to Use

### 1. Open the Web Interface
Navigate to: **http://localhost:3000**

### 2. Upload an Image
- **Left panel**: Click the upload area or drag & drop an image
- **Supported formats**: PNG, JPG, GIF, WebP
- **Max size**: 50MB
- **Preview**: Image appears immediately after upload

### 3. Select a Mutation
- **Right panel**: Choose from **Continuous** or **Discrete** mutations
- **Continuous mutations** have adjustable parameters (sliders)
- **Discrete mutations** have fixed effects

### 4. Adjust Parameters (if applicable)
- **Sliders**: Drag to adjust values
- **Real-time display**: See the current value
- **Apply button**: Becomes enabled when image + mutation are selected

### 5. Apply Mutation
- Click **"Apply Mutation"** button
- Watch the processing indicator
- See before/after comparison

### 6. Download Results
- **Download button**: Appears in results section
- **Start Over**: Clear all and try another mutation

---

## 🎯 Available Mutations

### Continuous Mutations (Adjustable Parameters)

#### 1. **Blur**
- **Parameter**: Sigma (0.1 - 50)
- **Effect**: Gaussian blur effect
- **Use case**: Soften or blur images

#### 2. **Brightness**
- **Parameter**: Percentage (-100 to +100)
- **Effect**: Increase or decrease brightness
- **Use case**: Brighten dark photos or darken bright ones

#### 3. **Rotation**
- **Parameter**: Degrees (0 - 360)
- **Effect**: Rotate image by angle
- **Use case**: Change image orientation

#### 4. **Contrast**
- **Parameter**: Percentage (-100 to +100)
- **Effect**: Adjust contrast levels
- **Use case**: Enhance or reduce contrast

#### 5. **Saturation**
- **Parameter**: Percentage (-100 to +200)
- **Effect**: Adjust color saturation
- **Use case**: Make colors more vibrant or muted

### Discrete Mutations (Fixed Options)

#### 1. **Color Reduce**
- **Options**: 2, 4, 8, 16, 32, 64, 128, 256 colors
- **Effect**: Reduce color palette
- **Use case**: Posterize or create artistic effects

#### 2. **Colorize**
- **Options**: Red, Green, Blue, Yellow, Cyan, Magenta, Grayscale
- **Effect**: Apply color tint to image
- **Use case**: Create monochrome or single-color versions

#### 3. **Grayscale**
- **No parameters**
- **Effect**: Convert to black & white
- **Use case**: Create grayscale versions

---

## 🔧 Backend Implementation

### API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/mutate` | Apply mutation to image |
| GET | `/api/mutations` | Get all available mutations |
| GET | `/api/health` | Check backend status |
| GET | `/api/image/<file>` | View result image |
| GET | `/api/download/<file>` | Download result image |

### Request Format (POST /api/mutate)

```json
{
  "image": <File>,
  "mutation": "blur",
  "parameters": { "sigma": 5.0 }
}
```

### Response Format

```json
{
  "success": true,
  "mutation": "blur",
  "parameters": { "sigma": 5.0 },
  "original_url": "/api/image/uuid_original.jpg",
  "result_url": "/api/image/uuid_result.jpg",
  "download_url": "/api/download/uuid_result.jpg",
  "timestamp": "2026-03-23T10:00:00"
}
```

---

## 🛠️ Technical Stack

### Frontend
- **Type**: Pure HTML5 + JavaScript
- **Port**: 3000 (Python HTTP server)
- **No build tools required**
- **Features**:
  - Drag & drop file upload
  - Real-time parameter sliders
  - Before/after image comparison
  - Automatic backend connection status
  - Responsive mobile design

### Backend
- **Framework**: Flask 2.3.0
- **Port**: 5000
- **Image processing**: Pillow (PIL)
- **Features**:
  - 8 mutation types
  - CORS enabled for frontend
  - File validation (type, size)
  - Error handling and logging
  - Temporary file storage

### Supported Libraries
- Flask (web server)
- Pillow (image processing)
- Flask-CORS (cross-origin requests)
- Python 3.10.12 (venv)

---

## 📊 File Storage

### Directories

| Directory | Purpose |
|-----------|---------|
| `uploads/` | Temporary uploaded images |
| `outputs/` | Original and result images |
| `logs/` | Application logs |

### Cleanup
Image files are stored for 24 hours. Old files should be manually cleaned if needed:

```bash
# Clean files older than 1 day
find /path/to/outputs -name "*.jpg" -mtime +1 -delete
```

---

## 🐛 Troubleshooting

### "Backend Not Running"
**Error**: Backend connection badge shows ❌

**Solution**:
```bash
cd backend
source venv/bin/activate
python3 app.py
```

### "Image Upload Failed"
**Possible issues**:
- File > 50MB - reduce file size
- Unsupported format - use PNG, JPG, GIF, WebP
- Backend offline - check backend status

### "Mutation Processing Error"
**Check**:
- All required parameters are set
- Image file is valid
- Backend error logs: `tail -f backend/logs/app.log`

### Frontend at localhost:3000 not loading
**Check**:
- Frontend server running: `curl http://localhost:3000`
- Try: `pkill -f frontend_server.py && python3 frontend_server.py`

---

## 📝 Example API Usage (curl)

### Upload and Mutate
```bash
# 1. Create test image
convert -size 200x200 xc:blue test.jpg

# 2. Apply blur mutation
curl -X POST http://localhost:5000/api/mutate \
  -F "image=@test.jpg" \
  -F "mutation=blur" \
  -F 'parameters={"sigma": 10}'

# 3. Download result
curl http://localhost:5000/api/image/uuid_result.jpg -o result.jpg
```

---

## 🚀 What's Next?

### Easy Extensions
1. **Add new mutations** in `backend/app.py` (ImageMutator class)
2. **Adjust parameters** in `/api/mutations` endpoint
3. **Customize colors** in the colorize mutation

### Advanced Features
1. **Batch processing** - Upload multiple images
2. **Custom presets** - Save favorite parameter combinations
3. **Image comparison** - Slider between before/after
4. **History** - Track all mutations applied
5. **Advanced filters** - Edge detection, sharpen, etc.

---

## 📚 Additional Documentation

- `TOOL_DESIGN_PLAN.md` - Complete feature specifications
- `API_REFERENCE.md` - Detailed endpoint documentation
- `DEVELOPER_GUIDE.md` - How to extend the tool
- `DOCUMENTATION_INDEX.md` - All documentation files

---

## ✨ Current Status

✅ **Fully operational**
- Image upload working
- All 8 mutations implemented
- Parameter adjustment working
- Before/after comparison available
- Download functionality enabled

🎉 **Ready to use!** Open **http://localhost:3000** now
