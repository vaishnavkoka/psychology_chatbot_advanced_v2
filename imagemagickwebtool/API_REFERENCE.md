# Image Mutation Tool - API Reference

Complete API documentation for the Image Mutation Tool backend.

**Base URL:** `http://localhost:5000/api` (development)

---

## Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Data Models](#data-models)
4. [Error Handling](#error-handling)
5. [Examples](#examples)

---

## Authentication

Currently, the API does not require authentication. Future versions will support:
- API Keys
- OAuth 2.0
- JWT Tokens

---

## Endpoints

### 1. Get All Mutations

Returns list of all available mutations with their parameters.

```
GET /mutations
```

**Response (200 OK):**

```json
{
  "continuous": {
    "blur": {
      "name": "blur",
      "description": "Gaussian blur effect",
      "parameters": {
        "sigma": {
          "type": "float",
          "min": 0.1,
          "max": 50,
          "default": 5
        }
      }
    },
    "brightness": {
      "name": "brightness",
      "description": "Adjust image brightness",
      "parameters": {
        "percentage": {
          "type": "int",
          "min": -100,
          "max": 100,
          "default": 0
        }
      }
    }
  },
  "discrete": {
    "color_reduce": {
      "name": "color_reduce",
      "description": "Reduce color palette",
      "parameters": {
        "colors": {
          "type": "choice",
          "choices": [2, 4, 8, 16, 32, 64, 128, 256],
          "default": 256
        }
      }
    },
    "colorize": {
      "name": "colorize",
      "description": "Apply color tint",
      "parameters": {
        "tone": {
          "type": "choice",
          "choices": ["red", "green", "blue", "yellow", "cyan", "magenta", "grayscale"],
          "default": "red"
        }
      }
    }
  },
  "all": { ... }
}
```

**cURL Example:**

```bash
curl -X GET http://localhost:5000/api/mutations
```

---

### 2. Upload Images

Upload one or more images to the server. Creates a new job session.

```
POST /upload
Content-Type: multipart/form-data
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `files` | file[] | Yes | Image files (JPEG, PNG, GIF, WebP, TIFF, BMP) |

**Response (201 Created):**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-15T10:30:00Z",
  "uploaded_files": 3,
  "files": [
    {
      "filename": "image1.jpg",
      "original_path": "uploads/550e8400-e29b-41d4-a716-446655440000/image1.jpg",
      "size_bytes": 102400,
      "width": 1920,
      "height": 1080,
      "format": "jpeg"
    },
    {
      "filename": "image2.png",
      "original_path": "uploads/550e8400-e29b-41d4-a716-446655440000/image2.png",
      "size_bytes": 256000,
      "width": 2560,
      "height": 1440,
      "format": "png"
    },
    {
      "filename": "image3.gif",
      "original_path": "uploads/550e8400-e29b-41d4-a716-446655440000/image3.gif",
      "size_bytes": 512000,
      "width": 640,
      "height": 480,
      "format": "gif"
    }
  ],
  "max_file_size_mb": 50,
  "storage_path": "uploads/550e8400-e29b-41d4-a716-446655440000"
}
```

**Error Responses:**

```json
{
  "error": "No files provided",
  "status": 400
}
```

```json
{
  "error": "File size exceeds maximum (50MB)",
  "status": 413,
  "file": "large_image.jpg"
}
```

```json
{
  "error": "Unsupported file format: bmp",
  "status": 415,
  "supported_formats": ["jpeg", "png", "gif", "webp", "tiff", "bmp"]
}
```

**cURL Example:**

```bash
# Single file
curl -X POST \
  -F "files=@image1.jpg" \
  http://localhost:5000/api/upload

# Multiple files
curl -X POST \
  -F "files=@image1.jpg" \
  -F "files=@image2.png" \
  -F "files=@image3.gif" \
  http://localhost:5000/api/upload
```

**Python Example:**

```python
import requests

files = [
    ('files', open('image1.jpg', 'rb')),
    ('files', open('image2.png', 'rb'))
]

response = requests.post(
    'http://localhost:5000/api/upload',
    files=files
)

data = response.json()
print(f"Job ID: {data['job_id']}")
```

---

### 3. Apply Mutation

Apply a mutation to one or more uploaded images.

```
POST /mutate
Content-Type: application/json
```

**Request Body:**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "mutation": "blur",
  "parameters": {
    "sigma": 10
  },
  "image_paths": [
    "uploads/550e8400-e29b-41d4-a716-446655440000/image1.jpg",
    "uploads/550e8400-e29b-41d4-a716-446655440000/image2.png"
  ]
}
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `job_id` | string | Yes | Job ID from upload endpoint |
| `mutation` | string | Yes | Mutation name (from /mutations endpoint) |
| `parameters` | object | Yes | Mutation parameters (structure varies by mutation) |
| `image_paths` | string[] | Yes | Paths of images to mutate (returned from upload) |

**Response (200 OK):**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "mutation": "blur",
  "parameters": {
    "sigma": 10
  },
  "status": "completed",
  "processed_images": [
    {
      "original": "image1.jpg",
      "mutated": "image1_blur_s10.jpg",
      "mutation_path": "outputs/550e8400-e29b-41d4-a716-446655440000/image1_blur_s10.jpg",
      "processing_time_ms": 1250,
      "output_size_bytes": 98765
    },
    {
      "original": "image2.png",
      "mutated": "image2_blur_s10.png",
      "mutation_path": "outputs/550e8400-e29b-41d4-a716-446655440000/image2_blur_s10.png",
      "processing_time_ms": 2100,
      "output_size_bytes": 234567
    }
  ],
  "total_processing_time_ms": 3350
}
```

**Error Responses:**

```json
{
  "error": "Invalid mutation: blur_invalid",
  "status": 400,
  "available_mutations": ["blur", "brightness", "rotation", ...]
}
```

```json
{
  "error": "Invalid parameter: sigma must be between 0.1 and 50",
  "status": 422,
  "parameter": "sigma",
  "value": 100,
  "valid_range": "0.1-50"
}
```

```json
{
  "error": "Image file not found: uploads/unknown.jpg",
  "status": 404
}
```

**cURL Examples:**

```bash
# Simple blur
curl -X POST http://localhost:5000/api/mutate \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "mutation": "blur",
    "parameters": {"sigma": 10},
    "image_paths": ["uploads/550e8400-e29b-41d4-a716-446655440000/image1.jpg"]
  }'

