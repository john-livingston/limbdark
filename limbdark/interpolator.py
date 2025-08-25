#!/usr/bin/env python
import numpy as np

from .util import get_interpolators


class LDInterpolator:

    def __init__(self, band, law='quadratic', kind='linear', cool=False):

        """
        band : photometric band. must be one of: B C H I J K Kp T R S1 S2 S3 S4 U V b g* i* r* u u* v y z*
        law : must be one of: linear quadratic squareroot logarithmic nonlinear
        cool : use True if band=='T' and Teff < 3500 (assumes Solar metallicity and using PHOENIX-COND models instead of the usual ATLAS models)
        """

        self.band = band
        self.law = law
        self.interpolators = get_interpolators(band, kind=kind, law=law, cool=cool)

    def __call__(self, teff, logg, feh):
        
        return [interp(teff, logg, feh) for interp in self.interpolators]