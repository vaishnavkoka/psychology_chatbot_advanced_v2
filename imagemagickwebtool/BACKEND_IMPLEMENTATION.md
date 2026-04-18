# Image Mutation Tool - Backend Implementation Guide

## 🏗 Architecture Overview

```
User Interface (React)
        ↓
   API Layer (Flask/FastAPI)
        ↓
   Mutation Engine
   ├─ PIL (Pillow)
   ├─ ImageMagick (via Wand)
   └─ OpenCV (optional)
        ↓
   File Storage (Local/S3)
        ↓
Metadata & Logging (JSON/Database)
```

---

## 📦 Project Structure

```
image-mutation-tool/
├── backend/
│   ├── app.py                      # Flask application entry
│   ├── config.py                   # Configuration settings
│   ├── mutations/
│   │   ├── __init__.py
│   │   ├── base.py                 # Base mutation class
│   │   ├── continuous.py           # Blur, brightness, etc.
│   │   ├── discrete.py             # Color reduction, etc.
│   │   └── registry.py             # Mutation catalog
│   ├── core/
│   │   ├── __init__.py
│   │   ├── image_handler.py        # Image I/O operations
│   │   ├── mutation_executor.py    # Execute mutations
│   │   └── batch_processor.py      # Batch operations
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── local_storage.py        # File system
│   │   ├── cloud_storage.py        # AWS S3 (optional)
│   │   └── manifest.py             # Metadata handling
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py               # API endpoints
│   │   ├── validation.py           # Input validation
│   │   └── responses.py            # Response formatting
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py               # Logging setup
│   │   ├── validators.py           # Data validation
│   │   └── helpers.py              # Utility functions
│   ├── assets/
│   │   └── mutations.json           # Mutation definitions
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_mutations.py
│   │   ├── test_api.py
│   │   └── test_storage.py
│   ├── requirements.txt             # Python dependencies
│   ├── wsgi.py                      # WSGI entry point
│   └── .env.example                 # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── index.js
│   ├── public/
│   ├── package.json
│   └── .env.example
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── scripts/
│   ├── setup.sh                     # Installation script
│   └── deploy.sh                    # Deployment script
├── docs/
│   ├── README.md
│   ├── API.md
│   ├── INSTALLATION.md
│   └── MUTATION_REFERENCE.md
└── .gitignore
```

---

## 🔧 Core Components

### 1. **Mutation Base Class** (`mutations/base.py`)

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class MutationParameter:
    """Defines a mutation parameter"""
    name: str
    type: str  # 'float', 'int', 'choice', 'bool'
    min_value: float = None
    max_value: float = None
    default_value: Any = None
    choices: list = None
    description: str = ""

