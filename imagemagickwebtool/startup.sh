#!/bin/bash

# ============================================================
# ImageMagick Web Tool - Automated Startup Script
# Starts both backend and frontend servers for easy deployment
# ============================================================

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}  🎨 ImageMagick Web Tool - Startup Script${NC}"
echo -e "${BLUE}===============================================${NC}"
echo ""

# Get local IP
LOCAL_IP=$(hostname -I | awk '{print $1}')
[ -z "$LOCAL_IP" ] && LOCAL_IP="127.0.0.1"
HOSTNAME=$(hostname)

# Function to check if port is in use
port_in_use() {
    lsof -i :$1 > /dev/null 2>&1
    return $?
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}⚠️  Shutting down services...${NC}"
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}✓${NC} Backend stopped (PID: $BACKEND_PID)"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}✓${NC} Frontend stopped (PID: $FRONTEND_PID)"
    fi
    
    echo ""
    echo -e "${GREEN}✅ All services stopped${NC}"
    exit 0
}

# Set trap for Ctrl+C
trap cleanup INT TERM

# Check if ports are available
echo -e "${BLUE}Checking ports...${NC}"

if port_in_use 5000; then
    echo -e "${RED}❌ Port 5000 is already in use${NC}"
    echo -e "${YELLOW}   Use: lsof -i :5000 to find the process${NC}"
    echo -e "${YELLOW}   Then: kill -9 <PID> to stop it${NC}"
    exit 1
fi

if port_in_use 3000; then
    echo -e "${RED}❌ Port 3000 is already in use${NC}"
    echo -e "${YELLOW}   Use: lsof -i :3000 to find the process${NC}"
    echo -e "${YELLOW}   Then: kill -9 <PID> to stop it${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Ports 3000 and 5000 are available"
echo ""

# Start Backend
echo -e "${BLUE}Starting Backend API on port 5000...${NC}"
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found, creating...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
else
    source venv/bin/activate
fi

python app.py > /tmp/imagemagick_backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}❌ Backend failed to start${NC}"
    echo -e "${YELLOW}   Check /tmp/imagemagick_backend.log for details${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
echo ""

# Start Frontend
echo -e "${BLUE}Starting Frontend Server on port 3000...${NC}"
cd "$PROJECT_DIR"

python frontend_server.py > /tmp/imagemagick_frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 1

if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}❌ Frontend failed to start${NC}"
    echo -e "${YELLOW}   Check /tmp/imagemagick_frontend.log for details${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
echo ""

# Display access information
echo -e "${BLUE}===============================================${NC}"
echo -e "${GREEN}🚀 Services Running!${NC}"
echo -e "${BLUE}===============================================${NC}"
echo ""
echo -e "${YELLOW}📍 Access the application:${NC}"
echo -e "   ${GREEN}Local:    http://localhost:3000${NC}"
echo -e "   ${GREEN}Network:  http://$LOCAL_IP:3000${NC}"
echo -e "   ${GREEN}Hostname: http://$HOSTNAME:3000${NC}"
echo ""
echo -e "${YELLOW}📊 Backend API:${NC}"
echo -e "   ${GREEN}http://$LOCAL_IP:5000${NC}"
echo ""
echo -e "${YELLOW}⚙️  Usage:${NC}"
echo "   1. Open browser and visit one of the URLs above"
echo "   2. Upload images to process"
echo "   3. Select filters and apply mutations"
echo ""
echo -e "${YELLOW}📋 Tips:${NC}"
echo "   • Share the Network URL with others on your LAN"
echo "   • Check console (F12) for any errors"
echo "   • Press Ctrl+C to stop all services"
echo ""
echo -e "${YELLOW}📝 Logs:${NC}"
echo "   Backend:  /tmp/imagemagick_backend.log"
echo "   Frontend: /tmp/imagemagick_frontend.log"
echo ""
echo -e "${BLUE}===============================================${NC}"
echo ""

# Keep script running
wait
