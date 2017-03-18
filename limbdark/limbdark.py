#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import NearestNDInterpolator

import pkg_resources
_fp = pkg_resources.resource_filename(__name__, 'data/claret_2011.csv')


def claret(band, teff, uteff, logg, ulogg, feh, ufeh, n=int(1e4)):

    """
    Uses table downloaded from:
    http://vizier.u-strasbg.fr/viz-bin/VizieR-3?-source=J/A%2bA/529/A75/table-af

    band must be one of: B C H I J K Kp R S1 S2 S3 S4 U V b g* i* r* u u* v y z*
    """

    df = pd.read_csv(_fp)
    idx = df.band == band
    df = df[idx]

    points = df['teff logg feh'.split()].values
    values = df['u1 u2'.split()].values

    s_teff = teff + np.random.randn(n) * uteff
    s_logg = logg + np.random.randn(n) * ulogg
    s_feh = feh + np.random.randn(n) * ufeh

    # interp = LinearNDInterpolator(points, values)
    # res = interp(s_teff, s_logg, s_feh)
    # u1, u2 = np.median(res, axis=0)
    # u1_sig, u2_sig = res.std(axis=0)

    interp_u1 = NearestNDInterpolator(points, values.T[0], rescale=True)
    interp_u2 = NearestNDInterpolator(points, values.T[1], rescale=True)
    u1 = np.median(interp_u1(s_teff, s_logg, s_feh))
    u1_sig = np.std(interp_u1(s_teff, s_logg, s_feh))
    u2 = np.median(interp_u2(s_teff, s_logg, s_feh))
    u2_sig = np.std(interp_u2(s_teff, s_logg, s_feh))

    return u1, u1_sig, u2, u2_sig
