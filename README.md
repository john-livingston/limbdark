# Limbdark

Limb darkening parameters from [Claret+2011](https://ui.adsabs.harvard.edu/?#abs/2011A%26A...529A..75C) and [Claret 2017](https://ui.adsabs.harvard.edu/?#abs/2017A%26A...600A..30C).

Uses Monte Carlo interpolation to propagate uncertainties in stellar parameters to uncertainties in limb darkening parameters for Bayesian transit analysis. The interpolation supports linear and nearest neighbor methods across the stellar parameter grid.

## Installation

```bash
pip install git+https://github.com/john-livingston/limbdark
```

## Supported Laws and Bands

**Laws:** linear, quadratic, square-root, logarithmic, nonlinear

**Bands:** B, C, H, I, J, K, Kp, T, R, S1, S2, S3, S4, U, V, b, g*, i*, r*, u, u*, v, y, z*