class MutationBase(ABC):
    """Base class for all mutations"""
    
    def __init__(self):
        self.name = ""
        self.description = ""
        self.category = "continuous"  # or "discrete"
        self.parameters = []
    
    @abstractmethod
    def validate_parameters(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate input parameters"""
        pass
    
    @abstractmethod
    def apply(self, image_path: str, output_path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply mutation to image
        
        Args:
            image_path: Path to input image
            output_path: Path to output image
            params: Mutation parameters
            
        Returns:
            Dict with execution metadata
        """
        pass
    
    def to_dict(self) -> Dict:
        """Serialize mutation definition"""
        return {
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "parameters": [
                {
                    "name": p.name,
                    "type": p.type,
                    "min": p.min_value,
                    "max": p.max_value,
                    "default": p.default_value,
                    "choices": p.choices,
                    "description": p.description
                }
                for p in self.parameters
            ]
        }
```

### 2. **Continuous Mutations** (`mutations/continuous.py`)

```python
from .base import MutationBase, MutationParameter
import subprocess
import time

class BlurMutation(MutationBase):
    """Gaussian blur mutation"""
    
    def __init__(self):
        super().__init__()
        self.name = "blur"
        self.category = "continuous"
        self.description = "Apply Gaussian blur with configurable sigma"
        self.parameters = [
            MutationParameter(
                name="sigma",
                type="float",
                min_value=0.1,
                max_value=50,
                default_value=5,
                description="Standard deviation of the blur (higher = more blur)"
            )
        ]
    
    def validate_parameters(self, params: dict) -> tuple:
        """Validate blur parameters"""
        if "sigma" not in params:
            return False, "Missing 'sigma' parameter"
        
        sigma = params["sigma"]
        if not isinstance(sigma, (int, float)):
            return False, "Sigma must be numeric"
        if not (0.1 <= sigma <= 50):
            return False, f"Sigma must be between 0.1 and 50, got {sigma}"
        
        return True, ""
    
    def apply(self, image_path: str, output_path: str, params: dict) -> dict:
        """Apply blur using ImageMagick"""
        sigma = params["sigma"]
        start_time = time.time()
        
        cmd = [
            "magick",
            image_path,
            "-blur", f"0x{sigma}",
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                raise Exception(f"ImageMagick error: {result.stderr}")
            
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "execution_time_ms": int(execution_time * 1000),
                "parameters_applied": params
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Blur operation timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class BrightnessMutation(MutationBase):
    """Brightness adjustment mutation"""
    
    def __init__(self):
        super().__init__()
        self.name = "brightness"
        self.category = "continuous"
        self.description = "Adjust image brightness"
        self.parameters = [
            MutationParameter(
                name="percentage",
                type="float",
                min_value=-100,
                max_value=100,
                default_value=0,
                description="Brightness adjustment (-100 to 100)"
            )
        ]
    
    def validate_parameters(self, params: dict) -> tuple:
        """Validate brightness parameters"""
        if "percentage" not in params:
            return False, "Missing 'percentage' parameter"
        
        pct = params["percentage"]
        if not isinstance(pct, (int, float)):
            return False, "Percentage must be numeric"
        if not (-100 <= pct <= 100):
            return False, "Percentage must be -100 to 100"
        
        return True, ""
    
    def apply(self, image_path: str, output_path: str, params: dict) -> dict:
        """Apply brightness using ImageMagick"""
        percentage = params["percentage"]
        start_time = time.time()
        
        # Convert percentage to modulate value (100 = no change)
        modulate_value = 100 + percentage
        
        cmd = [
            "magick",
            image_path,
            "-modulate", f"{modulate_value}",
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                raise Exception(f"ImageMagick error: {result.stderr}")
            
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "execution_time_ms": int(execution_time * 1000),
                "parameters_applied": params
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class RotationMutation(MutationBase):
    """Image rotation mutation"""
    
    def __init__(self):
        super().__init__()
        self.name = "rotation"
        self.category = "continuous"
        self.description = "Rotate image by specified degrees"
        self.parameters = [
            MutationParameter(
                name="degrees",
                type="float",
                min_value=0,
                max_value=360,
                default_value=45,
                description="Rotation angle in degrees (0-360)"
            )
        ]
    
    def validate_parameters(self, params: dict) -> tuple:
        if "degrees" not in params:
            return False, "Missing 'degrees' parameter"
        
        deg = params["degrees"]
        if not isinstance(deg, (int, float)):
            return False, "Degrees must be numeric"
        if not (0 <= deg <= 360):
            return False, "Degrees must be 0-360"
        
        return True, ""
    
    def apply(self, image_path: str, output_path: str, params: dict) -> dict:
        """Apply rotation using ImageMagick"""
        degrees = params["degrees"]
        start_time = time.time()
        
        cmd = [
            "magick",
            image_path,
            "-rotate", str(degrees),
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                raise Exception(f"ImageMagick error: {result.stderr}")
            
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "execution_time_ms": int(execution_time * 1000),
                "parameters_applied": params
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
```

### 3. **Discrete Mutations** (`mutations/discrete.py`)

```python
from .base import MutationBase, MutationParameter
import subprocess
import time

class ColorReduceMutation(MutationBase):
    """Color palette reduction mutation"""
    
    def __init__(self):
        super().__init__()
        self.name = "color_reduce"
        self.category = "discrete"
        self.description = "Reduce image to specified number of colors"
        self.parameters = [
            MutationParameter(
                name="num_colors",
                type="choice",
                choices=[2, 4, 8, 16, 32, 64, 128, 256],
                default_value=256,
                description="Number of colors in output palette"
            )
        ]
    
    def validate_parameters(self, params: dict) -> tuple:
        if "num_colors" not in params:
            return False, "Missing 'num_colors' parameter"
        
        num_colors = params["num_colors"]
        if num_colors not in [2, 4, 8, 16, 32, 64, 128, 256]:
            return False, f"num_colors must be one of: 2,4,8,16,32,64,128,256"
        
        return True, ""
    
    def apply(self, image_path: str, output_path: str, params: dict) -> dict:
        """Apply color reduction using ImageMagick"""
        num_colors = params["num_colors"]
        start_time = time.time()
        
        cmd = [
            "magick",
            image_path,
            "-colors", str(num_colors),
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                raise Exception(f"ImageMagick error: {result.stderr}")
            
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "execution_time_ms": int(execution_time * 1000),
                "parameters_applied": params
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class ColorizeDiscreteM(MutationBase):
    """Colorize mutation with predefined color tones"""
    
    def __init__(self):
        super().__init__()
        self.name = "colorize"
        self.category = "discrete"
        self.description = "Apply color tint to image"
        self.parameters = [
            MutationParameter(
                name="color_tone",
                type="choice",
                choices=["red", "green", "blue", "yellow", "cyan", "magenta", "grayscale"],
                default_value="red",
                description="Color tone to apply"
            )
        ]
    
    def validate_parameters(self, params: dict) -> tuple:
        if "color_tone" not in params:
            return False, "Missing 'color_tone' parameter"
        
        tone = params["color_tone"]
        valid_tones = ["red", "green", "blue", "yellow", "cyan", "magenta", "grayscale"]
        if tone not in valid_tones:
            return False, f"color_tone must be one of: {','.join(valid_tones)}"
        
        return True, ""
    
    def apply(self, image_path: str, output_path: str, params: dict) -> dict:
        """Apply colorize using ImageMagick"""
        color_tone = params["color_tone"]
        start_time = time.time()
        
        # Mapping color tones to ImageMagick colorize values
        tone_map = {
            "red": "100,0,0",
            "green": "0,100,0",
            "blue": "0,0,100",
            "yellow": "100,100,0",
            "cyan": "0,100,100",
            "magenta": "100,0,100",
            "grayscale": "-saturate 100"
        }
        
        if color_tone == "grayscale":
            cmd = [
                "magick",
                image_path,
                "-colorspace", "Gray",
                output_path
            ]
        else:
            colorize_val = tone_map[color_tone]
            cmd = [
                "magick",
                image_path,
                "-colorize", colorize_val,
                output_path
            ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                raise Exception(f"ImageMagick error: {result.stderr}")
            
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "execution_time_ms": int(execution_time * 1000),
                "parameters_applied": params
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
```

### 4. **Mutation Registry** (`mutations/registry.py`)

```python
from .continuous import (
    BlurMutation,
    BrightnessMutation,
    RotationMutation
)
from .discrete import (
    ColorReduceMutation,
    ColorizeDiscreteM
)

class MutationRegistry:
    """Central registry of all available mutations"""
    
    def __init__(self):
        self.mutations = {}
        self._register_all()
    
    def _register_all(self):
        """Register all available mutations"""
        # Continuous mutations
        blur = BlurMutation()
        self.register(blur.name, blur)
        
        brightness = BrightnessMutation()
        self.register(brightness.name, brightness)
        
        rotation = RotationMutation()
        self.register(rotation.name, rotation)
        
        # Discrete mutations
        color_reduce = ColorReduceMutation()
        self.register(color_reduce.name, color_reduce)
        
        colorize = ColorizeDiscreteM()
        self.register(colorize.name, colorize)
    
    def register(self, name: str, mutation_obj):
        """Register a mutation"""
        self.mutations[name] = mutation_obj
    
    def get(self, name: str):
        """Get mutation by name"""
        return self.mutations.get(name)
    
    def list_all(self):
        """List all available mutations"""
        return {name: mutation.to_dict() for name, mutation in self.mutations.items()}
    
    def list_continuous(self):
        """List continuous mutations"""
        return {
            name: mutation.to_dict()
            for name, mutation in self.mutations.items()
            if mutation.category == "continuous"
        }
    
    def list_discrete(self):
        """List discrete mutations"""
        return {
            name: mutation.to_dict()
            for name, mutation in self.mutations.items()
            if mutation.category == "discrete"
        }

# Global registry instance
mutation_registry = MutationRegistry()
```

### 5. **Flask Application** (`app.py`)

```python
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import uuid
import time

from mutations.registry import mutation_registry
from core.mutation_executor import MutationExecutor
from storage.manifest import ManifestGenerator

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER', 'outputs')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'tiff', 'bmp', 'webp'}
MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 52428800))  # 50MB default

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure folders exist
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/mutations', methods=['GET'])
def get_mutations():
    """Get list of all available mutations"""
    return jsonify({
        "all": mutation_registry.list_all(),
        "continuous": mutation_registry.list_continuous(),
        "discrete": mutation_registry.list_discrete()
    })


@app.route('/api/upload', methods=['POST'])
def upload_images():
    """Upload images for mutation"""
    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400
    
    files = request.files.getlist('files')
    job_id = str(uuid.uuid4())
    job_folder = Path(UPLOAD_FOLDER) / job_id
    job_folder.mkdir(parents=True, exist_ok=True)
    
    uploaded_info = []
    for file in files:
        if file.filename == '':
            continue
        
        if not allowed_file(file.filename):
            continue
        
        filename = secure_filename(file.filename)
        filepath = job_folder / filename
        file.save(str(filepath))
        
        uploaded_info.append({
            "filename": filename,
            "path": str(filepath),
            "size_bytes": os.path.getsize(filepath)
        })
    
    return jsonify({
        "job_id": job_id,
        "uploaded_files": len(uploaded_info),
        "files": uploaded_info
    })


@app.route('/api/mutate', methods=['POST'])
def apply_mutation():
    """Apply mutation to images"""
    data = request.json
    job_id = data.get('job_id')
    mutation_name = data.get('mutation')
    parameters = data.get('parameters', {})
    image_paths = data.get('image_paths', [])
    
    # Validate mutation exists
    mutation = mutation_registry.get(mutation_name)
    if not mutation:
        return jsonify({"error": f"Mutation '{mutation_name}' not found"}), 400
    
    # Validate parameters
    is_valid, error_msg = mutation.validate_parameters(parameters)
    if not is_valid:
        return jsonify({"error": f"Invalid parameters: {error_msg}"}), 400
    
    # Create output folder for this job
    output_folder = Path(OUTPUT_FOLDER) / job_id
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Apply mutations
    executor = MutationExecutor()
    results = []
    
    for image_path in image_paths:
        # Generate output filename
        base_name = Path(image_path).stem
        ext = Path(image_path).suffix
        output_filename = f"{base_name}_{mutation_name}_{int(time.time())}{ext}"
        output_path = output_folder / output_filename
        
        # Execute mutation
        result = mutation.apply(image_path, str(output_path), parameters)
        
        if result['success']:
            result['output_path'] = str(output_path)
            result['output_filename'] = output_filename
        
        results.append(result)
    
    return jsonify({
        "job_id": job_id,
        "mutation": mutation_name,
        "results": results,
        "output_folder": str(output_folder)
    })


@app.route('/api/download/<job_id>/<filename>', methods=['GET'])
def download_file(job_id, filename):
    """Download mutated image"""
    filepath = Path(OUTPUT_FOLDER) / job_id / secure_filename(filename)
    
    if not filepath.exists():
        return jsonify({"error": "File not found"}), 404
    
    return send_file(str(filepath), as_attachment=True)


@app.route('/api/manifest/<job_id>', methods=['GET'])
def get_manifest(job_id):
    """Get mutation manifest for a job"""
    manifest_path = Path(OUTPUT_FOLDER) / job_id / 'manifest.json'
    
    if not manifest_path.exists():
        return jsonify({"error": "Manifest not found"}), 404
    
    with open(manifest_path) as f:
        import json
        manifest = json.load(f)
    
    return jsonify(manifest)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "image-mutation-tool"})


if __name__ == '__main__':
    app.run(debug=bool(os.environ.get('DEBUG', False)))
```

---

## 📋 Requirements File (`requirements.txt`)

```
Flask==2.3.0
Flask-CORS==4.0.0
Pillow==9.5.0
Wand==0.6.11
opencv-python==4.7.0
python-dotenv==1.0.0
requests==2.31.0
Celery==5.3.0
redis==4.5.1
SQLAlchemy==2.0.0
pytest==7.3.0
python-magic==0.4.27
```

---

## 🚀 Quick Start Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install ImageMagick (system-level)
# On Ubuntu/Debian:
sudo apt-get install imagemagick

# On macOS:
brew install imagemagick

# 3. Run Flask app
python app.py

# 4. Test API
curl http://localhost:5000/api/mutations

# 5. Run tests
pytest tests/
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/mutations` | List all mutations |
| POST | `/api/upload` | Upload images |
| POST | `/api/mutate` | Apply mutation |
| GET | `/api/download/<job_id>/<filename>` | Download result |
| GET | `/api/manifest/<job_id>` | Get mutation metadata |
| GET | `/health` | Health check |

---

## 🧪 Testing

```python
# tests/test_mutations.py
import pytest
from mutations.registry import mutation_registry

def test_blur_mutation():
    """Test blur mutation"""
    blur = mutation_registry.get('blur')
    
    # Valid parameters
    is_valid, _ = blur.validate_parameters({'sigma': 5})
    assert is_valid
    
    # Invalid parameters
    is_valid, _ = blur.validate_parameters({'sigma': 100})
    assert not is_valid

def test_color_reduce_mutation():
    """Test color reduction"""
    color_reduce = mutation_registry.get('color_reduce')
    
    # Valid
    is_valid, _ = color_reduce.validate_parameters({'num_colors': 256})
    assert is_valid
    
    # Invalid
    is_valid, _ = color_reduce.validate_parameters({'num_colors': 100})
    assert not is_valid
```

This backend provides the foundation for the mutation tool. Next phase would implement the React frontend!

