#!/usr/bin/env python
import os
import sys
import numpy as np
import pandas as pd
from scipy.interpolate import NearestNDInterpolator

import pkg_resources


def _get_df(band, law, cool=False):

    if band in "B C H I J K Kp R S1 S2 S3 S4 U V b g* i* r* u u* v y z*".split():

        fn = 'claret+2011_{}.csv.gz'.format(law)
        fp = pkg_resources.resource_filename(__name__, os.path.join('data', fn))
        df = pd.read_csv(fp)
        idx = df.band == band
        df = df[idx]

    elif band == "T":

        if cool:
            tablenums = dict(linear=13, quadratic=15, squareroot=17, logarithmic=19, nonlinear=21)
        else:
            tablenums = dict(linear=24, quadratic=25, squareroot=26, logarithmic=27, nonlinear=28)

        fn = 'claret_2017_table{}.csv.gz'.format(tablenums[law])
        fp = pkg_resources.resource_filename(__name__, os.path.join('data', fn))
        df = pd.read_csv(fp)

    return df


def u_to_q(u1, u2):
    """
    Maps limb-darkening u space to q space
    """
    q1 = (u1 + u2)**2
    q2 = u1 / (2 * (u1 + u2))
    return [q1, q2]


def claret(band, teff, uteff, logg, ulogg, feh, ufeh, n=int(1e4), law='quadratic', transform=False, verbose=True):

    """
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

    if band not in "B C H I J K Kp T R S1 S2 S3 S4 U V b g* i* r* u u* v y z*".split():
        raise(ValueError("band must be one of: B C H I J K Kp T R S1 S2 S3 S4 U V b g* i* r* u u* v y z*"))

    if law not in "linear quadratic squareroot logarithmic nonlinear".split():
        raise(ValueError("law must be one of: linear quadratic squareroot logarithmic nonlinear"))

    if band == 'T':
        cool = teff < 3500
        if cool and verbose:
            print("WARNING: Teff < 3500, assuming Solar metallicity and using PHOENIX-COND models instead of the usual ATLAS models")
        df = _get_df(band, law, cool)
    else:
        df = _get_df(band, law)

    points = df['teff logg feh'.split()].values

    s_teff = teff + np.random.randn(n) * uteff
    s_logg = logg + np.random.randn(n) * ulogg
    s_feh = feh + np.random.randn(n) * ufeh

    if law == 'linear':

        keys = 'u'
        values = df[keys].values
        interp_u = NearestNDInterpolator(points, values, rescale=True)
        u = np.median(interp_u(s_teff, s_logg, s_feh))
        u_sig = np.std(interp_u(s_teff, s_logg, s_feh))

        return u, u_sig

    elif law == 'quadratic' or law == 'squareroot' or law == 'logarithmic':

        keys = 'u1 u2'.split()
        if law == 'quadratic' and transform:
            values = df[keys].apply(lambda x: u_to_q(*x), axis=1).values
        else:
            values = df[keys].values
        interp_u1 = NearestNDInterpolator(points, values.T[0], rescale=True)
        interp_u2 = NearestNDInterpolator(points, values.T[1], rescale=True)
        u1 = np.median(interp_u1(s_teff, s_logg, s_feh))
        u1_sig = np.std(interp_u1(s_teff, s_logg, s_feh))
        u2 = np.median(interp_u2(s_teff, s_logg, s_feh))
        u2_sig = np.std(interp_u2(s_teff, s_logg, s_feh))

        return u1, u1_sig, u2, u2_sig

    elif law == 'nonlinear':

        keys = 'u1 u2 u3 u4'.split()
        values = df[keys].values
        interp_u1 = NearestNDInterpolator(points, values.T[0], rescale=True)
        interp_u2 = NearestNDInterpolator(points, values.T[1], rescale=True)
        interp_u3 = NearestNDInterpolator(points, values.T[2], rescale=True)
        interp_u4 = NearestNDInterpolator(points, values.T[3], rescale=True)
        u1 = np.median(interp_u1(s_teff, s_logg, s_feh))
        u1_sig = np.std(interp_u1(s_teff, s_logg, s_feh))
        u2 = np.median(interp_u2(s_teff, s_logg, s_feh))
        u2_sig = np.std(interp_u2(s_teff, s_logg, s_feh))
        u3 = np.median(interp_u3(s_teff, s_logg, s_feh))
        u3_sig = np.std(interp_u3(s_teff, s_logg, s_feh))
        u4 = np.median(interp_u4(s_teff, s_logg, s_feh))
        u4_sig = np.std(interp_u4(s_teff, s_logg, s_feh))

        return u1, u1_sig, u2, u2_sig, u3, u3_sig, u4, u4_sig
