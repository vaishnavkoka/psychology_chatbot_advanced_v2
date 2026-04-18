# Image Mutation Web Tool - Design & Implementation Plan

## 📋 Overview

An interactive web-based platform allowing researchers, testers, and ML practitioners to apply controlled image mutations to test image classifiers, evaluate model robustness, and generate augmented datasets for training.

**Based on:** Research paper "Evaluation of the Impact of Image Mutations on the Origin Classification of Digital Images"

---

## 🎯 Tool Features

### 1. **Image Upload & Management**
- Single or batch image upload (JPG, PNG, GIF, TIFF, BMP)
- Maximum file size: 50MB per image (configurable)
- Preview uploaded images
- Support for multiple images in one session
- Image metadata display (resolution, size, format, color profile)

### 2. **Mutation Categories**

#### **CONTINUOUS MUTATIONS** (Adjustable Parameters)
Mutations that accept numeric ranges and can be applied with varying intensities:

| Mutation | Parameter | Range | Default | Use Case |
|----------|-----------|-------|---------|----------|
| **Blur** | Sigma | 0.1 - 50 | 5 | Test blur robustness |
| **Border** | Width (px) | 0 - 200 | 10 | Test edge padding |
| **Charcoal** | Radius | 0.1 - 20 | 5 | Test texture effect |
| **Brightness** | Percentage | -100 to +100 | 0 | Test brightness variation |
| **Contrast** | Percentage | -100 to +100 | 0 | Test contrast robustness |
| **Saturation** | Percentage | -100 to +200 | 0 | Test color saturation |
| **Hue-Rotate** | Degrees | 0 - 360 | 0 | Test color shift |
| **Noise** | Density | 0.01 - 0.5 | 0.1 | Test noise robustness |
| **Rotation** | Degrees | 0 - 360 | 0 | Test rotation invariance |
| **Zoom** | Scale Factor | 0.5 - 3.0 | 1.0 | Test scale variation |
| **Compression** | Quality | 1 - 100 | 85 | Test compression artifacts |

#### **DISCRETE MUTATIONS** (Fixed/Selection-Based)
Mutations applied as on/off effects or with predefined options:

| Mutation | Options | Default | Use Case |
|----------|---------|---------|----------|
| **Black Threshold** | 10%, 25%, 50%, 75% | 25% | Test binary conversion |
| **Color Reduction** | 2, 4, 8, 16, 32, 64, 128, 256 colors | 256 | Test color quantization |
| **Colorize** | Red, Green, Blue, Grayscale, Yellow, Cyan, Magenta | None | Test color tinting |
| **Colorspace** | RGB, CMYK, HSV, LAB, Grayscale, Rec709YCbCr | RGB | Test color space changes |
| **Posterize** | 2-8 levels | 4 | Test posterization |
| **Solarize** | On/Off | Off | Test solarization effect |
| **Flip** | Horizontal, Vertical, Both | None | Test reflection invariance |
| **Clip Path** | Using embedded paths | None | Test clipping effects |
| **Intensity Equalize** | On/Off | Off | Test histogram equalization |
| **Emboss** | On/Off | Off | Test emboss effect |
| **Edge Detect** | Sobel, Canny, Roberts | None | Test edge detection |

---

### 3. **Mutation Application Modes**

#### **Mode A: Single Mutation**
- Select one mutation type
- Configure its parameters
- Apply to selected image(s)
- Preview result in real-time (for fast mutations)
- Download individual mutated images

#### **Mode B: Mutation Pipeline**
- Apply multiple mutations sequentially
- Define order of operations
- Set parameters for each mutation
- Preview transformation chain
- Download final result

#### **Mode C: Batch Mutation Suite**
- Create a "mutation profile"
  - Define 3-5 mutations with parameters
  - Name the profile (e.g., "robustness-test-v1")
- Apply entire profile to all uploaded images
- Generate dataset summary (before/after comparison)
- Download all mutated images as ZIP

#### **Mode D: Random Mutation (Stress Testing)**
- Select mutation categories
- Set intensity levels (low/medium/high)
- Number of variations to generate per image
- Tool automatically applies random combinations
- Download all variants for stress testing

