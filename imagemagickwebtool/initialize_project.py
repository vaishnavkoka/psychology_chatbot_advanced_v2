#!/usr/bin/env python3
"""
Image Mutation Tool - Project Initializer
Automates setup of backend and frontend environments
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class ProjectInitializer:
    """Handles project setup and initialization"""
    
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.logs = []
    
    def log(self, message, level="INFO"):
        """Log messages with level indicators"""
        prefix = f"[{level}]"
        print(f"{prefix} {message}")
        self.logs.append(f"{prefix} {message}")
    
    def run_command(self, cmd, cwd=None, description=""):
        """Run shell command and capture output"""
        try:
            self.log(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
            result = subprocess.run(
                cmd,
                cwd=cwd or os.getcwd(),
                shell=isinstance(cmd, str),
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode != 0:
                self.log(f"Command failed: {result.stderr}", "ERROR")
                return False
            if result.stdout:
                self.log(f"Output: {result.stdout[:200]}", "DEBUG")
            return True
        except subprocess.TimeoutExpired:
            self.log("Command timed out", "ERROR")
            return False
        except Exception as e:
            self.log(f"Command error: {str(e)}", "ERROR")
            return False
    
    def check_prerequisites(self):
        """Check if all required tools are installed"""
        self.log("Checking prerequisites...")
        
        checks = {
            "Python 3.8+": ["python3", "--version"],
            "Node.js 14+": ["node", "--version"],
            "npm": ["npm", "--version"],
            "Git": ["git", "--version"],
        }
        
        missing = []
        for tool, cmd in checks.items():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.log(f"✓ {tool}: {result.stdout.strip()}", "OK")
                else:
                    missing.append(tool)
            except Exception:
                missing.append(tool)
        
        # ImageMagick optional but recommended
        try:
            subprocess.run(["magick", "--version"], capture_output=True, text=True, timeout=5)
            self.log("✓ ImageMagick: installed", "OK")
        except:
            self.log("⚠ ImageMagick not installed (optional, but recommended)", "WARN")
        
        if missing:
            self.log(f"Missing prerequisites: {', '.join(missing)}", "ERROR")
            return False
        
        self.log("All prerequisites satisfied!", "OK")
        return True
    
    def create_directory_structure(self):
        """Create required directories"""
        self.log("Creating directory structure...")
        
        dirs = [
            self.backend_dir,
            self.backend_dir / "mutations",
            self.backend_dir / "core",
            self.backend_dir / "api",
            self.backend_dir / "storage",
            self.backend_dir / "tests",
            self.frontend_dir / "src" / "components",
            self.frontend_dir / "src" / "pages",
            self.frontend_dir / "src" / "services",
            self.frontend_dir / "src" / "hooks",
            self.project_root / "uploads",
            self.project_root / "outputs",
            self.project_root / "logs",
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            self.log(f"✓ Created: {dir_path}")
        
        self.log("Directory structure created!", "OK")
        return True
    
    def setup_backend(self):
        """Setup Python backend environment"""
        self.log("Setting up backend environment...")
        
        # Create virtual environment
        venv_path = self.backend_dir / "venv"
        if not venv_path.exists():
            self.log("Creating Python virtual environment...")
            if not self.run_command([sys.executable, "-m", "venv", str(venv_path)]):
                return False
        
        # Determine pip command based on OS
        if sys.platform == "win32":
            pip_cmd = str(venv_path / "Scripts" / "pip.exe")
            python_cmd = str(venv_path / "Scripts" / "python.exe")
        else:
            pip_cmd = str(venv_path / "bin" / "pip")
            python_cmd = str(venv_path / "bin" / "python")
        
        # Create requirements.txt if not exists
        requirements_file = self.backend_dir / "requirements.txt"
        if not requirements_file.exists():
            requirements = """Flask==2.3.0
Flask-CORS==4.0.0
Pillow==9.5.0
Wand==0.6.11
opencv-python==4.7.0.72
python-dotenv==1.0.0
requests==2.28.2
Celery==5.3.0
redis==4.5.1
SQLAlchemy==2.0.0
pytest==7.3.0"""
            requirements_file.write_text(requirements)
            self.log(f"✓ Created {requirements_file}")
        
        # Install requirements
        self.log("Installing Python dependencies (this may take a few minutes)...")
        if not self.run_command([pip_cmd, "install", "-r", str(requirements_file)]):
            return False
        
        # Create .env file
        env_file = self.backend_dir / ".env"
        if not env_file.exists():
            env_content = """FLASK_ENV=development
