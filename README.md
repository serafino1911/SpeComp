# SpeComp - Spectral Comparator

**A comprehensive tool for Raman spectroscopy analysis, database comparison, and interactive spectral manipulation.**

## Overview

SpeComp (Spectral Comparator) is a Python-based desktop application designed for analyzing and comparing Raman spectra. It provides powerful tools for matching unknown spectra against a database, preprocessing spectral data, and performing interactive manual corrections with advanced filtering capabilities.

## Key Features

### 🔍 **Database Comparison & Matching**

Compare unknown spectra against a comprehensive database using multiple correlation algorithms:

- **Normalized Correlation** - Standard correlation coefficient analysis
- **Hit Quality Index (HQI)** - Specialized metric for spectral matching quality
- **Convolution** - Wavelength-domain convolution matching
- **FFT Convolution** - Fast Fourier Transform-based convolution (faster for large datasets)
- **Discrete Correlation** - Point-by-point correlation analysis
- **Correlate Correlation** - Integrated correlation analysis
- **Difference Metric** - Normalized difference calculation

Each algorithm can be enabled/disabled independently, allowing you to customize the analysis for your specific needs.

📖 **For detailed mathematical descriptions of all algorithms, see [METHODS.md](METHODS.md)**

### 📊 **Interactive Spectral Visualization**

- Display multiple spectra simultaneously
- Compare working files with filter references
- Real-time plot updates

### 🛠️ **Advanced Spectral Preprocessing**

#### Normalization Methods:
- **MinMax Normalization** - Scale data between 0 and 1
- **Statistical Normalization** - Z-score standardization (mean=0, std=1) (experimental)

#### Filtering Options:
- **Gaussian Filter** - Smooth spectral noise (customizable window size)
- **Baseline Correction** - Remove baseline drift using Savitzky-Golay filter
- **Fluorescence Filter** - Remove fluorescence background (beta feature)
- **Custom wavelength ranges** - Define specific regions for analysis
- **Exclusion zones** - Exclude specific wavelength regions from comparison

### ✨ **Interactive Filter Subtraction Tool**

The Filter Subtraction module provides tools for removing background signals and manually editing spectral peaks:

#### Automatic Subtraction Methods:
1. **Simple Subtract** 
   - Direct subtraction of filter from working spectrum
   - Ensures values don't go below zero
   - Best for straightforward background removal