---

### 4. **Parameter Control Interfaces**

#### **For Continuous Mutations:**
```
[Blur Effect]
┌─────────────────────────────────────┐
│ Sigma Value: [────●────]            │ 
│ Current: 5 (Range: 0.1 - 50)        │
│ Preview:  [✓] Real-time Preview     │
│                                     │
│ [Cancel]        [Apply]             │
└─────────────────────────────────────┘
```

#### **For Discrete Mutations:**
```
[Color Reduction]
┌─────────────────────────────────────┐
│ Target Colors:                      │
│ ○ 2   ○ 4   ○ 8   ○ 16             │
│ ○ 32  ○ 64  ○ 128  ●256 (default)  │
│                                     │
│ Preview:  [✓] Show Result           │
│                                     │
│ [Cancel]        [Apply]             │
└─────────────────────────────────────┘
```

---

### 5. **User Interface Layout**

```
┌──────────────────────────────────────────────────────────────────┐
│  IMAGE MUTATION RESEARCH TOOL                         [GitHub]   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐  ┌──────────────────────────────────┐ │
│  │   UPLOAD IMAGES     │  │     MUTATION CONTROLS            │ │
│  │                     │  │  ┌────────────────────────────┐  │ │
│  │  [Upload Button ▼]  │  │  │ Mode: [Single▼]           │  │ │
│  │  [Drag-Drop Area]   │  │  │                            │  │ │
│  │                     │  │  │ Mutation: [Blur ▼]       │  │ │
│  │ ✓ Image1.png       │  │  │ Sigma: [──●──] 5          │  │ │
│  │ ✓ Image2.jpg       │  │  │                            │  │ │
│  │ ✓ Image3.tiff      │  │  │ [Preview] [Apply]         │  │ │
│  │                     │  │  │                            │  │ │
│  │ Total: 3 images    │  │  └────────────────────────────┘  │ │
│  │ 25.3 MB            │  │                                  │ │
│  │                     │  │  ┌────────────────────────────┐  │ │
│  │ [✓ Clear All]      │  │  │ QUICK ACTIONS:            │  │ │
│  │                     │  │  │ [Single Mutation]         │  │ │
│  │                     │  │  │ [Mutation Pipeline]       │  │ │
│  │                     │  │  │ [Batch Suite]             │  │ │
│  │                     │  │  │ [Stress Test (Random)]    │  │ │
│  │                     │  │  └────────────────────────────┘  │ │
│  └─────────────────────┘  └──────────────────────────────────┘ │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  PREVIEW                                                  │  │
│  │  ┌──────────────────┐  ┌──────────────────┐             │  │
│  │  │   ORIGINAL       │  │   MUTATED        │             │  │
│  │  │                  │  │                  │             │  │
│  │  │   [Image]        │  │   [Image]        │             │  │
│  │  │                  │  │                  │             │  │
│  │  │ img1.png         │  │ img1_blur_5.png  │             │  │
│  │  │ 1920x1080        │  │ 1920x1080        │             │  │
│  │  │ 2.4 MB           │  │ 2.3 MB           │             │  │
│  │  └──────────────────┘  └──────────────────┘             │  │
│  │  < Previous   Next >                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  RESULTS & DOWNLOAD                                      │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ ✓ Image1_blur_5.png       [Download]             │ │  │
│  │  │ ✓ Image2_blur_5.jpg        [Download]             │ │  │
│  │  │ ✓ Image3_blur_5.tiff       [Download]             │ │  │
│  │  │ ✓ manifest.json (metadata)  [Download]             │ │  │
│  │  │                                                    │ │  │
│  │  │ [Download All as ZIP]  [Download Manifest]        │ │  │
│  │  │ [Copy Metadata]        [View Comparison]          │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Technical Stack

### **Backend**
- **Framework**: Flask (Python) or FastAPI (modern alternative)
- **Image Processing**: Pillow (PIL), ImageMagick (via subprocess/Wand), OpenCV
- **Queue Management**: Celery + Redis (for background processing of large batches)
- **Storage**: Local filesystem + cloud storage option (AWS S3, Google Cloud Storage)
- **Database**: SQLite (local) or PostgreSQL (production)

### **Frontend**
- **Framework**: React.js or Vue.js
- **Real-time Preview**: WebSockets or Server-Sent Events
- **UI Kit**: Bootstrap 5 / Material-UI
- **Image Comparison**: Before-After slider component
- **File Upload**: Dropzone.js or Fine Uploader

### **Deployment**
- **Server**: Nginx + Gunicorn (Flask) or Uvicorn (FastAPI)
- **Containerization**: Docker + Docker Compose
- **Cloud Options**: Heroku, AWS EC2, DigitalOcean, Azure App Service
- **Storage**: Local disk for dev, S3 for production

---

## 📊 Data Management

### **Mutation Metadata Output**

Every mutated image includes metadata (JSON manifest):

```json
{
  "job_id": "job_abc123xyz",
  "timestamp": "2024-03-23T15:30:45Z",
  "research_paper": "Image Mutations Impact on Classifier",
  "mutations_applied": [
    {
      "mutation_type": "blur",
      "parameters": {
        "sigma": 5,
        "radius": 0
      },
      "execution_time_ms": 234
    }
  ],
  "images": [
    {
      "original_name": "test_image.jpg",
      "original_size_bytes": 2457600,
      "original_dimensions": [1920, 1080],
      "original_checksum": "abc123...",
      "mutated_name": "test_image_blur_5.jpg",
      "mutated_size_bytes": 2394856,
      "mutated_dimensions": [1920, 1080],
      "mutated_checksum": "def456...",
      "mutation_depth": 1
    }
  ],
  "total_processing_time_s": 2.34,
  "environment": {
    "imagemagick_version": "7.1.0",
    "python_version": "3.10"
  }
}
```

---

## 🎨 Mutation Reference Table (from CSV)

### Primary Mutation Categories

| #  | Filter | Type | Parameters | Range | Use Case |
|----|--------|------|-----------|-------|----------|
| 1  | Blur | Continuous | sigma | 0.1-50 | Gaussian blur testing |
| 2  | Border | Continuous | width | 0-200px | Edge padding |
| 3  | Charcoal | Continuous | radius | 0.1-20 | Sketch effect |
| 4  | Black-Threshold | Discrete | threshold | 10%-75% | Binary conversion |
| 5  | Colors | Discrete | palette_size | 2-256 | Color quantization |
| 6  | Colorize | Discrete | tone | R/G/B/K | Color tinting |
| 7  | Colorspace | Discrete | space | RGB/HSV/LAB/... | Color model change |
| 8  | Clip-Mask | Discrete | mask_image | filepath | Masking/clipping |
| 9  | Annotate | Discrete | text | custom | Text overlay |
| 10 | Chop | Continuous | x_pixels | 0-width | Cropping |

---

## 🚀 Implementation Phases

### **Phase 1: MVP (Weeks 1-2)**
- ✓ Basic Flask backend
- ✓ Single mutation application (blur, colors, colorize)
- ✓ Image upload & download
- ✓ Basic HTML frontend
- ✓ Local filesystem storage
- **Deliverable**: Working tool with 3-4 mutations

### **Phase 2: Feature Expansion (Weeks 3-4)**
- ✓ Add all continuous mutations
- ✓ Add discrete mutations
- ✓ Mutation pipeline mode
- ✓ React frontend
- ✓ Real-time preview
- ✓ Metadata export (JSON/CSV)
- **Deliverable**: Full feature set

### **Phase 3: Optimization & Polish (Weeks 5-6)**
- ✓ Batch processing with Celery
- ✓ Before-after comparison slider
- ✓ Stress test mode
- ✓ Dataset summary & statistics
- ✓ User session management
- ✓ Error handling & validation
- **Deliverable**: Production-ready tool

### **Phase 4: Deployment & Research Integration (Week 7)**
- ✓ Docker containerization
- ✓ Cloud deployment
- ✓ Analytics/logging
- ✓ Documentation
- ✓ Research citation in UI
- **Deliverable**: Live tool accessible to public

---

## 📝 User Workflow Examples

### **Example 1: Simple Blur Test**
```
1. Upload image
2. Select "Single Mutation" mode
3. Select "Blur"
4. Set Sigma = 10
5. Click "Apply"
6. Review preview
7. Download "image_blur_10.jpg"
```

### **Example 2: Robustness Testing (Pipeline)**
```
1. Upload 5 test images
2. Select "Mutation Pipeline" mode
3. Add mutations:
   - Blur (sigma=5)
   - Compress (quality=70)
   - Rotate (45°)
