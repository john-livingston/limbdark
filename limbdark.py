#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd

def get_ld_rows(fp, band, teff, uteff, logg, ulogg):
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

def get_ld(fp, band, teff, uteff, logg, ulogg, median=True):

    df = get_ld_rows(fp, band, teff, uteff, logg, ulogg)
    u1, u2 = df.u1, df.u2

    if median:
        return np.median(u1), np.std(u1), np.median(u2), np.std(u2)

    return np.mean(u1), np.std(u1), np.mean(u2), np.std(u2)

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description="retrieve limb-darkening coefficients for Kepler")
    parser.add_argument('teff', help='effective temperature of the star (Teff) [Kelvin]', type=float)
    parser.add_argument('uteff', help='uncertainty in Teff', type=float)
    parser.add_argument('logg', help='surface gravity of the star (logg) [dex]', type=float, default=0)
    parser.add_argument('ulogg', help='uncertainty in logg', type=float, default=10)
    parser.add_argument('-b', '--band', help='the bandpass name: either kep or spz', type=str, default='kep')

    args = parser.parse_args()

    fp = 'claret2012_all.txt'
    if args.band == 'kep':
        df = get_ld_rows(fp, 'Kp', args.teff, args.uteff, args.logg, args.ulogg)
    elif args.band == 'spz':
        df = get_ld_rows(fp, 'S2', args.teff, args.uteff, args.logg, args.ulogg)

    print("number of models: {}".format(df.shape[0]))
    print("\tmin\tmean\tmax")
    print("temp:\t{0:.2f}\t{1:.2f}\t{2:.2f}".format(df.teff.min(), df.teff.mean(), df.teff.max()))
    print("logg:\t{0:.2f}\t{1:.2f}\t{2:.2f}".format(df.logg.min(), df.logg.mean(), df.logg.max()))
    print("feh:\t{0:.2f}\t{1:.2f}\t{2:.2f}".format(df.feh.min(), df.feh.mean(), df.feh.max()))
    print("-" * 10 + " limb-darkening coefficients " + "-" * 10)
    print("mean:   {0:.6f}, {1:.6f}".format(df.u1.mean(), df.u2.mean()))
    print("median: {0:.6f}, {1:.6f}".format(np.median(df.u1), np.median(df.u2)))
    print("std:    {0:.6f}, {1:.6f}".format(np.std(df.u1), np.std(df.u2)))
