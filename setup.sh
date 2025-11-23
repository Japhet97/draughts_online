#!/bin/bash

# Draughts Online - Setup Script
# This script sets up the development environment

echo "=========================================="
echo "  Draughts Online - Setup Script"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.11 or higher.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"

# Check if Docker is installed
echo "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠ Docker is not installed. Install Docker for easier deployment.${NC}"
    DOCKER_AVAILABLE=false
else
    echo -e "${GREEN}✓ Docker found: $(docker --version)${NC}"
    DOCKER_AVAILABLE=true
fi

# Check if Flutter is installed (optional)
echo "Checking Flutter installation..."
if ! command -v flutter &> /dev/null; then
    echo -e "${YELLOW}⚠ Flutter is not installed. Install Flutter to build mobile app.${NC}"
    FLUTTER_AVAILABLE=false
else
    echo -e "${GREEN}✓ Flutter found: $(flutter --version | head -n 1)${NC}"
    FLUTTER_AVAILABLE=true
fi

echo ""
echo "=========================================="
echo "  Backend Setup"
echo "=========================================="

# Navigate to backend
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    
    # Generate a random secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    # Update .env file with generated secret key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-change-this-in-production/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/your-secret-key-change-this-in-production/$SECRET_KEY/" .env
    fi
    
    echo -e "${YELLOW}⚠ Please update .env file with your PayChangu credentials${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

echo ""

# Ask user if they want to use Docker
if [ "$DOCKER_AVAILABLE" = true ]; then
    echo "Do you want to start the application with Docker? (y/n)"
    read -r USE_DOCKER
    
    if [ "$USE_DOCKER" = "y" ]; then
        echo "Starting application with Docker Compose..."
        docker-compose up -d
        echo -e "${GREEN}✓ Application started!${NC}"
        echo ""
        echo "Access the API at: http://localhost:8000"
        echo "API Documentation: http://localhost:8000/docs"
        echo ""
        echo "To view logs: docker-compose logs -f"
        echo "To stop: docker-compose down"
    else
        echo -e "${YELLOW}Manual setup selected. Please ensure PostgreSQL and Redis are running.${NC}"
        echo ""
        echo "To start the development server:"
        echo "  cd backend"
        echo "  source venv/bin/activate"
        echo "  uvicorn app.main:app --reload"
    fi
else
    echo -e "${YELLOW}Docker not available. Please ensure PostgreSQL and Redis are running.${NC}"
    echo ""
    echo "To start the development server:"
    echo "  cd backend"
    echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
    echo "  uvicorn app.main:app --reload"
fi

cd ..

echo ""
echo "=========================================="
echo "  Frontend Setup (Optional)"
echo "=========================================="

if [ "$FLUTTER_AVAILABLE" = true ]; then
    echo "Do you want to set up the Flutter app? (y/n)"
    read -r SETUP_FLUTTER
    
    if [ "$SETUP_FLUTTER" = "y" ]; then
        cd frontend/draughts_app
        echo "Getting Flutter dependencies..."
        flutter pub get
        echo -e "${GREEN}✓ Flutter app ready${NC}"
        echo ""
        echo "To run the Flutter app:"
        echo "  cd frontend/draughts_app"
        echo "  flutter run"
        cd ../..
    fi
else
    echo -e "${YELLOW}Flutter not installed. Skipping mobile app setup.${NC}"
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Update backend/.env with your configuration"
echo "2. Start the backend server"
echo "3. (Optional) Run the Flutter app"
echo ""
echo "Documentation:"
echo "  - README.md - Project overview"
echo "  - docs/API.md - API documentation"
echo "  - docs/DEPLOYMENT.md - Deployment guide"
echo ""
echo "Happy coding! 🎮"
