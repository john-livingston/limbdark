# Usage

## Python API

The main function is `limbdark.claret()`:

```python
import limbdark as ld

# Quadratic limb darkening (default)
u1, u1_err, u2, u2_err = ld.claret(
    band='Kp',
    teff=5800, uteff=100,
    logg=4.44, ulogg=0.05,
    feh=0.0, ufeh=0.1
)
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `band` | Photometric band (see [Reference](reference.md)) |
| `teff`, `uteff` | Effective temperature and uncertainty [K] |
| `logg`, `ulogg` | Surface gravity and uncertainty [cgs] |
| `feh`, `ufeh` | Metallicity and uncertainty [dex] |
| `n` | Number of Monte Carlo samples (default: 100000) |
| `law` | Limb darkening law (default: `'quadratic'`) |
| `kind` | Interpolation method: `'nearest'` (default) or `'linear'` |
| `transform` | Transform quadratic (u1, u2) to Kipping (q1, q2) space (default: `False`) |

### Return values

Depends on the law:

- **linear**: `u, u_err`
- **quadratic/squareroot/logarithmic**: `u1, u1_err, u2, u2_err`
- **nonlinear**: `u1, u1_err, u2, u2_err, u3, u3_err, u4, u4_err`

### Kipping transform

For quadratic law, the [Kipping (2013)](https://arxiv.org/abs/1308.0009) reparameterization ensures uniform sampling in physically allowed parameter space:

```python
q1, q1_err, q2, q2_err = ld.claret(
    band='Kp', teff=5800, uteff=100,
    logg=4.44, ulogg=0.05,
    feh=0.0, ufeh=0.1,
    transform=True
)
```

## Command line

```bash
limbdark --teff 5800,100 --logg 4.44,0.05 --feh 0,0.1 --band Kp
```

Options:

- `--law` — limb darkening law (default: `quadratic`)
- `-n` — number of MC samples (default: 10000)
- `-t` / `--transform` — use Kipping transform
