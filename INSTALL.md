# SpeComp Installation Guide

This directory contains installation scripts for different operating systems.

## Windows Installation

### Method 1: PowerShell Script (Recommended)

1. Right-click on `install.ps1` and select "Run with PowerShell"
   
   **OR**
   
   Open PowerShell in the SpeComp directory and run:
   ```powershell
   .\install.ps1
   ```

   **Note**: If you get an execution policy error, run PowerShell as Administrator and execute:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then try running the install script again.

2. The script will:
   - Check if Python is installed (and help you install it if needed)
   - Create a virtual environment
   - Install all required dependencies
   - Create a launcher (`launch.bat`)
   - Set up data directories

3. After installation, run SpeComp by double-clicking `launch.bat`

### Method 2: Manual Installation (Windows)

```batch
# Check Python version
python --version

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the program
python src\tools\GUI.py
```

## Linux/macOS Installation

### Method 1: Bash Script (Recommended)

1. Make the script executable:
   ```bash
   chmod +x install.sh
   ```

2. Run the installation script:
   ```bash
   ./install.sh
   ```

3. The script will:
   - Check if Python 3 is installed
   - Create a virtual environment
   - Install all required dependencies
   - Create a launcher (`launch.sh`)
   - Set up data directories

4. After installation, run SpeComp:
   ```bash
   ./launch.sh
   ```

### Method 2: Manual Installation (Linux/macOS)

```bash
# Check Python version
python3 --version

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the program
python src/tools/GUI.py
```

## Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows 10+, Linux (Ubuntu 18.04+, Debian, Fedora), macOS 10.14+
- **Dependencies** (automatically installed):
  - numpy
  - scipy
  - matplotlib

## Troubleshooting

### Python Not Found

**Windows:**
- Download from: https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# Fedora/RHEL
sudo dnf install python3 python3-pip
```

**macOS:**
```bash
# Using Homebrew
brew install python3
```

### Permission Errors (Linux/macOS)

If you get permission errors:
```bash
# Make scripts executable
chmod +x install.sh
chmod +x launch.sh
```

### Virtual Environment Issues

If the virtual environment fails to create:

**Windows:**
```powershell
# Install virtualenv
pip install virtualenv
virtualenv .venv
```

**Linux/macOS:**
```bash
# Install python3-venv
sudo apt-get install python3-venv  # Ubuntu/Debian
```

### tkinter Not Found

tkinter is usually included with Python, but if missing:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
tkinter should be included with Python from python.org

## Quick Start After Installation

### Windows
```batch
# Run the program
launch.bat

# Or manually:
.venv\Scripts\activate
python src\tools\GUI.py
```

### Linux/macOS
```bash
# Run the program
./launch.sh

# Or manually:
source .venv/bin/activate
python src/tools/GUI.py
```

## Directory Structure After Installation

```
SpeComp/
├── .venv/                  # Virtual environment (created by installer)
├── data/
│   ├── DB/                 # Your spectral database (create subfolders as needed)
│   ├── Unknown/            # Unknown spectra to analyze
│   └── Results/            # Analysis results
├── reports/
│   └── figures/            # Generated figures
├── src/
│   └── tools/              # Application code
├── install.ps1             # Windows installer
├── install.sh              # Linux/macOS installer
├── launch.bat              # Windows launcher (created by installer)
├── launch.sh               # Linux/macOS launcher (created by installer)
├── requirements.txt        # Python dependencies
└── README2.md              # Full documentation
```

## Updating

To update dependencies:

**Windows:**
```batch
.venv\Scripts\activate
pip install --upgrade -r requirements.txt
```

**Linux/macOS:**
```bash
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```

## Uninstalling

To remove SpeComp:
1. Delete the entire SpeComp directory
2. (Optional) Remove Python if you don't need it for other applications

## Support

For issues or questions:
- Check the [README.md](README.md) for detailed usage instructions
- Visit: https://github.com/serafino1911/SpeComp
- Check existing issues or create a new one

## What the Installers Do

The installation scripts perform the following steps:

1. **Python Check**: Verify Python 3.7+ is installed
2. **pip Check**: Ensure pip package manager is available
3. **Virtual Environment**: Create isolated Python environment
4. **Dependencies**: Install numpy, scipy, matplotlib
5. **Launcher**: Create convenient startup script
6. **Directories**: Set up data and reports folders
7. **Verification**: Confirm successful installation

After installation, you can start using SpeComp immediately with the launcher!