# Brightness adjustment
curl -X POST http://localhost:5000/api/mutate \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "mutation": "brightness",
    "parameters": {"percentage": 50},
    "image_paths": ["uploads/550e8400-e29b-41d4-a716-446655440000/image1.jpg"]
  }'

# Color reduction
curl -X POST http://localhost:5000/api/mutate \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "mutation": "color_reduce",
    "parameters": {"colors": 32},
    "image_paths": ["uploads/550e8400-e29b-41d4-a716-446655440000/image2.png"]
  }'
```

**Python Example:**

```python
import requests
import json

response = requests.post(
    'http://localhost:5000/api/mutate',
    headers={'Content-Type': 'application/json'},
    json={
        'job_id': 'job-id-here',
        'mutation': 'blur',
        'parameters': {'sigma': 10},
        'image_paths': ['uploads/job-id-here/image1.jpg']
    }
)

result = response.json()
print(f"Status: {result['status']}")
for img in result['processed_images']:
    print(f"  {img['original']} -> {img['mutated']} ({img['processing_time_ms']}ms)")
```

---

### 4. Download Mutated Image

Download a single mutated image file.

```
GET /download/<job_id>/<filename>
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `job_id` | string (path) | Yes | Job ID |
| `filename` | string (path) | Yes | Filename of mutated image |

**Response (200 OK):**

Binary image file with appropriate Content-Type header.

**Headers:**

```
Content-Type: image/jpeg (or appropriate image type)
Content-Disposition: attachment; filename="image1_blur_s10.jpg"
Content-Length: 98765
```

**Error Responses:**

```json
{
  "error": "File not found",
  "status": 404,
  "job_id": "invalid-job",
  "filename": "image1.jpg"
}
```

**cURL Example:**

```bash
# Download to file
curl -X GET http://localhost:5000/api/download/550e8400-e29b-41d4-a716-446655440000/image1_blur_s10.jpg \
  -o image1_blur_s10.jpg

# Display image metadata
curl -I http://localhost:5000/api/download/550e8400-e29b-41d4-a716-446655440000/image1_blur_s10.jpg
```

