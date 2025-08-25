#!/usr/bin/env python

import numpy as np
import argparse
from .claret import claret


def main():
    parser = argparse.ArgumentParser(description="retrieve limb-darkening coefficients for Kepler")
    parser.add_argument('--teff', help='effective temperature of the star -- Teff (Kelvin): mu,sigma', type=str)
    parser.add_argument('--logg', help='surface gravity of the star -- logg (cgs): mu,sigma', type=str, default=None)
    parser.add_argument('--feh', help='metallicity of the star -- [Fe/H] (dex): mu,sigma', type=str, default=None)
    parser.add_argument('--band', help='bandpass name', type=str, default='Kp')
    parser.add_argument('--law', help='limb-darkening law', type=str, default='quadratic')
    parser.add_argument('-n', '--nsamples', help='limb-darkening law', type=int, default=int(1e4))
    parser.add_argument('-t', '--transform', help='transform quadratic u-space to q-space', dest='transform', action='store_true')
    parser.set_defaults(transform=False)

    args = parser.parse_args()
    band = args.band
    nsamples = args.nsamples
    law = args.law
    transform = args.transform

    teff, uteff = map(float, args.teff.split(','))
    logg, ulogg = map(float, args.logg.split(','))
    feh, ufeh = map(float, args.feh.split(','))

    ld = claret(band, teff, uteff, logg, ulogg, feh, ufeh, n=nsamples, law=law, transform=transform)

    if law == 'linear':
        u, u_sig = ld
        print("u = {0:.4f} +/- {1:.4f}".format(u, u_sig))
    elif law == 'quadratic' or law == 'squareroot' or law == 'logarithmic':
        u1, u1_sig, u2, u2_sig = ld
        if transform:
            print("q1 = {0:.4f} +/- {1:.4f}".format(u1, u1_sig))
            print("q2 = {0:.4f} +/- {1:.4f}".format(u2, u2_sig))
        else:
            print("u1 = {0:.4f} +/- {1:.4f}".format(u1, u1_sig))
            print("u2 = {0:.4f} +/- {1:.4f}".format(u2, u2_sig))
    elif law == 'nonlinear':
        u1, u1_sig, u2, u2_sig, u3, u3_sig, u4, u4_sig = ld
        print("u1 = {0:.4f} +/- {1:.4f}".format(u1, u1_sig))
        print("u2 = {0:.4f} +/- {1:.4f}".format(u2, u2_sig))
        print("u3 = {0:.4f} +/- {1:.4f}".format(u3, u3_sig))
        print("u4 = {0:.4f} +/- {1:.4f}".format(u4, u4_sig))


if __name__ == "__main__":
    main()