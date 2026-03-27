# Reference

## Supported bands

| Band | System | λ_eff (μm) | Δλ (μm) |
|------|--------|-----------|------------|
| U | Johnson | 0.365 | 0.066 |
| u | Stromgren | 0.350 | 0.030 |
| u\* | SDSS | 0.354 | 0.057 |
| B | Johnson | 0.440 | 0.094 |
| b | Stromgren | 0.467 | 0.018 |
| v | Stromgren | 0.411 | 0.019 |
| g\* | SDSS | 0.477 | 0.137 |
| V | Johnson | 0.550 | 0.088 |
| y | Stromgren | 0.547 | 0.023 |
| C | CoRoT | 0.600 | 0.300 |
| R | Cousins | 0.640 | 0.158 |
| r\* | SDSS | 0.623 | 0.137 |
| Kp | Kepler | 0.640 | 0.400 |
| I | Cousins | 0.790 | 0.154 |
| i\* | SDSS | 0.763 | 0.153 |
| T | TESS | 0.790 | 0.400 |
| z\* | SDSS | 0.913 | 0.095 |
| J | 2MASS | 1.25 | 0.162 |
| H | 2MASS | 1.65 | 0.251 |
| K | 2MASS | 2.16 | 0.262 |
| S1 | Spitzer/IRAC | 3.6 | 0.75 |
| S2 | Spitzer/IRAC | 4.5 | 1.01 |
| S3 | Spitzer/IRAC | 5.8 | 1.43 |
| S4 | Spitzer/IRAC | 8.0 | 2.91 |

## Supported laws

| Law | Coefficients | Formula |
|-----|-------------|---------|
| linear | u | I(μ) = 1 − u(1 − μ) |
| quadratic | u1, u2 | I(μ) = 1 − u1(1 − μ) − u2(1 − μ)² |
| squareroot | u1, u2 | I(μ) = 1 − u1(1 − μ) − u2(1 − √μ) |
| logarithmic | u1, u2 | I(μ) = 1 − u1(1 − μ) − u2 μ ln(μ) |
| nonlinear | u1, u2, u3, u4 | I(μ) = 1 − Σ uₖ(1 − μ^(k/2)) |

## References

- Claret, A. & Bloemen, S. 2011, A&A, 529, A75 — [ADS](https://ui.adsabs.harvard.edu/abs/2011A%26A...529A..75C)
- Claret, A. 2017, A&A, 600, A30 — [ADS](https://ui.adsabs.harvard.edu/abs/2017A%26A...600A..30C)
- Kipping, D. M. 2013, MNRAS, 435, 2152 — [ADS](https://ui.adsabs.harvard.edu/abs/2013MNRAS.435.2152K)
