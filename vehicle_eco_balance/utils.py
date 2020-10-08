from datetime import datetime
import numpy as np


def get_interval_time(time1, time2):
    """ Calculate time difference in seconds between two points in time

    Parameters
    ----------
    time1: str
    time2: str
    Expected format is 2020-07-10T07:14:51

    Returns
    -------
    dt: float
        absolute time difference in seconds
    """

    return abs(datetime.strptime(time1, '%Y-%m-%dT%H:%M:%S') -
               datetime.strptime(time2, '%Y-%m-%dT%H:%M:%S')).total_seconds()


def calc_efficiency(res, res_min, res_max, eff_min, eff_max):
    """ Estimate efficiency by linear interpolation

    Parameters
    ----------
    res: numpy array
        driving resistance
    res_min: float
        minimum driving resistance for interpolation
    res_max: float
        maximum driving resistance for interpolation
    eff_min: float
        minimum efficiency for interpolation
    eff_max: float
        maximum efficiency for interpolation

    Returns
    -------
    efficiency: numpy array
        interpolated efficiency
    """

    return np.interp(res, [res_min, res_max], [eff_min, eff_max])

