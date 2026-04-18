# Filter Parameter Reference

## 🎯 Complete Filter-to-Parameter Mapping

This document shows exactly what parameters each filter expects and their valid ranges.

---

## CONTINUOUS FILTERS (Range-based Parameters)

### **1. Blur (Gaussian)**
```
Mutation Name: blur
Parameter Key: sigma
Type: float
Range: 0.1 to 20
Default: 5
Step: 0.5
Description: Blur strength where 0.1=sharp, 20=extreme blur

Example API Call:
POST /api/mutate
mutation=blur
parameters={"sigma": 8.5}
```

### **2. Black Threshold**
```
Mutation Name: black_threshold
Parameter Key: percentage
Type: int
Range: 0 to 100%
Default: 25%
Step: 5
Description: Brightness threshold (pixels below this become black)

Example:
mutation=black_threshold
parameters={"percentage": 40}
```

### **3. Border**
```
Mutation Name: border
Parameter Key: pixels
Type: int
Range: 0 to 100 pixels
Default: 10px
Step: 5
Description: Width of colored border to add

Example:
mutation=border
parameters={"pixels": 20}
```

### **4. Charcoal Effect**
```
Mutation Name: charcoal
Parameter Key: radius
Type: float
Range: 0.2 to 10
Default: 5
Step: 0.2
Description: Sketch intensity (0.2=subtle, 10=heavy)

Example:
mutation=charcoal
parameters={"radius": 3.5}
```

### **5. Color Palette Reduction**
```
Mutation Name: color_reduce
Parameter Key: colors
Type: int
Range: 2 to 256
Default: 16
Step: 1
Description: Number of colors (2=B&W, 256=full color)

Example:
mutation=color_reduce
parameters={"colors": 8}
```

### **6. Brightness**
```
Mutation Name: brightness
Parameter Key: percentage
Type: int
Range: -100 to +100%
Default: 0%
Step: 5
Description: Brightness adjustment (negative=darker, positive=lighter)

Example:
mutation=brightness
parameters={"percentage": 30}
```

### **7. Rotation**
```
Mutation Name: rotation
Parameter Key: degrees
Type: float
Range: 0 to 360°
Default: 0°
Step: 5
Description: Image rotation angle (clockwise)

Example:
mutation=rotation
parameters={"degrees": 45}
```

### **8. Contrast**
```
Mutation Name: contrast
Parameter Key: percentage
Type: int
Range: -100 to +100%
Default: 0%
Step: 5
Description: Contrast adjustment (negative=flatten, positive=enhance)

Example:
mutation=contrast
parameters={"percentage": 50}
```

### **9. Saturation**
```
Mutation Name: saturation
Parameter Key: percentage
Type: int
Range: -100 to +200%
Default: 0%
Step: 10
Description: Color intensity (negative=desaturate, positive=vibrant)

Example:
mutation=saturation
parameters={"percentage": 100}
```

---

## DISCRETE FILTERS (Choice-based Parameters)

### **1. Colorize**
```
Mutation Name: colorize
Parameter Key: tone
Type: string (choice)
Valid Options:
  - red       → Red color tint
  - green     → Green color tint
  - blue      → Blue color tint
  - yellow    → Yellow color tint
  - cyan      → Cyan color tint
  - magenta   → Magenta color tint
  - sepia     → Sepia/vintage tone
Default: blue

Example:
mutation=colorize
parameters={"tone": "sepia"}
```

### **2. Colorspace**
```
Mutation Name: colorspace
Parameter Key: colorspace
Type: string (choice)
Valid Options:
  - RGB       → Standard color (unchanged)
  - Gray      → Black and white
  - HSV       → Hue/Saturation/Value (artistic)
  - HCL       → Hue/Chroma/Lightness (perceptual)
  - CMY       → Cyan/Magenta/Yellow (print)
  - CMYK      → With Black channel (professional print)
  - YCbCr     → Video/broadcast standard
  - Lab       → LAB perceptual color space
Default: RGB

Example:
mutation=colorspace
parameters={"colorspace": "HSV"}
```

### **3. Text Annotation**
```
Mutation Name: annotate
Parameters: (Multiple - all required)
  
  text:     Type: string
            Max Length: 100 characters
            Description: Watermark text
            Example: "© 2024"
  
  position: Type: string (choice)
            Valid Options:
              - center       → Center of image
              - northwest    → Top-left corner
              - north        → Top center
              - northeast    → Top-right corner
              - west         → Left side, middle
              - east         → Right side, middle
              - southwest    → Bottom-left corner
              - south        → Bottom center
              - southeast    → Bottom-right corner
            Default: center
  
  fontSize: Type: string (choice)
            Valid Options:
              - 24   → Small (24px)
              - 36   → Medium (36px)
              - 48   → Large (48px)
              - 72   → Extra Large (72px)
            Default: 36
            
Complete Example:
mutation=annotate
parameters={
  "text": "CONFIDENTIAL",
  "position": "southeast",
  "fontSize": "48"
}

Result: White text with black outline, positioned at bottom-right, 48px font
```

### **4. Chop/Crop**
```
Mutation Name: chop
Parameters: (Multiple)

  type:     Type: string (choice)
            Valid Options:
              - horizontal → Remove from left and right sides
              - vertical   → Remove from top and bottom
              - center     → Crop from center outward
            Default: horizontal

  value:    Type: int
            Range: 1 to 200 pixels
            Description: Number of pixels to remove
            Default: 50

Example:
mutation=chop
parameters={
  "type": "center",
  "value": 75
}

Result: Crops 75px from all sides (center crop)
```

