# 🐳 Docker Deployment Guide - Psychology Chatbot

Complete guide to containerize, build, and deploy the Psychology Chatbot using Docker and Docker Compose.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Building Images](#building-images)
4. [Running Containers](#running-containers)
5. [Docker Compose](#docker-compose)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)
8. [Production Deployment](#production-deployment)

---

## Prerequisites

- **Docker**: 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: 1.29+ ([Install Compose](https://docs.docker.com/compose/install/))
- **GROQ API Key**: Required for LLM functionality
- **2GB+ RAM**: Minimum for containers
- **20GB+ Disk Space**: For images and data

Verify installation:
```bash
docker --version
docker-compose --version
```

---

## Quick Start

### Start Everything with Docker Compose
```bash
# Clone/navigate to project directory
cd psychology_chatbot_advanced

# Set your API keys
export GROQ_API_KEY="your-groq-api-key"
export HUGGINGFACE_API_KEY="your-huggingface-token"  # Optional
export SERPER_API_KEY="your-serper-api-key"         # Optional

# Build and start all services
docker-compose up --build

# In another terminal, verify services are running
docker-compose ps
```

**Access the application:**
- 🎨 **Frontend**: http://localhost:8501
- 🔌 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs

---

## Building Images

### Build Backend Image
```bash
# Build the backend image
docker build -t psychology-chatbot:backend .

# Build with specific Python version
docker build --build-arg PYTHON_VERSION=3.11 -t psychology-chatbot:backend .

# Build with buildkit for better caching
DOCKER_BUILDKIT=1 docker build -t psychology-chatbot:backend .
```

### Build Frontend Image
```bash
# Build the frontend image
docker build -f Dockerfile.frontend -t psychology-chatbot:frontend .

# Build with specific base image
docker build -f Dockerfile.frontend --build-arg BASE_IMAGE=python:3.11-slim -t psychology-chatbot:frontend .
```

### View Build Process
```bash
# Enable verbose output
docker build --progress=plain -t psychology-chatbot:backend .
```

---

## Running Containers

### Run Backend Standalone
```bash
# Simple run
docker run -p 8000:8000 \
    -e GROQ_API_KEY="your-key" \
    psychology-chatbot:backend

# With volume mounts for persistence
docker run -p 8000:8000 \
    -e GROQ_API_KEY="your-key" \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/logs:/app/logs \
    psychology-chatbot:backend

# With resource limits
docker run -p 8000:8000 \
    -e GROQ_API_KEY="your-key" \
    --memory="2g" \
    --cpus="1" \
    psychology-chatbot:backend

# Run in background (detached)
docker run -d \
    --name psychology-backend \
    -p 8000:8000 \
    -e GROQ_API_KEY="your-key" \
    psychology-chatbot:backend

# View logs
docker logs psychology-backend
docker logs -f psychology-backend  # Follow logs
```

### Run Frontend Standalone
```bash
# Simple run (requires backend running)
docker run -p 8501:8501 \
    --link psychology-backend:backend \
    psychology-chatbot:frontend

# With custom frontend
docker run -p 8501:8501 \
    psychology-chatbot:frontend \
    streamlit run frontend_modern.py
```

---

## Docker Compose

### Basic Commands

```bash
# Build services (if not already built)
docker-compose build

# Start services in foreground (see logs)
docker-compose up

# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View running services
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild a specific service
docker-compose build backend
docker-compose up -d backend  # Restart with new image
```

### Advanced Commands

```bash
# Pull latest images
docker-compose pull

# Remove containers, networks, and volumes
docker-compose down -v

# Restart specific service
docker-compose restart backend

# Execute command in running container
docker-compose exec backend bash
docker-compose exec backend python -c "import agents.psychology_agents"

# Scale services (e.g., multiple backend instances - requires load balancer)
docker-compose up -d --scale backend=3

# Check resource usage
docker stats psychology-chatbot-backend psychology-chatbot-frontend
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required
GROQ_API_KEY=your-groq-api-key-here

# Optional
HUGGINGFACE_API_KEY=your-hf-token
SERPER_API_KEY=your-serper-key

# Container settings
ENV=production
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1

# Logging
LOG_LEVEL=INFO
STREAMLIT_LOGGER_LEVEL=info
```

### Using Compose Overrides

Create `docker-compose.override.yml` for local development:

```yaml
version: '3.8'

services:
  backend:
    environment:
      - ENV=development
      - LOG_LEVEL=DEBUG
    volumes:
      - ./agents:/app/agents:rw  # Enable live editing
      - ./data:/app/data:rw
  
  frontend:
    environment:
      - STREAMLIT_LOGGER_LEVEL=debug
```

Compose automatically merges these files.

### Resource Limits

Edit `docker-compose.yml` under `deploy.resources`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'        # Max 2 CPU cores
          memory: 4G       # Max 4GB RAM
        reservations:
          cpus: '1'        # Reserve 1 core
          memory: 2G       # Reserve 2GB
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs container_name

# Check if port is already in use
lsof -i :8000
lsof -i :8501

# Remove stopped containers
docker container prune

# Check container details
docker inspect psychology-chatbot-backend
```

### API Key Issues

```bash
# Verify environment variable is set
docker-compose config | grep GROQ_API_KEY

# Update .env file and restart
docker-compose down
docker-compose up -d
```

### Memory/Performance Issues

```bash
# Monitor resource usage
docker stats

# Limit memory for container
docker update --memory 2g psychology-chatbot-backend

# Check available system memory
free -h
```

### Network Connectivity

```bash
# Test backend from frontend container
docker-compose exec frontend curl http://backend:8000/health

# Check network
docker network inspect psychology-net

# Rebuild network
docker-compose down
docker-compose up -d
```

### Volume Permission Issues

```bash
# Fix permissions
sudo chown -R 1000:1000 data/ logs/ generated_reports/

# View mounted volumes
docker inspect psychology-chatbot-backend | grep -A 20 "Mounts"
```

---

## Production Deployment

### Best Practices

1. **Use specific versions** in Dockerfile
   ```dockerfile
   FROM python:3.11-slim  # Prefer specific tags over 'latest'
   ```

2. **Multi-stage builds** (already implemented)
   - Reduces final image size
   - Improves security
   - Better caching

3. **Non-root user** (already implemented)
   - Runs as user 1000 (appuser)
   - Reduces security vulnerabilities

4. **Health checks** (already implemented)
   - Auto-restart unhealthy containers
   - Load balancer aware

5. **Resource limits**
   - Set CPU and memory limits
   - Prevent resource exhaustion

### Kubernetes Deployment

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: psychology-chatbot
spec:
  replicas: 2
  selector:
    matchLabels:
      app: psychology-chatbot
  template:
    metadata:
      labels:
        app: psychology-chatbot
    spec:
      containers:
      - name: backend
        image: psychology-chatbot:backend
        ports:
        - containerPort: 8000
        env:
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: groq-api-key
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 20
```

Deploy:
```bash
kubectl apply -f k8s-deployment.yaml
```

### Docker Swarm Deployment

```bash
# Initialize Swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml psychology-chatbot

# View services
docker service ls

# Scale service
docker service scale psychology_chatbot_backend=3
```

### Registry Push

```bash
# Tag images
docker tag psychology-chatbot:backend myregistry.azurecr.io/psychology-chatbot:backend
docker tag psychology-chatbot:frontend myregistry.azurecr.io/psychology-chatbot:frontend

# Push to registry
docker push myregistry.azurecr.io/psychology-chatbot:backend
docker push myregistry.azurecr.io/psychology-chatbot:frontend

# Update docker-compose to use registry
# Change: build: . 
# To: image: myregistry.azurecr.io/psychology-chatbot:backend
```

---

## Performance Optimization

### Image Size

```bash
# Check image sizes
docker images | grep psychology

# Optimize by:
# 1. Using alpine/slim base images (already done)
# 2. Multi-stage builds (already done)
# 3. Removing unnecessary dependencies
# 4. Cleaning package managers

# Scan for security vulnerabilities
docker scan psychology-chatbot:backend
```

### Container Startup

```bash
# Check startup time
time docker run psychology-chatbot:backend --help

# Use docker BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build -t psychology-chatbot:backend .
```

### Caching Strategy

```bash
# Force rebuild without cache
docker build --no-cache -t psychology-chatbot:backend .

# Use cache mount (BuildKit)
docker build --mount type=cache,target=/pip-cache -t psychology-chatbot:backend .
```

---

## Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything (containers, images, volumes, networks) - CAUTION!
docker system prune -a --volumes

# Get disk space usage
docker system df
```

---

## Support & Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Container Hardening](https://docs.docker.com/engine/security/)

---

**Last Updated**: April 18, 2026
**Version**: 1.0
**Maintainer**: Psychology Chatbot Team
