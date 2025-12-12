# SpeComp - Spectral Comparator

**A comprehensive tool for Raman spectroscopy analysis, database comparison, and interactive spectral manipulation.**

## Overview

SpeComp (Spectral Comparator) is a Python-based desktop application designed for analyzing and comparing Raman spectra. It provides powerful tools for matching unknown spectra against a database, preprocessing spectral data, and performing interactive manual corrections with advanced filtering capabilities.

## Key Features

### 🔍 **Database Comparison & Matching**

Compare unknown spectra against a comprehensive database using multiple correlation algorithms:

- **Normalized Correlation** - Standard correlation coefficient analysis
- **Hit Quality Index (HQI)** - Specialized metric for spectral matching quality
- **Convolution** - Wavelenght-domain convolution matching
- **FFT Convolution** - Fast Fourier Transform-based convolution (faster for large datasets)
- **Discrete Correlation** - Point-by-point correlation analysis
- **Correlate Correlation** - Integrated correlation analysis
- **Difference Metric** - Normalized difference calculation

Each algorithm can be enabled/disabled independently, allowing you to customize the analysis for your specific needs.

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
   - Wavelength-dependent adaptive subtraction using local least-squares optimization
   - Assumes that $s(\lambda) \approx t(\lambda) + \beta(\lambda)b(\lambda)$, where:
     - $s(\lambda)$ = observed spectrum (working file)
     - $t(\lambda)$ = true sample spectrum
     - $b(\lambda)$ = background/filter spectrum
     - $\beta(\lambda)$ = wavelength-dependent scaling factor
   - The corrected spectrum is: $t(\lambda) = s(\lambda) - \beta(\lambda)b(\lambda)$
   - For each wavelength $\lambda_0$, uses a sliding window $W$ (adjustable parameter) to solve:
     
     $$\beta(\lambda_0) = \min_{\beta} \sum_{\lambda \in W} [s(\lambda) - \beta(\lambda_0)b(\lambda)]^2$$
   
   - The optimal scaling factor at each point is:
     
     $$\beta(\lambda_0) = \frac{\sum_{W} s(\lambda)b(\lambda)}{\sum_{W} b(\lambda)^2}$$
   
   - Window size can be adjusted via the input field (default: 25 points)
   - Automatically smooths the scaling function to reduce noise
   - Best for varying background contributions across the spectrum
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

### Requirements

- Python 3.7 or higher
- Required packages (see `requirements.txt`):
  - numpy
  - scipy
  - matplotlib
  - tkinter (usually included with Python)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/serafino1911/SpeComp.git
cd SpeComp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/tools/GUI.py
```

## Usage Guide

### Basic Workflow

1. **Load Your Spectrum**
   - Click "Load File" and select your unknown spectrum (*.txt file)
   - The file should contain two columns: wavelength and intensity

2. **Configure Analysis Settings** (Optional)
   - Menu → Configuration
   - Select desired comparison algorithms
   - Choose normalization method
   - Set filtering options
   - Define wavelength ranges if needed

3. **Load Database**
   - In Configuration, set the database folder path
   - The program will automatically scan for all *.txt files

4. **Run Comparison**
   - Click "Start" to begin the analysis
   - Results will display the best matches for each enabled algorithm

5. **View Results**
   - Results are ranked by correlation strength
   - Each algorithm shows its top matches (configurable number)
   - Save results to file for documentation

### Advanced Features

#### Filter Subtraction Workflow

1. **Load Working File**: Your spectrum to be processed
2. **Load Filter File**: Reference background or filter spectrum
3. **Click "Filter Subtraction"** to open interactive tool
4. **Choose Method**:
   - **Simple Subtract**: Quick direct subtraction
   - **Smart Subtract**: Automatic intelligent scaling
   - **Manual Peaks**: Fine-tune individual peaks
5. **Manual Peak Editing**:
   - Click on a peak to select it
   - Adjust boundaries with arrow keys
   - Modify intensity up/down as needed
   - Press ESC to deselect
6. **Save**: Export your corrected spectrum

#### Noise Modification

1. Click "Modify noise" to access advanced preprocessing
2. Configure:
   - Gaussian filter parameters (odd numbers only)
   - Baseline correction window length and polynomial order
   - Differential offset
3. Preview different processing options
4. Save modified or difference spectra

#### Display Multiple Spectra

1. Click "Display" to open the multi-spectrum viewer
2. Paste file paths (one per line) into the text box
3. Navigate through spectra with Next/Previous buttons
4. Compare your working file with database entries

## File Format

Spectral data files should be plain text with two tab-separated columns:

```
wavelength1    intensity1
wavelength2    intensity2
wavelength3    intensity3
...
```

Example:
```
200.5    1250.3
201.0    1248.7
201.5    1251.2
```

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
├── data/
│   ├── DB/                           # Database folder (not tracked)
│   ├── Unknown/                      # Unknown spectra (not tracked)
│   └── Results/                      # Analysis results (not tracked)
├── reports/                          # Generated reports (not tracked)
├── requirements.txt                  # Python dependencies
└── README.md                        # This file
```

## Tips & Best Practices

### For Best Comparison Results:
- Use consistent normalization across all spectra
- Apply appropriate filtering to reduce noise
- Define relevant wavelength ranges to focus on diagnostic regions
- Use exclusion zones to remove problematic spectral regions
- Enable multiple algorithms to cross-validate results

### For Filter Subtraction:
- Start with Smart Subtract for automatic baseline matching
- Use Manual Peaks for fine-tuning specific features
- Adjust peak boundaries carefully to maintain smooth transitions
- Zoom in for precise editing of small features
- Save intermediate results to preserve your work

### For Database Management:
- Ensure all spectra cover similar wavelength ranges

## Troubleshooting

**Program won't start**: Ensure all dependencies are installed (`pip install -r requirements.txt`)

**Database not found**: Check that the database path in Configuration points to the correct folder

**Poor matching results**: Try different normalization methods or enable/disable filtering

**Filter subtraction issues**: Ensure working file and filter file have overlapping wavelength ranges

**Peak editing not working**: Click "Manual Peaks" button first, then click on a peak to select it

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

For detailed tutorials and examples:
- [Quick Guide (English) (to be updated)](https://github.com/user-attachments/files/21970889/Raman.Spectra.Comparator_ENGL.pptx)
- [Quick Guide (Italian) (to be updated)](https://github.com/serafino1911/SpeComp/files/11122359/Raman.Spectra.Comparator.pptx)

## License

See [LICENSE](LICENSE) file for details.

## Authors

See [AUTHORS.md](AUTHORS.md) for contributor information.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/serafino1911/SpeComp).

---

**Version**: 2.0  
**Last Updated**: December 2025
