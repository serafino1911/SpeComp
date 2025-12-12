# SpeComp Usage Guide

Complete guide to using all features of SpeComp for Raman spectroscopy analysis.

## Table of Contents
- [Basic Workflow](#basic-workflow)
- [Advanced Features](#advanced-features)
- [File Format](#file-format)
- [Tips & Best Practices](#tips--best-practices)

---

## Basic Workflow

### 1. Load Your Spectrum

1. Click **"Load File"** button in the main window
2. Navigate to your unknown spectrum file (*.txt format)
3. Select the file and click "Open"
4. The filename will appear in the working file field

**File Requirements:**
- Plain text format (*.txt)
- Two tab-separated columns: wavelength and intensity
- Consistent wavelength spacing recommended but not required

---

### 2. Configure Analysis Settings

Access the configuration window through **Menu → Configuration**

#### Select Comparison Algorithms

Enable the algorithms you want to use by checking their boxes:
- ☑️ **Normalized Correlation** - General purpose matching
- ☑️ **Hit Quality Index (HQI)** - Spectroscopy-specific metric
- ☑️ **Convolution** - Pattern matching with shift tolerance
- ☑️ **FFT Convolution** - Fast version for large databases
- ☑️ **Discrete Correlation** - Alternative correlation method
- ☑️ **Correlate Correlation** - Integrated similarity
- ☑️ **Difference Metric** - Direct comparison (lower is better)

**Tip:** Enable multiple algorithms for cross-validation

#### Choose Normalization Method

Select one normalization approach:
- **MinMax** - Scales all values to [0, 1] range (recommended for most cases)
- **Stat** - Z-score normalization (experimental, for emphasizing deviations)

#### Set Filtering Options

- ☑️ **Filter** - Apply Gaussian smoothing to reduce noise
- ☑️ **Fluorescence Filter** - Remove fluorescence background (beta feature)

#### Configure Analysis Parameters

- **List results**: Set how many top matches to display for each algorithm (1-100)
- **Database Folder**: Click "Browse" and select your spectral database directory

#### Define Wavelength Ranges (Optional)

- **Min/Max**: Limit analysis to specific wavelength range
  - Example: Min=400, Max=2000 for visible to near-IR region
- **Min Exclusion/Max Exclusion**: Exclude problematic regions
  - Example: Exclude laser line or saturated regions

#### Save/Load Configurations

- **Save**: Store current settings to a *.cnf file for reuse
- **Load**: Import previously saved configuration
- **Use**: Apply settings and close the configuration window

---

### 3. Load Database

In the Configuration window:
1. Click the **"Browse"** button next to "Database Folder"
2. Navigate to the folder containing your reference spectra
3. Select the folder
4. Click **"Use"** to apply

**Database Requirements:**
- All *.txt files in the folder will be automatically included
- Files should have the same format as your working file
- Subdirectories are not scanned (only top-level files)

---

### 4. Run Comparison

1. Ensure working file is loaded and configuration is set
2. Click **"Start"** button in the main window
3. A loading animation will appear
4. Processing time depends on:
   - Number of reference spectra
   - Number of enabled algorithms
   - Filtering options

**Performance Tips:**
- Use FFT Convolution instead of regular Convolution for large databases
- Disable unused algorithms to speed up processing
- Consider using wavelength range limits to reduce data points

---

### 5. View Results

After processing completes, a results window will display:

#### Results Organization

Results are grouped by algorithm:
```
NORM_CORR:
    path/to/spectrum1.txt = 0.987
    path/to/spectrum2.txt = 0.956
    path/to/spectrum3.txt = 0.923
    ...

HQI:
    path/to/spectrum4.txt = 0.945
    path/to/spectrum1.txt = 0.932
    ...
```

#### Interpreting Results

**For most algorithms (higher is better):**
- Values near **1.0** = excellent match
- Values **0.7-0.9** = good similarity
- Values **< 0.5** = weak correlation

**For DIFF algorithm (lower is better):**
- Values near **0** = nearly identical
- Higher values = more different

#### Saving Results

1. Click **"Save"** button in results window
2. Choose location and filename
3. Results saved as plain text file

---

## Advanced Features

### Filter Subtraction Workflow

The Filter Subtraction tool enables background removal and manual peak editing.

#### Setup

1. **Load Working File**: Your spectrum to be corrected
2. **Load Filter File**: Reference background/filter spectrum
   - Click "Load Filter" button
   - Select appropriate background spectrum
3. Click **"Filter Subtraction"** button to open interactive tool

#### Interactive Window Layout

- **Main Plot**: Shows three spectra
  - Dashed line: Original working file
  - Thin line: Filter file
  - Thick line: Modified spectrum (starts as copy of working file)
- **Control Buttons** (bottom):
  - Simple Subtract
  - Smart Subtract
  - Manual Peaks
  - Reset
  - Save
  - Zoom Out
- **Window Size Input** (above buttons): For Smart Subtract parameter

---

### Simple Subtract

**When to use:** Direct background subtraction with constant offset

**How it works:**
1. Click **"Simple Subtract"** button
2. Filter spectrum is interpolated to match working file wavelength axis
3. Direct subtraction: Modified = Working - Filter
4. Negative values are set to zero
5. Plot updates immediately

**Best for:**
- Flat baselines
- Constant background signals
- Quick initial correction

---

### Smart Subtract

**When to use:** Variable background that changes across wavelength range

**How it works:**
1. Adjust **Window** parameter if needed (default: 25 points)
   - Smaller window: Adapts faster to local changes
   - Larger window: Smoother but less adaptive
2. Click **"Smart Subtract"** button
3. Algorithm calculates optimal scaling factor at each wavelength
4. Applies wavelength-dependent subtraction
5. Plot updates with corrected spectrum

**Best for:**
- Fluorescence with varying intensity
- Wavelength-dependent backgrounds
- Complex baseline shapes

**See [METHODS.md](METHODS.md#smart-subtract-adaptive-weighted-subtraction) for mathematical details**

---

### Manual Peaks Editing

**When to use:** Fine-tuning individual peaks after automatic subtraction

#### Activation

1. Click **"Manual Peaks"** button
2. Instruction window appears with keyboard controls
3. Plot becomes interactive

#### Selecting a Peak

1. **Click** anywhere on a peak you want to modify
2. Peak boundaries are automatically detected
3. Selected region highlights in **red**
4. Console shows peak range and available controls

#### Adjusting Peak Boundaries

Modify the extent of the selected peak region:

- **LEFT Arrow**: Expand boundary to the left (add one point)
- **RIGHT Arrow**: Expand boundary to the right (add one point)
- **SHIFT + LEFT**: Shrink boundary from the left (remove one point)
- **SHIFT + RIGHT**: Shrink boundary from the right (remove one point)

**Tips:**
- Zoom in for precise boundary adjustment
- Boundaries stop at adjacent peaks or data limits
- Zoom level is preserved during adjustments

#### Modifying Peak Intensity

Adjust the height of the selected peak:

- **UP Arrow**: Increase intensity by 2%
- **DOWN Arrow**: Decrease intensity by 2%
- Hold key for multiple increments

**Features:**
- Smooth edge blending prevents discontinuities
- Baseline interpolation maintains realistic transitions
- Changes apply to entire selected region
- Zoom level is preserved

#### Deselecting

- Press **ESC** to deselect current peak
- Red highlight disappears
- Select a different peak by clicking elsewhere

#### Using Matplotlib Tools

All standard matplotlib navigation tools work:
- **Pan**: Click and drag to move view
- **Zoom**: Use zoom rectangle tool
- **Home**: Reset to original view
- **Back/Forward**: Navigate view history

---

### Reset and Save

- Click **"Reset"** button to restore original working file data
- Click **"Save"** button to save the modified spectrum

---

### Noise Modification

Access advanced preprocessing tools.

1. Click **"Modify noise"** button in main window
2. Preprocessing window opens

#### Available Options

**Gaussian Filter:**
- Check "Gaussian Filter (odd)"
- Enter window size (must be odd number)
- Smooths high-frequency noise
- Larger window = more smoothing

**Baseline Correction:**
- Check "Baseline Correction"
- Set window_length (odd number, typically 401)
- Set polyorder (typically 3)
- Removes baseline drift using Savitzky-Golay filter

**Differential:**
- Set "Diff" value (offset parameter)

#### Display Options

- ☑️ **Display Original**: Show unprocessed spectrum
- ☑️ **Display Modified**: Show processed spectrum

#### Actions

- **Apply**: View preprocessed spectrum
- **Save**: Export processed data
- **Save Difference**: Export difference between original and processed

---

### Display Multiple Spectra

Compare your working file with multiple reference spectra.

1. Click **"Display"** button
2. Text box window opens
3. **Paste file paths** (one per line)
   - Full paths recommended
   - Can include database matches from results (copy and past from the result window)
4. Click **"Display"** button

#### Navigation

- **Next**: Advance by one spectrum
- **Prev**: Go back one spectrum  
- **Next N Files**: Jump forward by N spectra (N set in configuration)
- **Prev N Files**: Jump back by N spectra

#### Display Options

- Click **"Config"** to set normalization and filtering
- Choices apply only to this display session

---

## File Format

### Input File Specification

Spectral data files must be plain text with tab-separated values.

#### Format

```
wavelength1    intensity1
wavelength2    intensity2
wavelength3    intensity3
...
```

#### Example

```
200.0	1250.3
200.5	1248.7
201.0	1251.2
201.5	1255.8
202.0	1249.3
```

#### Requirements

- **Separator**: Tab character (`\t`)
- **Columns**: Exactly 2 (wavelength, intensity)
- **Data Type**: Numeric values (integers or floats)
- **Encoding**: Plain text (UTF-8 recommended)
- **Extension**: .txt (simpler, but every text file works)

#### Optional Characteristics

- **Header**: No header row (data starts from first line)
- **Spacing**: Can be irregular (will be interpolated when needed)
- **Range**: No specific limits, but consistency across dataset recommended


## Tips & Best Practices

#### Filter Subtraction Window

- **Click**: Select peak (in Manual Peaks mode)
- **LEFT/RIGHT**: Adjust peak boundaries
- **SHIFT+LEFT/RIGHT**: Shrink peak boundaries
- **UP/DOWN**: Modify peak intensity
- **ESC**: Deselect current peak

#### Matplotlib Navigation

- **Pan**: Click and drag
- **Zoom**: Zoom rectangle tool
- **Home**: Reset view
- **Back/Forward**: View history
- **Save**: Export plot image

---

### Troubleshooting Workflow Issues

#### No Results Appear

**Check:**
- [ ] Working file is loaded
- [ ] Database folder is set and contains *.txt files
- [ ] At least one algorithm is enabled
- [ ] Wavelength ranges overlap between working and database files

#### Poor Match Quality

**Try:**
- Different normalization method
- Enable/disable filtering
- Adjust wavelength range to diagnostic regions
- Use exclusion zones for problematic regions
- Check if database contains relevant reference spectra

#### Filter Subtraction Not Working

**Verify:**
- Both working file AND filter file are loaded
- Files have overlapping wavelength ranges
- Filter file represents appropriate background

#### Manual Peaks Issues

**Solutions:**
- Click "Manual Peaks" button first
- Click directly on a peak to select it
- Ensure peak has detectable boundaries (local minima)
- Try zooming in for better selection


**For mathematical details**: See [METHODS.md](METHODS.md)  
**For installation help**: See [INSTALL.md](INSTALL.md)  
**For quick start**: See [README.md](README.md)

---


