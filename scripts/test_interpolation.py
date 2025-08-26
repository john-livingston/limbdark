#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from limbdark.interpolator import LDInterpolator

# Initialize limb-darkening interpolator
ldi = LDInterpolator('T')

# Grid of Teff and logg
teff_vals = np.linspace(4500, 5500, 21)
logg_vals = np.linspace(4, 5, 21)
X, Y = np.meshgrid(teff_vals, logg_vals)

# Setup figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Initial computation
feh = 0.2
U, V = ldi(X, Y, feh)

# Display with imshow
im1 = ax1.imshow(U, origin='lower', extent=(4500, 5500, 4, 5), aspect='auto', cmap='viridis')
im2 = ax2.imshow(V, origin='lower', extent=(4500, 5500, 4, 5), aspect='auto', cmap='viridis')

# Configure axes
ax1.set_title(r"$u_1$")
ax1.set_xlabel(r"$T_\mathrm{eff}$")
ax1.set_ylabel(r"$\log g$")
ax2.set_title(r"$u_2$")
ax2.set_xlabel(r"$T_\mathrm{eff}$")
ax2.set_ylabel(r"$\log g$")

# Colorbars
cbar1 = fig.colorbar(im1, ax=ax1, orientation='vertical')
cbar2 = fig.colorbar(im2, ax=ax2, orientation='vertical')

plt.tight_layout()
plt.savefig('interpolation_test.png', dpi=150, bbox_inches='tight')
plt.close()
