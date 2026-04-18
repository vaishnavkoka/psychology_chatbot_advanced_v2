#!/bin/bash

# Docker Entrypoint Script for Psychology Chatbot Backend
# Provides startup logic, health checks, and graceful shutdown

set -e

# Console colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running in Docker
if [ -f /.dockerenv ]; then
    log_info "Running inside Docker container"
else
    log_warn "Not running inside Docker (or custom environment)"
fi

# Verify required directories exist
log_info "Verifying directory structure..."
required_dirs=("data" "agents" "config" "safety" "logs")
for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        log_warn "Creating missing directory: $dir"
        mkdir -p "$dir"
    fi
done
log_success "All directories verified/created"

# Check API key is configured
if [ -z "$GROQ_API_KEY" ]; then
    log_warn "GROQ_API_KEY is not set. Using default/empty key."
else
    log_success "GROQ_API_KEY is configured"
fi

# Display startup information
log_info "======================================"
log_info "Psychology Chatbot Backend Starting"
log_info "======================================"
log_info "Python version: $(python --version 2>&1)"
log_info "Working directory: $(pwd)"
log_info "User: $(id -un)"
log_info "Environment: ${ENV:-development}"
log_info "======================================\n"

# Handle different startup modes
case "${1:-start}" in
    start)
        log_info "Starting FastAPI backend..."
        exec uvicorn backend:app \
            --host 0.0.0.0 \
            --port 8000 \
            --workers 2 \
            --loop uvloop \
            --timeout-keep-alive 30
        ;;
    
    dev)
        log_info "Starting FastAPI backend in development mode (auto-reload)..."
        exec uvicorn backend:app \
            --host 0.0.0.0 \
            --port 8000 \
            --reload \
            --timeout-keep-alive 30
        ;;
    
    shell)
        log_info "Starting interactive shell..."
        exec /bin/bash
        ;;
    
    test)
        log_info "Running tests..."
        exec python -m pytest tests/ -v --cov --tb=short
        ;;
    
    *)
        log_error "Unknown command: $1"
        log_info "Available commands: start, dev, shell, test"
        exit 1
        ;;
esac