2. **Smart Subtract** 
   - Adaptive wavelength-dependent background subtraction using local least-squares optimization
   - Window size adjustable via input field (default: the whole spectrum, minimum possible 25)
   - Automatically smooths the scaling function to reduce noise
   - Best for varying background contributions across the spectrum
   - _See [METHODS.md](METHODS.md#smart-subtract-adaptive-weighted-subtraction) for mathematical details_
   
#### Manual Peak Editing:
Interactive peak-by-peak modification with keyboard controls:

- **Click to Select**: Click on any peak to select it for editing
- **Automatic Peak Detection**: Intelligently finds peak boundaries by detecting local minima
- **Boundary Adjustment**:
  - `LEFT/RIGHT arrows` - Expand peak region outward
  - `SHIFT + LEFT/RIGHT` - Shrink peak region inward
- **Intensity Modification**:
  - `UP arrow` - Increase peak intensity (2% per press)
  - `DOWN arrow` - Decrease peak intensity (2% per press)
- **Zoom Preservation**: Maintains your current zoom level during all editing operations
- **ESC**: Deselect current peak

#### Additional Features:
- **Reset Button**: Restore original data at any time
- **Save Button**: Export modified spectra to new files

### 📁 **Data Management**

- Load spectral data from text files (tab-separated: wavelength, intensity)
- Support for large database directories with automatic file discovery
- Save processed and modified spectra
- Export comparison results in readable text format
- Configure and save analysis settings (*.cnf files)

### ⚙️ **Configuration System**

Create, save, and load custom analysis configurations including:
- Selected comparison algorithms
- Normalization preferences
- Filter settings
- Number of results to display
- Database location
- Wavelength ranges and exclusion zones

## Installation

**📦 For detailed installation instructions including automated setup scripts, troubleshooting, and platform-specific guidance, see [INSTALL.md](INSTALL.md)**

### Quick Start

**Requirements:** Python 3.7 or higher

**Automated Installation (Recommended):**
- **Windows:** Run `install.ps1` in PowerShell
- **Linux/macOS:** Run `./install.sh` in terminal

**Manual Installation:**
```bash
git clone https://github.com/serafino1911/SpeComp.git
cd SpeComp
pip install -r requirements.txt
python src/tools/GUI.py
```

## Quick Start

After installation:

1. **Load your spectrum** - Click "Load File" and select your *.txt file
2. **Configure settings** - Menu → Configuration (select algorithms, set database path)
3. **Run comparison** - Click "Start" to analyze
4. **View results** - Review matches and save results

📖 **For detailed usage instructions, workflows, and tips, see [USAGE.md](USAGE.md)**

## Project Structure

```
SpeComp/
├── src/
│   └── tools/
│       ├── GUI.py                    # Main application window
│       ├── comarator.py              # Comparison algorithms
│       └── modules/
│           ├── basic_functions.py    # Data processing utilities
│           ├── gui_functions.py      # GUI interaction functions
│           └── importer.py           # Common imports
├── requirements.txt                  # Python dependencies
├── README.md                         # This file (quick overview)
├── USAGE.md                          # Complete usage guide
├── METHODS.md                        # Mathematical documentation
├── INSTALL.md                        # Installation guide
```

## File Format

Spectral data files should be plain text with two tab-separated columns:

```
wavelength    intensity
200.5         1250.3
201.0         1248.7
201.5         1251.2
```

📖 **For detailed file format specifications, see [USAGE.md](USAGE.md#file-format)**

## Troubleshooting

**Common issues:**
- **Program won't start**: Ensure all dependencies are installed (`pip install -r requirements.txt`)
- **Database not found**: Check that the database path in Configuration points to the correct folder
- **Poor matching results**: Try different normalization methods or enable/disable filtering
- **Filter subtraction issues**: Ensure working file and filter file have overlapping wavelength ranges
- **Peak editing not working**: Click "Manual Peaks" button first, then click on a peak to select it

📖 **For more detailed troubleshooting and installation issues, see [INSTALL.md](INSTALL.md#troubleshooting)**

## Citation

If you use SpeComp in your research, please cite:

Santostefano, M. (2025). SpeComp: A comprehensive tool for Raman spectroscopy analysis (Version 2.0) [Computer software]. https://github.com/serafino1911/SpeComp


**BibTeX format:**
```bibtex
@software{specomp,
   title = {SpeComp: A comprehensive tool for Raman spectroscopy analysis},
   author = {Santostefano, Matteo},
   organization = {PM_TEN S.r.l},
   year = {2025},
   url = {https://github.com/serafino1911/SpeComp},
   version = {2.0}
}
```

**CIF format available at:** [CITATION.cff](CITATION.cff)


## Documentation

### Technical Documentation
- **[USAGE.md](USAGE.md)** - Complete usage guide with workflows, tips, and best practices
- **[METHODS.md](METHODS.md)** - Detailed mathematical descriptions of all comparison algorithms and processing methods
- **[INSTALL.md](INSTALL.md)** - Complete installation guide with automated scripts and troubleshooting

### Tutorials and Guides
- [Quick Guide (English) (to be updated)](https://github.com/user-attachments/files/21970889/Raman.Spectra.Comparator_ENGL.pptx)
- [Quick Guide (Italian) (to be updated)](https://github.com/serafino1911/SpeComp/files/11122359/Raman.Spectra.Comparator.pptx)

## License

See [LICENSE](LICENSE) file for details.

## Authors

See [AUTHORS.md](AUTHORS.md) for contributor information.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/serafino1911/SpeComp).

---

