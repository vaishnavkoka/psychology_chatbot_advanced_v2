# Image Format Preservation

## Overview
The Image Mutation Tool now supports **all common image formats** and preserves the input format for the output.

## Supported Formats
- `.jpg` / `.jpeg` - JPEG format
- `.png` - PNG format (with transparency support)
- `.gif` - GIF format
- `.bmp` - Bitmap format
- `.webp` - WebP format
- `.tiff` / `.tif` - TIFF format

## How It Works

### Input Processing
When you upload an image:
1. **Format Detection**: The tool detects the image format from the file extension
2. **Format Preservation**: The original format is stored and used for output
3. **Dual Processing**: 
   - **Wand First**: Attempts to use ImageMagick's Wand library for faster processing
   - **PIL Fallback**: If Wand can't handle the format, automatically falls back to PIL (Python Image Library)

### Output Processing
When mutations are applied:
- **Same Format Output**: Result files use the same format as the input
- **Example**: 
  - Input: `screenshot.png` → Output: `screenshot_blur.png` (stays PNG)
  - Input: `photo.jpg` → Output: `photo_brightness.jpg` (stays JPEG)
  - Input: `image.bmp` → Output: `image_contrast.bmp` (stays BMP)

## Implementation Details

### Backend Logic (`backend/app.py`)

```python
# Format mapping
ext_to_format = {
    '.jpg': 'jpeg',
    '.jpeg': 'jpeg',
    '.png': 'png',
    '.gif': 'gif',
    '.webp': 'webp',
    '.bmp': 'bmp',
    '.tiff': 'tiff',
    '.tif': 'tiff'
}
```

### Processing Pipeline
1. Read uploaded file
2. Try to open with Wand (ImageMagick)
3. If Wand fails (e.g., missing PNG delegates), use PIL
4. Apply mutation using appropriate library
5. Save result in original format

### Supported Mutations
All mutations work with all formats:
- **grayscale** - Convert to grayscale
- **blur** - Apply Gaussian blur
- **brightness** - Adjust brightness level
- **rotation** - Rotate image by degrees
- **contrast** - Adjust contrast level
- **saturation** - Adjust color saturation
- **color_reduce** - Reduce number of colors
- **colorize** - Apply color tint

## Download Filenames
Download filenames automatically include the correct extension:
- `screenshot_grayscale.png` (for PNG images)
- `photo_blur.jpg` (for JPEG images)
- `image_rotation.bmp` (for BMP images)

## MIME Types
The correct MIME type is automatically set for downloads based on format:
- PNG: `image/png`
- JPEG: `image/jpeg`
- GIF: `image/gif`
- BMP: `image/bmp`
- WebP: `image/webp`
- TIFF: `image/tiff`

## Testing
Test format preservation with different file types:

```bash
# PNG Test
curl -X POST -F "image=@test.png" -F "mutation=grayscale" \
  http://localhost:5000/api/mutate

# JPEG Test
curl -X POST -F "image=@photo.jpg" -F "mutation=blur" \
  http://localhost:5000/api/mutate

# BMP Test
curl -X POST -F "image=@graphic.bmp" -F "mutation=contrast" \
  http://localhost:5000/api/mutate
```

All responses will show the original format is preserved in:
- `original_url` - URL to original image
- `result_url` - URL to mutated image
- `download_filename` - Filename for download (includes correct extension)
