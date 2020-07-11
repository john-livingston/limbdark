import os
import pandas as pd
from scipy.interpolate import NearestNDInterpolator
import pkg_resources

BANDS = "B C H I J K Kp T R S1 S2 S3 S4 U V b g* i* r* u u* v y z*".split()
LAWS = "linear quadratic squareroot logarithmic nonlinear".split()


def u_to_q(u1, u2):

    """
    Maps limb-darkening u space to q space
    see https://arxiv.org/abs/1308.0009
    """

    q1 = (u1 + u2)**2
    q2 = u1 / (2 * (u1 + u2))

    return [q1, q2]


def get_df(band, law, cool=False):

    if band == "T":

        if cool:
            tablenums = dict(linear=13, quadratic=15, squareroot=17, logarithmic=19, nonlinear=21)
        else:
            tablenums = dict(linear=24, quadratic=25, squareroot=26, logarithmic=27, nonlinear=28)

        fn = 'claret_2017_table{}.csv.gz'.format(tablenums[law])
        fp = pkg_resources.resource_filename(__name__, os.path.join('data', fn))
        df = pd.read_csv(fp)

    elif band in BANDS:

        fn = 'claret+2011_{}.csv.gz'.format(law)
        fp = pkg_resources.resource_filename(__name__, os.path.join('data', fn))
        df = pd.read_csv(fp)
        idx = df.band == band
        df = df[idx]

    return df


def get_interpolators(band, law='quadratic', cool=False, verbose=False):

    if band not in BANDS:
        raise(ValueError(f"band must be one of: {' '.join(BANDS)}"))

    if law not in LAWS:
        raise(ValueError(f"law must be one of: {' '.join(LAWS)}"))

    df = get_df(band, law, cool=cool)

    points = df['teff logg feh'.split()].values

    if law == 'linear':
        keys = 'u'
        values = df[keys].values
        interp = NearestNDInterpolator(points, values, rescale=True)
        return [interp]

    elif law == 'quadratic' or law == 'squareroot' or law == 'logarithmic':
        keys = 'u1 u2'.split()
        values = df[keys].values
        interp_u1 = NearestNDInterpolator(points, values.T[0], rescale=True)
        interp_u2 = NearestNDInterpolator(points, values.T[1], rescale=True)
        return [interp_u1, interp_u2]

    elif law == 'nonlinear':
        keys = 'u1 u2 u3 u4'.split()
        values = df[keys].values
        interp_u1 = NearestNDInterpolator(points, values.T[0], rescale=True)
        interp_u2 = NearestNDInterpolator(points, values.T[1], rescale=True)
        interp_u3 = NearestNDInterpolator(points, values.T[2], rescale=True)
        interp_u4 = NearestNDInterpolator(points, values.T[3], rescale=True)
        return [interp_u1, interp_u2, interp_u3, interp_u4]