**Python Example:**

```python
import requests

response = requests.get(
    'http://localhost:5000/api/download/job-id-here/image1_blur_s10.jpg'
)

if response.status_code == 200:
    with open('downloaded_image.jpg', 'wb') as f:
        f.write(response.content)
    print("Image downloaded successfully")
```

---

### 5. Get Mutation Manifest

Get metadata about all mutations performed on images in a job.

```
GET /manifest/<job_id>
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `job_id` | string (path) | Yes | Job ID |

**Response (200 OK):**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T10:30:00Z",
  "mutations": [
    {
      "mutation_id": "mut-001",
      "name": "blur",
      "parameters": {"sigma": 10},
      "applied_at": "2024-01-15T10:31:00Z",
      "images": [
        {
          "original": "image1.jpg",
          "mutated": "image1_blur_s10.jpg",
          "mutation_path": "outputs/.../image1_blur_s10.jpg",
          "processing_time_ms": 1250
        },
        {
          "original": "image2.png",
          "mutated": "image2_blur_s10.png",
          "mutation_path": "outputs/.../image2_blur_s10.png",
          "processing_time_ms": 2100
        }
      ]
    },
    {
      "mutation_id": "mut-002",
      "name": "brightness",
      "parameters": {"percentage": 50},
      "applied_at": "2024-01-15T10:32:00Z",
      "images": [
        {
          "original": "image1.jpg",
          "mutated": "image1_brightness_p50.jpg",
          "mutation_path": "outputs/.../image1_brightness_p50.jpg",
          "processing_time_ms": 950
        }
      ]
    }
  ],
  "total_mutations": 2,
  "total_images_processed": 3,
  "research_metadata": {
    "paper_title": "Evaluation of Image Mutations on Origin Classification",
    "mutations_studied": ["blur", "brightness", "color_reduce"],
    "classification_metrics": {}
  }
}
```

**cURL Example:**

```bash
curl -X GET http://localhost:5000/api/manifest/550e8400-e29b-41d4-a716-446655440000
```

**Python Example:**

```python
import requests
import json

response = requests.get(
    'http://localhost:5000/api/manifest/job-id-here'
)

manifest = response.json()
print(f"Total mutations applied: {manifest['total_mutations']}")
print(f"Total images processed: {manifest['total_images_processed']}")

for mutation in manifest['mutations']:
    print(f"\n{mutation['name']} (sigma={mutation['parameters']})")
    for img in mutation['images']:
        print(f"  {img['original']} -> {img['mutated']}")
```

---

### 6. Health Check

Check if the API is running and accessible.

```
GET /health
```

**Response (200 OK):**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "uptime_seconds": 3600,
  "services": {
    "database": "ok",
    "imagemagick": "ok",
    "storage": "ok"
  }
}
```

**cURL Example:**

```bash
curl http://localhost:5000/api/health
```

---

## Data Models

### MutationParameter

Defines a parameter for a mutation.

```json
{
  "type": "float|int|choice|bool",
  "min": 0.1,
  "max": 50,
  "step": 0.1,
  "default": 5,
  "choices": [2, 4, 8, 16, 32, 64, 128, 256],
  "description": "Sigma value for Gaussian blur"
}
```

### Mutation

Represents an available mutation with its parameters.

```json
{
  "name": "blur",
  "description": "Apply Gaussian blur to image",
  "category": "continuous",
  "parameters": {
    "sigma": {
      "type": "float",
      "min": 0.1,
      "max": 50,
      "default": 5
    }
  }
}
```

### Job

Represents a user session with uploaded images.

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T10:30:00Z",
  "status": "active",
  "uploaded_images": 10,
  "processed_images": 25,
  "storage_usage_bytes": 5242880,
  "expires_at": "2024-01-22T10:30:00Z"
}
```

---

## Error Handling

### Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Mutation applied successfully |
| 201 | Created | Job created from upload |
| 400 | Bad Request | Invalid mutation name |
| 404 | Not Found | Job ID or file not found |
| 413 | Payload Too Large | File exceeds max size |
| 415 | Unsupported Media Type | Invalid image format |
| 422 | Unprocessable Entity | Invalid parameters |
| 500 | Server Error | ImageMagick subprocess failure |