### **5. Grayscale**
```
Mutation Name: grayscale
Parameters: (None - no parameters required)
Description: Simple black and white conversion

Example:
mutation=grayscale
parameters={}

Result: Full grayscale conversion (no adjustment needed)
```

---

## 📋 Quick Parameter Table

| Filter | Mutation Name | Key Parameter(s) | Type | Range | Example |
|--------|---------------|------------------|------|-------|---------|
| Blur | `blur` | `sigma` | float | 0.1-20 | 8.5 |
| Black Threshold | `black_threshold` | `percentage` | int | 0-100 | 30 |
| Border | `border` | `pixels` | int | 0-100 | 15 |
| Charcoal | `charcoal` | `radius` | float | 0.2-10 | 5.5 |
| Color Palette | `color_reduce` | `colors` | int | 2-256 | 16 |
| Brightness | `brightness` | `percentage` | int | -100 to +100 | 40 |
| Rotation | `rotation` | `degrees` | float | 0-360 | 45 |
| Contrast | `contrast` | `percentage` | int | -100 to +100 | 50 |
| Saturation | `saturation` | `percentage` | int | -100 to +200 | 100 |
| Colorize | `colorize` | `tone` | string | 7 options | "sepia" |
| Colorspace | `colorspace` | `colorspace` | string | 8 options | "HSV" |
| Annotation | `annotate` | `text`, `position`, `fontSize` | string, string, string | see above | see above |
| Chop | `chop` | `type`, `value` | string, int | see above | see above |
| Grayscale | `grayscale` | (none) | - | - | - |

---

## 🔧 API Usage Examples

### **Example 1: Blur with high sigma**
```bash
curl -X POST http://localhost:5000/api/mutate \
  -F "image=@photo.jpg" \
  -F "mutation=blur" \
  -F "parameters={\"sigma\": 15}"
```

### **Example 2: Add watermark**
```bash
curl -X POST http://localhost:5000/api/mutate \
  -F "image=@photo.jpg" \
  -F "mutation=annotate" \
  -F "parameters={\"text\": \"© 2024\", \"position\": \"southeast\", \"fontSize\": \"48\"}"
```

### **Example 3: Convert to HSV colorspace**
```bash
curl -X POST http://localhost:5000/api/mutate \
  -F "image=@photo.jpg" \
  -F "mutation=colorspace" \
  -F "parameters={\"colorspace\": \"HSV\"}"
```

### **Example 4: Posterize effect (reduce colors)**
```bash
curl -X POST http://localhost:5000/api/mutate \
  -F "image=@photo.jpg" \
  -F "mutation=color_reduce" \
  -F "parameters={\"colors\": 4}"
```

### **Example 5: Charcoal sketch**
```bash
curl -X POST http://localhost:5000/api/mutate \
  -F "image=@photo.jpg" \
  -F "mutation=charcoal" \
  -F "parameters={\"radius\": 4}"
```

---

## ✅ Parameter Validation

The backend validates all parameters:
- **Range checks**: Values outside [min, max] are rejected
- **Type checks**: Wrong data types generate errors
- **String choices**: Only valid options are accepted
- **Required fields**: Missing parameters return error messages

Example error response:
```json
{
  "error": "Mutation failed: sigma value 50 exceeds maximum of 20"
}
```

---

## 📝 Frontend to Backend Mapping

How the UI sends parameters:

```javascript
// CONTINUOUS FILTER (Blur)
const params = { sigma: document.getElementById('blurSlider').value };
// Sent as: {"sigma": 8.5}

// DISCRETE FILTER (Annotation)
const params = {
  text: document.getElementById('annotateText').value,
  position: document.getElementById('annotatePosition').value,
  fontSize: document.getElementById('annotateFontSize').value
};
// Sent as: {"text": "TEST", "position": "center", "fontSize": "36"}
```

---

## 🎨 Common Parameter Presets

### **Soft Focus (Portrait)**
```
blur: sigma = 8
saturation: percentage = 30 (slight desaturate)
brightness: percentage = 10 (slightly brighter)
```

### **Vintage Effect**
```
colorize: tone = "sepia"
saturation: percentage = -30 (less vibrant)
contrast: percentage = 20 (slight boost)
```

### **Sketch Art**
```
charcoal: radius = 3
color_reduce: colors = 2 (pure B&W)
saturation: percentage = -100 (desaturate fully)
```

### **Dramatic HDR**
```
contrast: percentage = 100 (double contrast)
saturation: percentage = 150 (very vibrant)
brightness: percentage = -20 (darker)
```

### **Instagram B&W**
```
colorspace: "Gray"
contrast: percentage = 50
brightness: percentage = 5
border: pixels = 10 (white frame)
```

---

## 🚀 Integration Guide

**When building custom apps:**

1. **Get filter definitions**: `GET /api/mutations`
2. **Extract parameter details**: Use response to build UI
3. **Validate user input**: Check against min/max/options
4. **Send to backend**: POST with mutation name + parameters

```javascript
// Step 1: Fetch available filters
fetch('/api/mutations').then(r => r.json()).then(filters => {
  console.log(filters.continuous.blur.parameters.sigma.max); // 20
});

// Step 2: Validate user input
function validateParameter(mutation, param, value) {
  const def = filterDefinitions[mutation].parameters[param];
  return value >= def.min && value <= def.max;
}

// Step 3: Send to API
fetch('/api/mutate', {
  method: 'POST',
  body: formData // with image, mutation, parameters
});
```

---

**Reference Version: 2.0**
**Last Updated: 2024-03-23**
**Status: Complete & Validated**
