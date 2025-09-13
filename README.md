# Limbdark

Limb darkening parameters from [Claret+2011](https://ui.adsabs.harvard.edu/?#abs/2011A%26A...529A..75C) and [Claret 2017](https://ui.adsabs.harvard.edu/?#abs/2017A%26A...600A..30C).

Uses Monte Carlo interpolation to propagate uncertainties in stellar parameters to uncertainties in limb darkening parameters for Bayesian transit analysis. The interpolation supports linear and nearest neighbor methods across the stellar parameter grid.

## Installation

```bash
pip install git+https://github.com/john-livingston/limbdark
```

## Usage

### Command Line

```bash
limbdark --teff 4970,120 --logg 4.25,0.03 --feh 0,0.2 --band Kp
```

### Python

```python
import limbdark as ld

# Get quadratic limb darkening parameters for Kepler band
u1_mean, u1_std, u2_mean, u2_std = ld.claret(
    band='Kp',
    teff=4970, uteff=120,
    logg=4.25, ulogg=0.03,
    feh=0.0, ufeh=0.2,
    law='quadratic'
)

print(f"u1 = {u1_mean:.4f} ± {u1_std:.4f}")
print(f"u2 = {u2_mean:.4f} ± {u2_std:.4f}")
```

## Supported Laws and Bands

**Laws:** linear, quadratic, square-root, logarithmic, nonlinear

**Bands:** B, C, H, I, J, K, Kp, T, R, S1, S2, S3, S4, U, V, b, g*, i*, r*, u, u*, v, y, z*