4. Click "Apply Pipeline"
5. Download all 5 × 3 = 15 mutated images
6. Use for classifier testing
```

### **Example 3: Stress Testing (Random)**
```
1. Upload image
2. Select "Stress Test" mode
3. Configure:
   - Mutations: Blur, Brightness, Noise
   - Intensity: High
   - Variants per image: 20
4. Click "Generate 20 Random Mutations"
5. Wait ~30 seconds
6. Download ZIP with 20 variants
7. Get statistics: "Created 20 variations"
```

---

## 🔬 Research Integration

The tool will prominently feature:

1. **Citation to Research Paper**
   - "Based on: Evaluation of the Impact of Image Mutations..."
   - Link to paper DOI
   - Citation format (BibTeX + APA)

2. **Mutation Methodology Section**
   - Explain why each mutation matters
   - Link to specific findings from paper
   - Suggested mutation combinations

3. **Results Tracking**
   - Store all mutations in database
   - Generate usage statistics
   - Track impact on classifier robustness

4. **Export for Research**
   - Dataset manifest with mutation parameters
   - Reproducibility information
   - Suggested citation for people using tool

---

## 📦 Deliverables

### **Code**
```
image-mutation-tool/
├── backend/
│   ├── app.py                 # Flask app
│   ├── mutations.py           # Mutation logic
│   ├── imagemagick_wrapper.py # IM interface
│   ├── storage.py             # File management
│   ├── metadata.py            # Manifest generation
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageUpload.jsx
│   │   │   ├── MutationControls.jsx
│   │   │   ├── PreviewWindow.jsx
│   │   │   └── ResultsPanel.jsx
│   │   └── App.jsx
│   └── package.json
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── README.md
│   ├── INSTALLATION.md
│   ├── USER_GUIDE.md
│   └── MUTATION_REFERENCE.md
└── tests/
    ├── test_mutations.py
    └── test_api.py
