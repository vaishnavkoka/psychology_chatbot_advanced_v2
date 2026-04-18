# Image Mutation Tool - Developer Guide

Complete guide for developers working on the Image Mutation Tool codebase.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Code Organization](#code-organization)
3. [Adding New Mutations](#adding-new-mutations)
4. [Extending the Backend](#extending-the-backend)
5. [Extending the Frontend](#extending-the-frontend)
6. [Testing](#testing)
7. [Performance Optimization](#performance-optimization)
8. [Debugging](#debugging)
9. [Deployment](#deployment)
10. [Contributing Guidelines](#contributing-guidelines)

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  ImageUpload → MutationSelector → Preview → Results          │
└────────────────────┬────────────────────────────────────────┘
                     │
                  HTTP/API
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Backend (Flask)                             │
│  Routes → Validation → MutationRegistry → ImageMagick        │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼───┐  ┌────▼────┐  ┌────▼────┐
   │ Storage │  │ImageMagick  │Celery │
   │ (Local) │  │(subprocess) │(Queue)│
   └────────┘  └─────────┘  └────────┘
```

### Data Flow

1. **Upload Phase**: User uploads images → Server stores in `/uploads/{job_id}/`
2. **Selection Phase**: User selects mutation and parameters → Frontend validates
3. **Processing Phase**: Backend applies mutation using ImageMagick → Output stored in `/outputs/{job_id}/`
4. **Download Phase**: User downloads result or batch ZIP

### Key Design Patterns

- **Registry Pattern** (MutationRegistry): Centralized mutation catalog
- **Abstract Base Class Pattern** (MutationBase): Template for all mutations
- **Service Layer Pattern**: Separation of API routes from business logic
- **Component Composition Pattern** (React): Nested, reusable components

---

## Code Organization

### Backend Structure

```
backend/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
│
├── mutations/
│   ├── __init__.py
│   ├── base.py                 # MutationBase abstract class
│   ├── continuous.py           # Continuous mutations (blur, brightness, etc.)
│   ├── discrete.py             # Discrete mutations (color reduce, etc.)
│   └── registry.py             # MutationRegistry class
│
├── core/
│   ├── mutation_executor.py    # Executes ImageMagick commands
│   └── image_handler.py        # Image processing utilities
│
├── storage/
│   ├── local_storage.py        # Local filesystem operations
│   └── manifest.py             # Mutation metadata tracking
│
├── api/
│   ├── routes.py               # Flask route definitions
│   ├── validators.py           # Input validation
│   └── schemas.py              # Request/response schemas
│
├── models/
│   ├── job.py                  # Job model
│   └── mutation_history.py     # Mutation tracking
│
└── tests/
    ├── test_mutations.py       # Mutation tests
    ├── test_api.py             # API endpoint tests
    ├── test_executor.py        # Executor tests
    └── fixtures/               # Test images
```

### Frontend Structure

```
frontend/src/
├── App.jsx                     # Main app component
├── index.js                    # React entry point
│
├── pages/
│   ├── HomePage.jsx            # Landing page
│   ├── MutationPage.jsx        # Main tool page
│   ├── BatchPage.jsx           # Batch processing page
│   └── DocumentationPage.jsx   # Help/docs page
│
├── components/
│   ├── ImageUpload.jsx         # File upload component
│   ├── MutationSelector.jsx    # Mutation selection
│   ├── ParameterControls.jsx   # Dynamic parameter UI
│   ├── PreviewWindow.jsx       # Image preview
│   ├── BeforeAfterSlider.jsx   # Comparison slider
│   └── ResultsPanel.jsx        # Results display
│
├── services/
│   └── api.js                  # API client
│
├── hooks/
│   ├── useImageMutations.js    # Mutation state hook
│   └── useJobManagement.js     # Job session hook
│
├── utils/
│   ├── validators.js           # Validation utilities
│   └── formatters.js           # Formatting utilities
│
└── styles/
    ├── index.css               # Global styles
    ├── components.css          # Component styles
    └── animations.css          # Animations
```

---

## Adding New Mutations

### Step 1: Implement the Mutation Class

Create a new file in `backend/mutations/` (continuous.py or discrete.py):

```python
# backend/mutations/continuous.py (for numeric parameters)

from mutations.base import MutationBase, MutationParameter
import subprocess
from pathlib import Path

class SharpenMutation(MutationBase):
    """Sharpen image using ImageMagick -sharpen"""
    
    def __init__(self):
        super().__init__(
            name="sharpen",
            description="Sharpen image with adjustable radius",
            category="continuous",
            parameters={
                "radius": MutationParameter(
                    type="float",
                    min=0.1,
                    max=10.0,
                    step=0.5,
                    default=1.0,
                    description="Sharpen radius in pixels"
                ),
                "sigma": MutationParameter(
                    type="float",
                    min=0.1,
                    max=5.0,
                    step=0.1,
                    default=1.0,
                    description="Sharpen sigma"
                )
            }
        )
    
    def validate_parameters(self, parameters):
        """Validate mutation parameters"""
        super().validate_parameters(parameters)
        
        # Custom validation
        if parameters.get("radius") and parameters.get("sigma"):
            if parameters["radius"] < parameters["sigma"]:
                raise ValueError("Radius must be >= sigma")
    
    def apply(self, image_path, output_path, parameters):
        """Apply sharpen mutation"""
        self.validate_parameters(parameters)
        
        radius = parameters.get("radius", self.parameters["radius"].default)
        sigma = parameters.get("sigma", self.parameters["sigma"].default)
        
        # ImageMagick command
        cmd = [
            "magick",
            str(image_path),
            "-sharpen",
            f"{radius}x{sigma}",
            str(output_path)
        ]
        
        # Execute with timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"ImageMagick error: {result.stderr}")
        
        return {
            "success": True,
            "output_path": str(output_path),
            "parameters_used": {
                "radius": radius,
                "sigma": sigma
            }
        }
```

### Step 2: Discrete Mutation Example

```python
# backend/mutations/discrete.py

from mutations.base import MutationBase, MutationParameter

class DesaturateMutation(MutationBase):
    """Desaturate (grayscale) with optional tinting"""
    
    def __init__(self):
        super().__init__(
            name="desaturate",
            description="Convert to grayscale with optional tint",
            category="discrete",
            parameters={
                "mode": MutationParameter(
                    type="choice",
                    choices=["true_gray", "sepia", "blue_tone", "pure_gray"],
                    default="true_gray",
                    description="Desaturation mode"
                )
            }
        )
    
    def apply(self, image_path, output_path, parameters):
        """Apply desaturation"""
        self.validate_parameters(parameters)
        
        mode = parameters.get("mode", "true_gray")
        
        # Map modes to ImageMagick commands
        mode_map = {
            "true_gray": ["-type", "Grayscale"],
            "sepia": ["-sepia-tone", "80%"],
            "blue_tone": ["-modulate", "100,0", "-fill", "blue", "-colorize", "30%"],
            "pure_gray": ["-colorspace", "Gray"]
        }
        
        cmd = ["magick", str(image_path)] + mode_map[mode] + [str(output_path)]
        subprocess.run(cmd, capture_output=True, timeout=30, check=True)
        
        return {"success": True}
```

### Step 3: Register the Mutation

In `backend/mutations/registry.py`:

```python
from mutations.continuous import BlurMutation, BrightnessMutation, SharpenMutation
from mutations.discrete import ColorReduceMutation, DesaturateMutation

class MutationRegistry:
    def __init__(self):
        self.registry = {}
        self.continuous_mutations = {}
        self.discrete_mutations = {}
        
        # Register mutations
        self._register(SharpenMutation())  # NEW
        self._register(DesaturateMutation())  # NEW
        # ... other mutations
    
    def _register(self, mutation):
        """Register a mutation"""
        self.registry[mutation.name] = mutation
        
        if mutation.category == "continuous":
            self.continuous_mutations[mutation.name] = mutation
        elif mutation.category == "discrete":
            self.discrete_mutations[mutation.name] = mutation
```

### Step 4: Test the Mutation

```python
# backend/tests/test_mutations.py

import pytest
from mutations.continuous import SharpenMutation
from PIL import Image
import tempfile

def test_sharpen_mutation():
    """Test sharpen mutation"""
    # Create test image
    img = Image.new('RGB', (100, 100), color='red')
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_in:
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_out:
            img.save(tmp_in.name)
            
            # Create and apply mutation
            mutation = SharpenMutation()
            result = mutation.apply(
                tmp_in.name,
                tmp_out.name,
                {"radius": 2.0, "sigma": 1.0}
            )
            
            # Verify
            assert result["success"]
            assert Path(tmp_out.name).exists()
            assert Path(tmp_out.name).stat().st_size > 0

def test_sharpen_validation():
    """Test parameter validation"""
    mutation = SharpenMutation()
    
    # Invalid: radius < sigma
    with pytest.raises(ValueError):
        mutation.validate_parameters({"radius": 0.5, "sigma": 1.0})
```

### Step 5: Update Frontend (Optional)

The frontend will automatically pick up new mutations via the `/api/mutations` endpoint. To add UI-specific features:

```javascript
// frontend/src/components/MutationSelector.jsx

const MUTATION_ICONS = {
    'blur': '🔳',
    'sharpen': '✨',  // NEW
    'desaturate': '⚫', // NEW
    'brightness': '☀️',
    // ...
};

const MUTATION_DESCRIPTIONS = {
    'sharpen': 'Make images clearer and more defined',
    'desaturate': 'Convert to grayscale with optional tinting',
    // ...
};
```

---

## Extending the Backend

### Adding New API Endpoints

```python
# backend/api/routes.py

from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/custom-endpoint', methods=['POST'])
def custom_endpoint():
    """Custom endpoint example"""
    data = request.get_json()
    
    # Validation
    if 'required_field' not in data:
        return {'error': 'Missing required field'}, 400
    
    # Processing
    result = process_something(data)
    
    # Response
    return {'success': True, 'result': result}, 200
```

### Adding Database Models

```python
# backend/models/mutation_history.py

from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON

class MutationHistory:
    """Track mutation history for analytics"""
    
    def __init__(self):
        self.id = None
        self.job_id = None
        self.mutation_name = None
        self.parameters = {}
        self.processing_time_ms = None
        self.image_count = None
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'mutation': self.mutation_name,
            'parameters': self.parameters,
            'processing_time_ms': self.processing_time_ms,
            'created_at': self.created_at.isoformat()
        }
```

### Adding Background Tasks

```python
# backend/tasks.py - Celery tasks

from celery import shared_task
import subprocess

@shared_task
def process_mutation_async(job_id, mutation_name, parameters, image_paths):
    """Process mutation asynchronously"""
    try:
        # Get mutation
        mutation = mutation_registry.get(mutation_name)
        
        # Apply to each image
        results = []
        for image_path in image_paths:
            result = mutation.apply(image_path, output_path, parameters)
            results.append(result)
        
        # Update job status
        update_job_status(job_id, 'completed', results)
        
        return {'status': 'completed', 'results': results}
    
    except Exception as e:
        update_job_status(job_id, 'failed', {'error': str(e)})
        raise
```

---

## Extending the Frontend

### Adding New React Components

```javascript
// frontend/src/components/AdvancedMutationPanel.jsx

import React, { useState } from 'react';

function AdvancedMutationPanel({ mutation, onApply }) {
    const [preset, setPreset] = useState('balanced');
    const [customParams, setCustomParams] = useState({});
    
    const presets = {
        balanced: { radius: 1.5, sigma: 1.0 },
        light: { radius: 0.5, sigma: 0.5 },
        heavy: { radius: 5.0, sigma: 3.0 }
    };
    
    const handlePresetChange = (presetName) => {
        setPreset(presetName);
        setCustomParams(presets[presetName]);
    };
    
    return (
        <div className="advanced-mutation-panel">
            <div className="preset-buttons">
                {Object.keys(presets).map(name => (
                    <button
                        key={name}
                        onClick={() => handlePresetChange(name)}
                        className={preset === name ? 'active' : ''}
                    >
                        {name.charAt(0).toUpperCase() + name.slice(1)}
                    </button>
                ))}
            </div>
            
            <div className="custom-controls">
                {/* Custom parameter controls */}
            </div>
            
            <button onClick={() => onApply(customParams)}>
                Apply Advanced Mutation
            </button>
        </div>
    );
}

export default AdvancedMutationPanel;
```

### Adding State Management

```javascript
// frontend/src/hooks/useAdvancedMutations.js

import { useState, useCallback } from 'react';

export function useAdvancedMutations() {
    const [mutationHistory, setMutationHistory] = useState([]);
    const [savedPresets, setSavedPresets] = useState([]);
    
    const saveMutationPreset = useCallback((name, mutation, parameters) => {
        setSavedPresets([
            ...savedPresets,
            { name, mutation, parameters, createdAt: new Date() }
        ]);
    }, [savedPresets]);
    
    const applyPreset = useCallback((preset) => {
        return {
            mutation: preset.mutation,
            parameters: preset.parameters
        };
    }, []);
    
    return {
        mutationHistory,
        savedPresets,
        saveMutationPreset,
        applyPreset
    };
}
```

---

## Testing

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test

# Coverage report
pytest tests/ --cov=mutations --cov-report=html
```

### Writing Tests

```python
# backend/tests/test_api.py

import pytest
from app import create_app

@pytest.fixture
def client():
    """Test client"""
    app = create_app('testing')
    return app.test_client()

def test_mutations_endpoint(client):
    """Test mutations listing endpoint"""
    response = client.get('/api/mutations')
    assert response.status_code == 200
    data = response.get_json()
    assert 'continuous' in data
    assert 'discrete' in data

def test_upload_endpoint(client, tmp_path):
    """Test file upload"""
    # Create test image
    test_image = tmp_path / "test.jpg"
    # ... create image ...
    
    response = client.post('/api/upload', data={
        'files': (test_image.open('rb'), 'test.jpg')
    })
    assert response.status_code == 201
    assert 'job_id' in response.get_json()
```

---

## Performance Optimization

### Image Optimization

```python
# backend/core/image_handler.py

def optimize_image_for_processing(image_path, max_dimension=2048):
    """Resize large images to improve processing speed"""
    from PIL import Image
    
    img = Image.open(image_path)
    
    # Check if resize needed
    if max(img.size) > max_dimension:
        ratio = max_dimension / max(img.size)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        img.save(image_path, optimize=True, quality=95)
```

### Batch Processing

```python
# backend/core/mutation_executor.py - Parallel processing

from concurrent.futures import ThreadPoolExecutor, as_completed

def apply_mutation_batch(mutation, image_paths, parameters, max_workers=4):
    """Apply mutation to multiple images in parallel"""
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(apply_single, image_path, mutation, parameters): image_path
            for image_path in image_paths
        }
        
        for future in as_completed(futures):
            image_path = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({'error': str(e), 'image': image_path})
    
    return results
```

### Caching

```javascript
// frontend/src/services/api.js - Response caching

const mutationCache = new Map();

async function fetchMutations() {
    if (mutationCache.has('mutations')) {
        return mutationCache.get('mutations');
    }
    
    const response = await axios.get('/api/mutations');
    mutationCache.set('mutations', response.data);
    
    // Invalidate cache after 5 minutes
    setTimeout(() => mutationCache.delete('mutations'), 5 * 60 * 1000);
    
    return response.data;
}
```

---

## Debugging

### Enable Debug Logging

```bash
# Backend
export DEBUG=True
export LOG_LEVEL=DEBUG
python app.py

# Frontend
export REACT_APP_DEBUG=true
npm start
```

### Debug ImageMagick Commands

```python
# backend/core/mutation_executor.py

def apply_with_debug(image_path, output_path, cmd):
    """Execute command with debug output"""
    import subprocess
    
    print(f"[DEBUG] Command: {' '.join(cmd)}")
    print(f"[DEBUG] Input: {image_path}")
    print(f"[DEBUG] Output: {output_path}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print(f"[DEBUG] stdout: {result.stdout}")
    if result.stderr:
        print(f"[DEBUG] stderr: {result.stderr}")
    
    return result
```

### Frontend Debugging

```javascript
// Add to frontend/.env
REACT_APP_DEBUG=true
REACT_APP_API_DEBUG=true

// In components
const apiDebug = (message, data) => {
    if (process.env.REACT_APP_API_DEBUG) {
        console.log(`[API] ${message}`, data);
    }
};
```

---

## Deployment

### Docker Deployment

```dockerfile
# docker/Dockerfile.backend

FROM python:3.9-slim

WORKDIR /app

# Install ImageMagick
RUN apt-get update && \
    apt-get install -y imagemagick libmagickwand-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY backend .

# Run
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Environment Configuration

```bash
# .env.production

FLASK_ENV=production
DEBUG=False
DATABASE_URL=postgresql://user:pass@db:5432/mutations
REDIS_URL=redis://redis:6379/0
LOG_LEVEL=INFO

# Frontend
REACT_APP_API_URL=https://api.example.com
```

---

## Contributing Guidelines

### Code Style

- **Python**: PEP 8 (use Black formatter)
- **JavaScript**: Prettier configuration in `frontend/.prettierrc`
- **Git**: Conventional commits (`feat:`, `fix:`, `docs:`, etc.)

### Pull Request Process

1. Fork the repository
2. Create feature branch: `git checkout -b feat/new-mutation`
3. Make changes and commit: `git commit -m "feat: add sharpen mutation"`
4. Push: `git push origin feat/new-mutation`
5. Open PR with description

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

Closes #<issue-number>
```

Example:
```
feat(mutations): add sharpen mutation

- Implement SharpenMutation class
- Add radius and sigma parameters
- Add tests for validation

Closes #42
```

### Documentation Standards

- All functions must have docstrings
- All complex logic must have comments
- New features must include examples
- Update README.md if adding user-facing features

### Review Checklist

- [ ] Code follows style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.logs/print statements
- [ ] No hardcoded values
- [ ] Performance impact assessed

---

## Resources

- **ImageMagick Docs**: https://imagemagick.org/script/command-line-processing.php
- **Flask Docs**: https://flask.palletsprojects.com/
- **React Docs**: https://react.dev/
- **pytest Docs**: https://docs.pytest.org/

---

## Getting Help

- **GitHub Issues**: Report bugs and discuss features
- **Documentation**: See `/docs` folder for detailed guides
- **Research Paper**: See project root for linked paper

