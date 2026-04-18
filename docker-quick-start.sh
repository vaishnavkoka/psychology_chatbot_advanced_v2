#!/bin/bash

# Psychology Chatbot - Docker Quick Start Script
# Automates Docker and Docker Compose setup and deployment

set -e

# Console colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        print_info "Install Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    print_success "Docker found: $(docker --version)"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        print_info "Install Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi
    print_success "Docker Compose found: $(docker-compose --version)"
    
    # Check Docker daemon
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker daemon is not running"
        print_info "Start Docker and try again"
        exit 1
    fi
    print_success "Docker daemon is running"
}

# Setup environment
setup_environment() {
    print_header "Setting Up Environment"
    
    # Check for .env file
    if [ ! -f .env ]; then
        if [ -f .env.docker ]; then
            print_info "Copying .env.docker to .env"
            cp .env.docker .env
            print_success ".env file created from .env.docker"
        else
            print_warn ".env file not found"
            print_info "Creating default .env file..."
            cat > .env << EOF
GROQ_API_KEY=your-groq-api-key-here
HUGGINGFACE_API_KEY=
SERPER_API_KEY=
ENV=production
PYTHONUNBUFFERED=1
PYTHON_DONT_WRITE_BYTECODE=1
EOF
            print_info "Please update .env with your API keys"
        fi
    else
        print_success ".env file already exists"
    fi
    
    # Create required directories
    for dir in data logs generated_reports; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_success "Created directory: $dir"
        fi
    done
}

# Show API key prompt
prompt_api_keys() {
    print_header "API Key Configuration"
    
    # Check if GROQ_API_KEY is set
    if grep -q "GROQ_API_KEY=your-groq-api-key-here" .env; then
        print_warn "GROQ_API_KEY is not configured"
        echo -e "Enter your GROQ API key (get from https://console.groq.com/):"
        read -r groq_key
        
        if [ -n "$groq_key" ]; then
            sed -i "s|GROQ_API_KEY=your-groq-api-key-here|GROQ_API_KEY=$groq_key|g" .env
            print_success "GROQ_API_KEY updated"
        else
            print_error "GROQ_API_KEY is required to run the application"
            exit 1
        fi
    else
        print_success "GROQ_API_KEY is configured"
    fi
}

# Build Docker images
build_images() {
    print_header "Building Docker Images"
    
    print_info "Building backend image..."
    if DOCKER_BUILDKIT=1 docker build -t psychology-chatbot:backend .; then
        print_success "Backend image built successfully"
    else
        print_error "Failed to build backend image"
        exit 1
    fi
    
    print_info "Building frontend image..."
    if DOCKER_BUILDKIT=1 docker build -f Dockerfile.frontend -t psychology-chatbot:frontend .; then
        print_success "Frontend image built successfully"
    else
        print_error "Failed to build frontend image"
        exit 1
    fi
    
    # Show image sizes
    echo ""
    print_info "Image sizes:"
    docker images | grep psychology-chatbot
}

# Start services with Docker Compose
start_services() {
    print_header "Starting Services"
    
    print_info "Bringing up services..."
    if docker-compose up -d; then
        print_success "Services started successfully"
    else
        print_error "Failed to start services"
        exit 1
    fi
    
    # Wait for services to be ready
    print_info "Waiting for services to be ready..."
    sleep 10
    
    # Check service status
    echo ""
    print_info "Service Status:"
    docker-compose ps
    
    # Check health
    echo ""
    print_info "Health Checks:"
    
    if docker-compose exec -T backend curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Backend is healthy"
    else
        print_warn "Backend health check failed (may still be starting)"
    fi
    
    if docker-compose exec -T frontend curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
        print_success "Frontend is healthy"
    else
        print_warn "Frontend health check failed (may still be starting)"
    fi
}

# Show access information
show_access_info() {
    print_header "Application Ready!"
    
    echo -e "${GREEN}Access your application at:${NC}\n"
    echo -e "  🎨 Frontend: ${CYAN}http://localhost:8501${NC}"
    echo -e "  🔌 Backend:  ${CYAN}http://localhost:8000${NC}"
    echo -e "  📚 API Docs: ${CYAN}http://localhost:8000/docs${NC}\n"
    
    echo -e "${GREEN}Useful commands:${NC}\n"
    echo -e "  View logs:       ${CYAN}docker-compose logs -f${NC}"
    echo -e "  Stop services:   ${CYAN}docker-compose down${NC}"
    echo -e "  Restart services: ${CYAN}docker-compose restart${NC}"
    echo -e "  Backend shell:   ${CYAN}docker-compose exec backend bash${NC}"
    echo -e "  View stats:      ${CYAN}docker stats${NC}\n"
}

# Main menu
show_menu() {
    echo -e "\n${BLUE}Psychology Chatbot - Docker Setup${NC}\n"
    echo "Select an option:"
    echo "  1) Full setup (build + start)"
    echo "  2) Build images only"
    echo "  3) Start services (docker-compose up)"
    echo "  4) Stop services (docker-compose down)"
    echo "  5) View logs"
    echo "  6) Restart services"
    echo "  7) Update environment"
    echo "  8) Exit"
    echo ""
    read -p "Enter your choice [1-8]: " choice
}

# Handle menu selection
handle_menu() {
    case $choice in
        1)
            check_prerequisites
            setup_environment
            prompt_api_keys
            build_images
            start_services
            show_access_info
            ;;
        2)
            check_prerequisites
            setup_environment
            build_images
            ;;
        3)
            print_header "Starting Services"
            docker-compose up -d
            docker-compose ps
            show_access_info
            ;;
        4)
            print_header "Stopping Services"
            docker-compose down
            print_success "Services stopped"
            ;;
        5)
            docker-compose logs -f
            ;;
        6)
            print_header "Restarting Services"
            docker-compose restart
            print_success "Services restarted"
            docker-compose ps
            ;;
        7)
            setup_environment
            echo ""
            read -p "Do you want to update API keys? (y/n): " update_keys
            if [ "$update_keys" = "y" ]; then
                prompt_api_keys
                print_info "Rebuilding with updated configuration..."
                docker-compose down
                docker-compose up -d
            fi
            ;;
        8)
            print_info "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid option"
            ;;
    esac
}

# Main execution
main() {
    # Check if running in interactive mode
    if [ -t 0 ]; then
        # Interactive mode
        while true; do
            show_menu
            handle_menu
            echo ""
            read -p "Press Enter to continue..."
        done
    else
        # Non-interactive mode (full setup)
        check_prerequisites
        setup_environment
        prompt_api_keys
        build_images
        start_services
        show_access_info
    fi
}

# Run main function
main
