#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd

import pkg_resources
fp = pkg_resources.resource_filename(__name__, 'data/claret_2011.csv')


def claret_ld_df(band, teff, uteff, logg, ulogg, feh=None, ufeh=None):

    """
    Uses table downloaded from:
    http://vizier.u-strasbg.fr/viz-bin/VizieR-3?-source=J/A%2bA/529/A75/table-af
    """

    df = pd.read_csv(fp)

    if feh is not None and ufeh is not None:
        idx = (df.teff <= teff + uteff) & (df.teff >= teff - uteff) &\
              (df.logg <= logg + ulogg) & (df.logg >= logg - ulogg) &\
              (df.feh <= feh + ufeh) & (df.feh >= feh - ufeh) &\
              (df.band == band)
    else:
        idx = (df.teff <= teff + uteff) & (df.teff >= teff - uteff) &\
              (df.logg <= logg + ulogg) & (df.logg >= logg - ulogg) &\
              (df.band == band)

    return df[idx]


def claret_ld(band, teff, uteff, logg, ulogg, feh=None, ufeh=None, median=True, verbose=True):

    """
    band must be one of: B C H I J K Kp R S1 S2 S3 S4 U V b g* i* r* u u* v y z*
    """

    df = claret_ld_df(band, teff, uteff, logg, ulogg, feh, ufeh)
    if df.shape[0] == 0:
        ff = 1
        while df.shape[0] == 0:
            df = claret_ld_df(band, teff, ff*uteff, logg, ff*ulogg, feh, ff*ufeh)
            ff += 0.1

    u1, u2 = df.u1, df.u2

    if verbose:
        print "Using {} models".format(df.shape[0])
        for key in "teff logg feh".split():
            print "{} range: {} - {}".format(key, df[key].min(), df[key].max())

    if median:
        return np.median(u1), np.std(u1), np.median(u2), np.std(u2)

    return np.mean(u1), np.std(u1), np.mean(u2), np.std(u2)