DEBUG=True
UPLOAD_FOLDER=../uploads
OUTPUT_FOLDER=../outputs
MAX_FILE_SIZE=52428800
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///./mutations.db"""
            env_file.write_text(env_content)
            self.log(f"✓ Created {env_file}")
        
        # Verify installation
        self.log("Verifying backend installation...")
        self.run_command(
            [python_cmd, "-c", 
             "from flask import Flask; from PIL import Image; print('Backend OK')"],
            cwd=str(self.backend_dir)
        )
        
        self.log("Backend setup complete!", "OK")
        return True
    
    def setup_frontend(self):
        """Setup Node.js frontend environment"""
        self.log("Setting up frontend environment...")
        
        # Create package.json if not exists
        package_json = self.frontend_dir / "package.json"
        if not package_json.exists():
            package_content = {
                "name": "image-mutation-tool",
                "version": "1.0.0",
                "description": "Web tool for applying image mutations",
                "dependencies": {
                    "react": "^18.2.0",
                    "react-dom": "^18.2.0",
                    "react-router-dom": "^6.0.0",
                    "axios": "^1.3.0",
                    "react-dropzone": "^14.2.0",
                    "react-slider": "^1.8.0"
                },
                "scripts": {
                    "start": "react-scripts start",
                    "build": "react-scripts build",
                    "test": "react-scripts test",
                    "eject": "react-scripts eject"
                },
                "eslintConfig": {
                    "extends": ["react-app"]
                },
                "browserslist": {
                    "production": [">0.2%", "not dead", "not op_mini all"],
                    "development": ["last 1 chrome version", "last 1 firefox version"]
                }
            }
            package_json.write_text(json.dumps(package_content, indent=2))
            self.log(f"✓ Created {package_json}")
        
        # Install dependencies
        self.log("Installing Node.js dependencies (this may take a few minutes)...")
        if not self.run_command(["npm", "install"], cwd=str(self.frontend_dir)):
            self.log("Warning: npm install encountered issues, but continuing...", "WARN")
        
        # Create .env file
        env_file = self.frontend_dir / ".env"
        if not env_file.exists():
            env_content = "REACT_APP_API_URL=http://localhost:5000/api"
            env_file.write_text(env_content)
            self.log(f"✓ Created {env_file}")
        
        self.log("Frontend setup complete!", "OK")
        return True
    
    def create_startup_scripts(self):
        """Create convenient startup scripts"""
        self.log("Creating startup scripts...")
        
        # Linux/macOS startup script
        if sys.platform != "win32":
            startup_script = self.project_root / "start.sh"
            content = """#!/bin/bash
set -e

echo "Starting Image Mutation Tool..."
echo ""

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!

sleep 3

# Start frontend
echo "Starting frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "✓ Backend running on http://localhost:5000"
echo "✓ Frontend running on http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

wait
"""
            startup_script.write_text(content)
            startup_script.chmod(0o755)
            self.log(f"✓ Created {startup_script}")
        
        # Windows startup script
        if sys.platform == "win32" or True:  # Create for all platforms
            startup_script = self.project_root / "start.cmd"
            content = """@echo off
echo Starting Image Mutation Tool...
echo.

REM Start backend in new window
echo Starting backend server...
cd backend
call venv\\Scripts\\activate
start "Backend" python app.py

timeout /t 3

REM Start frontend in new window
echo Starting frontend...
cd ..\\frontend
start "Frontend" npm start

echo.
echo Backend running on http://localhost:5000
echo Frontend running on http://localhost:3000
echo.
pause
"""
            startup_script.write_text(content)
            self.log(f"✓ Created {startup_script}")
    
    def run_initialization(self):
        """Execute full initialization"""
        self.log("=" * 60)
        self.log("Image Mutation Tool - Project Initializer", "INFO")
        self.log("=" * 60)
        self.log("")
        
        steps = [
            ("Checking Prerequisites", self.check_prerequisites),
            ("Creating Directory Structure", self.create_directory_structure),
            ("Setting Up Backend", self.setup_backend),
            ("Setting Up Frontend", self.setup_frontend),
            ("Creating Startup Scripts", self.create_startup_scripts),
        ]
        
        for step_name, step_func in steps:
            self.log("")
            self.log(f"Step {steps.index((step_name, step_func)) + 1}/{len(steps)}: {step_name}")
            try:
                if not step_func():
                    self.log(f"Failed at step: {step_name}", "ERROR")
                    return False
            except Exception as e:
                self.log(f"Exception in {step_name}: {str(e)}", "ERROR")
                return False
        
        self.log("")
        self.log("=" * 60)
        self.log("✓ Project initialization complete!", "OK")
        self.log("=" * 60)
        self.log("")
        self.log("Next steps:")
        self.log("1. Review QUICK_START.md for detailed instructions")
        self.log("2. Run: ./start.sh (Linux/macOS) or start.cmd (Windows)")
        self.log("3. Open http://localhost:3000 in your browser")
        self.log("")
        
        return True


def main():
    """Main entry point"""
    initializer = ProjectInitializer()
    success = initializer.run_initialization()
    
    # Save logs
    log_file = Path("initialization.log")
    log_file.write_text("\n".join(initializer.logs))
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
