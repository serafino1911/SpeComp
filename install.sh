#!/bin/bash
# SpeComp Installation Script for Linux/macOS
# This script checks for Python, installs dependencies, and sets up the application

echo "========================================"
echo "  SpeComp - Spectral Comparator Setup  "
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to check if Python is installed
check_python() {
    if command -v python3 &> /dev/null; then
        return 0
    elif command -v python &> /dev/null; then
        # Check if it's Python 3
        version=$(python --version 2>&1 | grep -oP '\d+\.\d+')
        if [ "${version%%.*}" -ge 3 ]; then
            return 0
        fi
    fi
    return 1
}

# Get Python command (python3 or python)
get_python_cmd() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    else
        echo "python"
    fi
}

# Check Python installation
echo -e "${YELLOW}Checking for Python installation...${NC}"

if check_python; then
    PYTHON_CMD=$(get_python_cmd)
    VERSION=$($PYTHON_CMD --version 2>&1)
    echo -e "${GREEN}✓ Python found: $VERSION${NC}"
    
    # Check version
    MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
    MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')
    
    if [ "$MAJOR" -lt 3 ] || { [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 7 ]; }; then
        echo -e "${RED}✗ Python version is too old. Python 3.7 or higher is required.${NC}"
        echo -e "${YELLOW}Please install Python 3.7 or higher from: https://www.python.org/downloads/${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo ""
    echo -e "${YELLOW}Please install Python 3.7 or higher:${NC}"
    echo "  - Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
    echo "  - Fedora/RHEL:   sudo dnf install python3 python3-pip"
    echo "  - macOS:         brew install python3"
    echo "  - Or download from: https://www.python.org/downloads/"
    exit 1
fi

echo ""

# Check if pip is available
echo -e "${YELLOW}Checking for pip...${NC}"
if $PYTHON_CMD -m pip --version &> /dev/null; then
    PIP_VERSION=$($PYTHON_CMD -m pip --version)
    echo -e "${GREEN}✓ pip found: $PIP_VERSION${NC}"
else
    echo -e "${RED}✗ pip not found. Installing pip...${NC}"
    $PYTHON_CMD -m ensurepip --upgrade
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ pip installed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to install pip${NC}"
        exit 1
    fi
fi

echo ""

# Create virtual environment
echo -e "${YELLOW}Setting up virtual environment...${NC}"
if [ -d ".venv" ]; then
    echo -e "${CYAN}Virtual environment already exists. Skipping creation.${NC}"
else
    $PYTHON_CMD -m venv .venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    else
        echo -e "${RED}✗ Failed to create virtual environment${NC}"
        exit 1
    fi
fi

echo ""

# Activate virtual environment and install requirements
echo -e "${YELLOW}Installing dependencies...${NC}"
echo -e "${CYAN}This may take a few minutes...${NC}"

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo -e "${CYAN}Upgrading pip...${NC}"
python -m pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo -e "${CYAN}Installing packages from requirements.txt...${NC}"
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ All dependencies installed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to install some dependencies${NC}"
        echo -e "${YELLOW}Please check the error messages above${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ requirements.txt not found!${NC}"
    exit 1
fi

echo ""

# Create launcher script
echo -e "${YELLOW}Creating launcher...${NC}"

cat > launch.sh << 'EOF'
#!/bin/bash
# SpeComp Launcher

echo "========================================"
echo "  SpeComp - Spectral Comparator"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -f ".venv/bin/activate" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run install.sh first."
    exit 1
fi

# Activate virtual environment and run the program
source .venv/bin/activate
python src/tools/GUI.py

# Deactivate virtual environment
deactivate
EOF

chmod +x launch.sh

if [ -f "launch.sh" ]; then
    echo -e "${GREEN}✓ Launcher created: launch.sh${NC}"
else
    echo -e "${RED}✗ Failed to create launcher${NC}"
fi

echo ""

# Create data directories if they don't exist
echo -e "${YELLOW}Setting up data directories...${NC}"

directories=("data/DB" "data/Unknown" "data/Results" "reports/figures")
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "${GREEN}✓ Created directory: $dir${NC}"
    else
        echo -e "${CYAN}Directory already exists: $dir${NC}"
    fi
done

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${GREEN}  Installation Complete!                ${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "${YELLOW}To run SpeComp:${NC}"
echo "  ./launch.sh"
echo ""
echo -e "${YELLOW}To activate virtual environment manually:${NC}"
echo "  source .venv/bin/activate"
echo ""