```

### **Documentation**
- Installation guide
- User guide with screenshots
- API documentation
- Mutation reference (from CSV)
- Deployment instructions
- Research methodology

### **Artifacts**
- Master filter CSV (enhanced with UI mappings)
- Sample mutation profiles
- Test dataset
- Deployment templates

---

## 🎓 Future Enhancements

1. **ML Integration**
   - Test classifier robustness directly in tool
   - Automatic evaluation on uploaded models

2. **Mutation Analytics**
   - Which mutations affect classifiers most?
   - Heatmaps of sensitivity

3. **Collaborative Features**
   - Share mutation profiles
   - Compare results across users

4. **Advanced Features**
   - GAN-based mutations
   - Adversarial perturbations
   - Multi-image blending

5. **Mobile Support**
   - Mobile-friendly UI
   - Native apps for iOS/Android

---

## 👥 Expected Users

1. **ML Researchers** - Testing classifier robustness
2. **QA Engineers** - Image processing validation
3. **Data Scientists** - Augmentation & dataset generation
4. **Computer Vision Teams** - Model evaluation
5. **Academic Researchers** - Reproducibility studies
6. **Students** - Learning about image mutations

---

## ✅ Success Metrics

- ✓ Tool processes images in <5s (single mutation)
- ✓ Batch mode handles 100+ images reliably
- ✓ >95% uptime on deployment
- ✓ <100ms UI response time
- ✓ Support 50+ concurrent users
- ✓ >500 citations of research paper via tool
- ✓ >1000 mutated images generated monthly (target growth)

