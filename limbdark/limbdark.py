#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd

import pkg_resources
fp = pkg_resources.resource_filename(__name__, 'data/claret2012_all.txt')

def get_ld_df(band, teff, uteff, logg, ulogg, fp=fp):
    """
    Requires whitespace delimited table from:
    http://vizier.cfa.harvard.edu/viz-bin/VizieR-3?-source=J/A%2bA/546/A14
    """

    names = 'logg teff feh xi u1 u2 band method model'.split()
    df = pd.read_table(fp, names=names, delim_whitespace=True)

    idx = (df.teff <= teff + uteff) & (df.teff >= teff - uteff) &\
          (df.logg <= logg + ulogg) & (df.logg >= logg - ulogg) &\
          (df.band == band)

    return df.loc[idx]

def get_ld(band, teff, uteff, logg, ulogg, median=True, fp=fp):

    df = get_ld_rows(band, teff, uteff, logg, ulogg, fp)
    u1, u2 = df.u1, df.u2

    if median:
        return np.median(u1), np.std(u1), np.median(u2), np.std(u2)

    return np.mean(u1), np.std(u1), np.mean(u2), np.std(u2)
