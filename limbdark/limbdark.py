#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd

import pkg_resources
fp = pkg_resources.resource_filename(__name__, 'data/claret_2011.csv')


def get_ld_df(band, teff, uteff, logg, ulogg, feh=None, ufeh=None):

    """
    Table downloaded from:
    http://vizier.u-strasbg.fr/viz-bin/VizieR-3?-source=J/A%2bA/529/A75/table-af
    """

    df = pd.read_csv(fp)

    if feh is not None and ufeh is not None:
        idx = (df.teff <= teff + uteff) & (df.teff >= teff - uteff) &\
              (df.logg <= logg + ulogg) & (df.logg >= logg - ulogg) &\
              (df.mh <= feh + ufeh) & (df.mh >= feh - ufeh) &\
              (df.band == band)
    else:
        idx = (df.teff <= teff + uteff) & (df.teff >= teff - uteff) &\
              (df.logg <= logg + ulogg) & (df.logg >= logg - ulogg) &\
              (df.band == band)

    return df[idx]


def get_ld(band, teff, uteff, logg, ulogg, feh=None, ufeh=None, median=True):

    df = get_ld_df(band, teff, uteff, logg, ulogg, feh, ufeh)
    u1, u2 = df.a, df.b

    if median:
        return np.median(u1), np.std(u1), np.median(u2), np.std(u2)

    return np.mean(u1), np.std(u1), np.mean(u2), np.std(u2)
