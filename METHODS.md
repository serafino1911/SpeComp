# Mathematical Methods in SpeComp

This document provides detailed mathematical descriptions of all comparison and processing methods used in SpeComp.

## Table of Contents
- [Comparison Algorithms](#comparison-algorithms)
- [Preprocessing Methods](#preprocessing-methods)
- [Filter Subtraction Methods](#filter-subtraction-methods)

---

## Comparison Algorithms

SpeComp implements seven different algorithms for comparing spectral data. Each algorithm has different strengths and is suited for different types of spectral analysis.

### 1. Normalized Correlation (NORM_CORR)

**Mathematical Definition:**

The normalized correlation coefficient (Pearson correlation) between two spectra $s_1(\lambda)$ and $s_2(\lambda)$ is:

$$r = \frac{\sum_{i=1}^{n} (s_1(\lambda_i) - \bar{s_1})(s_2(\lambda_i) - \bar{s_2})}{\sqrt{\sum_{i=1}^{n} (s_1(\lambda_i) - \bar{s_1})^2} \sqrt{\sum_{i=1}^{n} (s_2(\lambda_i) - \bar{s_2})^2}}$$

where:
- $s_1(\lambda_i)$ and $s_2(\lambda_i)$ are the intensity values at wavelength $\lambda_i$
- $\bar{s_1}$ and $\bar{s_2}$ are the mean values of each spectrum
- $n$ is the number of data points

**Output:** Absolute value $|r|$ ranging from 0 to 1
- **1** = perfect correlation
- **0** = no correlation

**Best for:** General spectral matching, identifying similar chemical compositions

---

### 2. Hit Quality Index (HQI)

**Mathematical Definition:**

The HQI metric is defined as:

$$\text{HQI} = \frac{(s_1 \cdot s_2)^2}{(s_1 \cdot s_1)(s_2 \cdot s_2)}$$

where $s_1 \cdot s_2$ represents the dot product:

$$s_1 \cdot s_2 = \sum_{i=1}^{n} s_1(\lambda_i) \cdot s_2(\lambda_i)$$

This can also be written as:

$$\text{HQI} = \left(\frac{\sum_{i=1}^{n} s_1(\lambda_i) s_2(\lambda_i)}{\sqrt{\sum_{i=1}^{n} s_1(\lambda_i)^2} \sqrt{\sum_{i=1}^{n} s_2(\lambda_i)^2}}\right)^2$$

**Output:** Value ranging from 0 to 1
- **1** = perfect match
- **0** = no similarity

**Best for:** Library matching in spectroscopy, emphasizing peak positions and relative intensities

---

### 3. Convolution (CONV)

**Mathematical Definition:**

The discrete convolution of two spectra is:

$$(s_1 \star s_2)[k] = \sum_{i=0}^{n-1} s_1[i] \cdot s_2[k-i]$$

The similarity metric is the maximum value:

$$\text{Similarity} = \max_k (s_1 \star s_2)[k]$$

For meaningful comparison, this is normalized by the self-convolution:

$$\text{Normalized Similarity} = \frac{\max(s_1 \star s_2)}{\max(s_1 \star s_1)}$$

**Output:** Normalized value, higher = better match

**Best for:** Detecting patterns that may be shifted or comparing peak shapes

---

### 4. FFT Convolution (FFT_CONV)

**Mathematical Definition:**

Uses the convolution theorem from Fourier analysis:

$$s_1 \star s_2 = \mathcal{F}^{-1}\{\mathcal{F}\{s_1\} \cdot \mathcal{F}\{s_2\}\}$$

where:
- $\mathcal{F}$ is the Fast Fourier Transform
- $\mathcal{F}^{-1}$ is the Inverse Fast Fourier Transform

Note: The spectrum is reversed ($s_2[::-1]$) to compute correlation instead of convolution.

The similarity metric is:

$$\text{Similarity} = \frac{\max|\mathcal{F}^{-1}\{\mathcal{F}\{s_1\} \cdot \mathcal{F}\{s_2^{rev}\}\}|}{\max|\mathcal{F}^{-1}\{\mathcal{F}\{s_1\} \cdot \mathcal{F}\{s_1\}\}|}$$

**Output:** Normalized value, higher = better match

**Best for:** Fast computation on large datasets (same result as CONV but faster)

---

### 5. Discrete Correlation (DISCR)

**Mathematical Definition:**

Identical to Normalized Correlation (uses `np.corrcoef`):

$$r = \frac{\text{cov}(s_1, s_2)}{\sigma_{s_1} \sigma_{s_2}}$$

where:
- $\text{cov}(s_1, s_2)$ is the covariance between the two spectra
- $\sigma_{s_1}$ and $\sigma_{s_2}$ are the standard deviations

**Output:** Absolute correlation coefficient $|r|$ from 0 to 1

**Best for:** Alternative correlation implementation, cross-validation with NORM_CORR

---

### 6. Correlate Correlation (CORRE)

**Mathematical Definition:**

Uses cross-correlation and integrates the result:

$$\text{Correlation}[k] = \sum_{i} s_1[i] \cdot s_2[i+k]$$

The similarity metric is the integral (area under curve):

$$\text{Similarity} = \int \text{Correlation}[k] \, dk \approx \sum_{k} \text{Correlation}[k]$$

Normalized by self-correlation:

$$\text{Normalized Similarity} = \frac{\int (s_1 \star s_2) dk}{\int (s_1 \star s_1) dk}$$

**Output:** Normalized integrated correlation value

**Best for:** Emphasizing overall spectral similarity including broad features

---

### 7. Difference Metric (DIFF)

**Mathematical Definition:**

Computes the normalized absolute difference:

$$\text{Difference} = \frac{1}{n} \sum_{i=1}^{n} |s_1(\lambda_i) - s_2(\lambda_i)|$$

This is the mean absolute error (MAE) between the two spectra.

**Output:** Value ≥ 0
- **0** = identical spectra
- **Higher values** = more different

**Note:** This metric is **reversed** - lower values indicate better matches.

**Best for:** Finding nearly identical spectra, quality control applications

---

## Preprocessing Methods

### Normalization Methods

#### MinMax Normalization

Scales all intensity values to the range [0, 1]:

$$s_{\text{norm}}(\lambda_i) = \frac{s(\lambda_i) - \min(s)}{\max(s) - \min(s)}$$

**Use when:** You want to compare spectral shapes regardless of absolute intensity.

#### Statistical Normalization (Z-score)

Standardizes data to have mean = 0 and standard deviation = 1:

$$s_{\text{norm}}(\lambda_i) = \frac{s(\lambda_i) - \mu_s}{\sigma_s}$$

where:
- $\mu_s = \frac{1}{n}\sum_{i=1}^{n} s(\lambda_i)$ is the mean
- $\sigma_s = \sqrt{\frac{1}{n}\sum_{i=1}^{n} (s(\lambda_i) - \mu_s)^2}$ is the standard deviation

**Use when:** You want to emphasize deviations from the mean intensity (experimental).

---

### Filtering Methods

#### Gaussian Filter

Applies a Gaussian smoothing kernel:

$$s_{\text{filtered}}(\lambda_i) = \sum_{j} w_j \cdot s(\lambda_{i+j})$$

where $w_j$ is the Gaussian weight:

$$w_j = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{j^2}{2\sigma^2}}$$

The window size determines the extent of smoothing (must be odd).

**Use when:** Reducing high-frequency noise while preserving peak shapes.

#### Baseline Correction (Savitzky-Golay)

Uses a Savitzky-Golay filter to estimate and remove baseline:

$$s_{\text{corrected}}(\lambda) = s(\lambda) - \text{Baseline}(\lambda)$$

The baseline is estimated using a polynomial fit in a sliding window:

$$\text{Baseline}[i] = \sum_{j=0}^{p} a_j \cdot i^j$$

where $p$ is the polynomial order (typically 3).

**Parameters:**
- `window_length`: Size of the smoothing window (must be odd)
- `polyorder`: Degree of polynomial used for fitting

**Use when:** Removing slow baseline drift or fluorescence background.

---

### Wavelength Range Selection

#### Inclusion Range

Only uses data within specified wavelength limits:

$$s_{\text{limited}}(\lambda) = \begin{cases} 
s(\lambda) & \text{if } \lambda_{\min} \leq \lambda \leq \lambda_{\max} \\
\text{excluded} & \text{otherwise}
\end{cases}$$

**Use when:** Focusing on diagnostic spectral regions.

#### Exclusion Zone

Removes data within specified wavelength limits:

$$s_{\text{masked}}(\lambda) = \begin{cases} 
\text{excluded} & \text{if } \lambda_{\text{ex,min}} \leq \lambda \leq \lambda_{\text{ex,max}} \\
s(\lambda) & \text{otherwise}
\end{cases}$$

**Use when:** Removing problematic regions (saturated peaks, artifacts, solvent bands).

---

## Filter Subtraction Methods

### Simple Subtract

Direct subtraction with floor at zero:

$$t(\lambda) = \max(0, s(\lambda) - b(\lambda))$$

where:
- $s(\lambda)$ = working spectrum
- $b(\lambda)$ = filter/background spectrum (interpolated to match working wavelength axis)
- $t(\lambda)$ = corrected spectrum

**Use when:** Background is a constant offset or simple additive component.

---

### Smart Subtract (Adaptive Weighted Subtraction)

Wavelength-dependent scaling using local least-squares optimization.

#### Mathematical Model

Assumes the observed spectrum is a linear combination:

$$s(\lambda) \approx t(\lambda) + \beta(\lambda) \cdot b(\lambda)$$

where:
- $s(\lambda)$ = observed spectrum (working file)
- $t(\lambda)$ = true sample spectrum (what we want to recover)
- $b(\lambda)$ = background/filter spectrum
- $\beta(\lambda)$ = wavelength-dependent scaling factor

#### Optimization Problem

For each wavelength $\lambda_0$, define a local window $W$ centered at $\lambda_0$ containing $2w+1$ points.

Find the optimal scaling factor $\beta(\lambda_0)$ that minimizes the squared residual:

$$\beta(\lambda_0) = \arg\min_{\beta} \sum_{\lambda \in W} [s(\lambda) - \beta \cdot b(\lambda)]^2$$

#### Analytical Solution

Taking the derivative with respect to $\beta$ and setting to zero:

$$\frac{\partial}{\partial \beta} \sum_{\lambda \in W} [s(\lambda) - \beta \cdot b(\lambda)]^2 = 0$$

$$-2 \sum_{\lambda \in W} b(\lambda)[s(\lambda) - \beta \cdot b(\lambda)] = 0$$

Solving for $\beta$:

$$\beta(\lambda_0) = \frac{\sum_{\lambda \in W} s(\lambda) \cdot b(\lambda)}{\sum_{\lambda \in W} b(\lambda)^2}$$

This is the local least-squares solution.

#### Smoothing Step

To reduce noise in the $\beta(\lambda)$ function, a Savitzky-Golay filter is applied:

$$\beta_{\text{smooth}}(\lambda) = \text{SavGol}(\beta(\lambda), \text{window}=51, \text{poly}=2)$$

#### Final Correction

The corrected spectrum is:

$$t(\lambda) = \max(0, s(\lambda) - \beta_{\text{smooth}}(\lambda) \cdot b(\lambda))$$

#### Parameters

- **Window size (W)**: Number of points on each side of $\lambda_0$ (default: all working spectrum, in this case $\beta(\lambda)$ is no longer $\lambda$ dipendent)
  - Small window: Better tracks rapid changes, more noise (min 25)
  - Large window: Smoother $\beta(\lambda)$, averages over features
  - Adjustable via input field in the GUI

**Use when:** Background contribution varies across the spectrum (e.g., wavelength-dependent fluorescence, varying baseline slopes).

---

### Manual Peak Editing

Interactive modification of individual peaks with smooth blending.

#### Peak Detection Algorithm

Starting from a clicked point $\lambda_c$, find peak boundaries by searching for local minima:

**Left boundary search:**
```
for λ from λ_c going left:
    if s(λ) < s(λ_left) or s(λ) < 1.1 × s(λ_left):
        λ_left = λ
    else:
        break
```

**Right boundary search:**
```
for λ from λ_c going right:
    if s(λ) < s(λ_right) or s(λ) < 1.1 × s(λ_right):
        λ_right = λ
    else:
        break
```

#### Smooth Scaling Algorithm

For a selected peak region $[\lambda_L, \lambda_R]$ with scaling factor $\alpha$:

1. **Baseline interpolation:** Define baseline at each point as linear interpolation:

$$B(\lambda) = s(\lambda_L) \cdot \frac{\lambda_R - \lambda}{\lambda_R - \lambda_L} + s(\lambda_R) \cdot \frac{\lambda - \lambda_L}{\lambda_R - \lambda_L}$$

2. **Blend factor:** Define smooth transition zones near edges with width $w_b = \min(5, \frac{\lambda_R - \lambda_L}{4})$:

$$\phi(\lambda) = \begin{cases}
\frac{\lambda - \lambda_L}{w_b} & \text{if } \lambda - \lambda_L < w_b \text{ (left edge)} \\
\frac{\lambda_R - \lambda}{w_b} & \text{if } \lambda_R - \lambda < w_b \text{ (right edge)} \\
1 & \text{otherwise (center)}
\end{cases}$$

3. **Apply scaled modification:**

$$s'(\lambda) = B(\lambda) + [s(\lambda) - B(\lambda)] \cdot [1 + (\alpha - 1) \cdot \phi(\lambda)]$$

4. **Ensure non-negative:**

$$s'(\lambda) = \max(0, s'(\lambda))$$

**Parameters:**
- $\alpha = 1.02$ for UP arrow (2% increase)
- $\alpha = 0.98$ for DOWN arrow (2% decrease)

**Effect:** Peak intensity changes smoothly with minimal discontinuity at boundaries.

---

## Algorithm Selection Guide

| Goal | Recommended Algorithms | Why |
|------|----------------------|-----|
| General library search | NORM_CORR, HQI | Fast, robust, well-established |
| Large database (>1000 spectra) | FFT_CONV | Computationally efficient |
| Exact matches | DIFF | Sensitive to small differences |
| Shifted or translated peaks | CONV, FFT_CONV | Translation-invariant |
| Broad feature comparison | CORRE | Integrates overall similarity |
| Cross-validation | Multiple algorithms | Different metrics for confidence |

---

## References

- Pearson Correlation: Pearson, K. (1895). "Notes on regression and inheritance in the case of two parents". *Proceedings of the Royal Society of London*, 58, 240–242.
- Savitzky-Golay Filter: Savitzky, A.; Golay, M.J.E. (1964). "Smoothing and Differentiation of Data by Simplified Least Squares Procedures". *Analytical Chemistry*, 36 (8): 1627–39.
- FFT Convolution: Cooley, James W.; Tukey, John W. (1965). "An algorithm for the machine calculation of complex Fourier series". *Mathematics of Computation*, 19 (90): 297–301.