### Error Response Format

```json
{
  "error": "Human-readable error message",
  "status": 400,
  "error_code": "INVALID_MUTATION",
  "details": {
    "field": "mutation",
    "value": "blur_invalid",
    "reason": "Unknown mutation"
  }
}
```

---

## Examples

### Complete Upload → Mutate → Download Workflow

```bash
#!/bin/bash

# Step 1: Upload images
echo "Uploading images..."
UPLOAD_RESPONSE=$(curl -s -X POST \
  -F "files=@image1.jpg" \
  -F "files=@image2.png" \
  http://localhost:5000/api/upload)

JOB_ID=$(echo $UPLOAD_RESPONSE | jq -r '.job_id')
echo "Job ID: $JOB_ID"

# Step 2: Apply blur mutation
echo "Applying blur mutation..."
curl -s -X POST http://localhost:5000/api/mutate \
  -H "Content-Type: application/json" \
  -d "{
    \"job_id\": \"$JOB_ID\",
    \"mutation\": \"blur\",
    \"parameters\": {\"sigma\": 10},
    \"image_paths\": [
      \"uploads/$JOB_ID/image1.jpg\",
      \"uploads/$JOB_ID/image2.png\"
    ]
  }" | jq '.'

# Step 3: Get manifest
echo "Retrieving mutation manifest..."
curl -s http://localhost:5000/api/manifest/$JOB_ID | jq '.'

# Step 4: Download results
echo "Downloading mutated images..."
curl -O http://localhost:5000/api/download/$JOB_ID/image1_blur_s10.jpg
curl -O http://localhost:5000/api/download/$JOB_ID/image2_blur_s10.png

echo "Done!"
```

### Python Integration Example

```python
import requests
import json
from pathlib import Path

class ImageMutationAPI:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url
    
    def upload_images(self, image_paths):
        """Upload images and return job_id"""
        files = [('files', open(path, 'rb')) for path in image_paths]
        response = requests.post(f"{self.base_url}/upload", files=files)
        response.raise_for_status()
        return response.json()
    
    def apply_mutation(self, job_id, mutation, parameters, image_paths):
        """Apply mutation to images"""
        response = requests.post(
            f"{self.base_url}/mutate",
            json={
                'job_id': job_id,
                'mutation': mutation,
                'parameters': parameters,
                'image_paths': image_paths
            }
        )
        response.raise_for_status()
        return response.json()
    
    def download_image(self, job_id, filename, output_path):
        """Download mutated image"""
        response = requests.get(
            f"{self.base_url}/download/{job_id}/{filename}"
        )
        response.raise_for_status()
        
        Path(output_path).write_bytes(response.content)
        return output_path
    
    def get_manifest(self, job_id):
        """Get mutation manifest"""
        response = requests.get(f"{self.base_url}/manifest/{job_id}")
        response.raise_for_status()
        return response.json()

# Usage
api = ImageMutationAPI()

# Upload
result = api.upload_images(['image1.jpg', 'image2.png'])
job_id = result['job_id']

# Apply mutations
api.apply_mutation(job_id, 'blur', {'sigma': 10}, 
                   [f'uploads/{job_id}/image1.jpg'])
api.apply_mutation(job_id, 'brightness', {'percentage': 50},
                   [f'uploads/{job_id}/image1.jpg'])

# Download
api.download_image(job_id, 'image1_blur_s10.jpg', 'output1.jpg')
api.download_image(job_id, 'image1_brightness_p50.jpg', 'output2.jpg')

# Get manifest
manifest = api.get_manifest(job_id)
print(json.dumps(manifest, indent=2))
```

---

## Rate Limiting

Currently not enforced, but planned for Phase 2:
- 100 requests per minute per IP
- 1GB storage per job
- 24-hour job session timeout

---

## CORS Headers

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

Configurable in `backend/config.py`

---

## See Also

- [QUICK_START.md](QUICK_START.md) - Getting started guide
- [BACKEND_IMPLEMENTATION.md](BACKEND_IMPLEMENTATION.md) - Backend code details
- [TOOL_DESIGN_PLAN.md](TOOL_DESIGN_PLAN.md) - Complete feature documentation

