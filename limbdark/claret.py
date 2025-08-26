#!/usr/bin/env python
import numpy as np

from .util import u_to_q
from .interpolator import LDInterpolator


def claret(band, teff, uteff, logg, ulogg, feh, ufeh, n=int(1e5), law='quadratic', kind='nearest', transform=False):

    """
    Estimates limb darkening from stellar parameters and their 
    associated uncertainties, based on: 
    Claret+2011 (https://ui.adsabs.harvard.edu/abs/2011A%26A...529A..75C/abstract)
    Claret+2017 (https://ui.adsabs.harvard.edu/abs/2017A%26A...600A..30C/abstract)

    band : photometric band. must be one of: B C H I J K Kp T R S1 S2 S3 S4 U V b g* i* r* u u* v y z*
    teff : stellar effective temperature [K]
    uteff : uncertainty in stellar effective temperature [K]
    logg : stellar surface gravity [cgs]
    ulogg : uncertainty in stellar surface gravity [cgs]
    feh : metallicity [dex]
    ufeh : uncertainty in metallicity [dex]
    n : Number of onte Carlo samples (optional, default is 10000)
    law : limb darkening law (optional, default is quadratic) must be one of: linear quadratic squareroot logarithmic nonlinear
    transform : transform quadratic limb darkening parameters to q-space (optional, default is False), see https://arxiv.org/abs/1308.0009

    All bands come from Claret+2011, except for T (TESS), which comes from Claret 2017.

    Uses tables downloaded from:
    http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=J%2FA%2BA%2F529%2FA75
    http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=J%2FA%2BA%2F600%2FA30
    """

    if band == 'T' and teff < 3500:
        print("Teff < 3500: assuming Solar metallicity and using PHOENIX-COND models instead of the usual ATLAS models")
        cool = True
    else:
        cool = False

    s_teff = teff + np.random.randn(n) * uteff
    s_logg = logg + np.random.randn(n) * ulogg
    s_feh = feh + np.random.randn(n) * ufeh

    interp = LDInterpolator(band, law=law, kind=kind, cool=cool)

    if law == 'linear':

        u = interp(s_teff, s_logg, s_feh)[0]
        return np.nanmean(u), np.nanstd(u)

    elif law == 'quadratic' or law == 'squareroot' or law == 'logarithmic':

        u1, u2 = interp(s_teff, s_logg, s_feh)
        if law == 'quadratic' and transform:
            q1, q2 = u_to_q(u1, u2)
            return [val for u in [q1, q2] for val in [np.nanmean(u), np.nanstd(u)]]
        else:
            return [val for u in [u1, u2] for val in [np.nanmean(u), np.nanstd(u)]]

    elif law == 'nonlinear':

        u1, u2, u3, u4 = interp(s_teff, s_logg, s_feh)
        return [val for u in [u1, u2, u3, u4] for val in [np.nanmean(u), np.nanstd(u)]]