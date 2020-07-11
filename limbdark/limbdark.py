#!/usr/bin/env python
import numpy as np

from .util import get_interpolators, u_to_q

class LDInterpolator:

    def __init__(self, band, law='quadratic', cool=False):

        """
        band : photometric band. must be one of: B C H I J K Kp T R S1 S2 S3 S4 U V b g* i* r* u u* v y z*
        law : must be one of: linear quadratic squareroot logarithmic nonlinear
        cool : use True if band=='T' and Teff < 3500 (assumes Solar metallicity and using PHOENIX-COND models instead of the usual ATLAS models)
        """

        self.band = band
        self.law = law
        self.interpolators = get_interpolators(band, law=law, cool=cool)

    def __call__(self, teff, logg, feh):
        
        return [interp(teff, logg, feh) for interp in self.interpolators]

def claret(band, teff, uteff, logg, ulogg, feh, ufeh, 
    n=int(1e5), law='quadratic', transform=False):

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

    if law == 'linear':

        interp = LDInterpolator(band, law, cool)
        u = interp(s_teff, s_logg, s_feh)[0]
        return u.mean(), u.std()

    elif law == 'quadratic' or law == 'squareroot' or law == 'logarithmic':

        interp = LDInterpolator(band, law, cool)
        u1, u2 = interp(s_teff, s_logg, s_feh)
        if law == 'quadratic' and transform:
            q1, q2 = u_to_q(u1, u2)
            return q1.mean(), q1.std(), q2.mean(), q2.std()
        else:
            return u1.mean(), u1.std(), u2.mean(), u2.std()

    elif law == 'nonlinear':

        interp = LDInterpolator(band, law, cool)
        u1, u2, u3, u4 = interp(s_teff, s_logg, s_feh)
        return u1.mean(), u1.std(), u2.mean(), u2.std(), u3.mean(), u3.std(), u4.mean(), u4.std()
