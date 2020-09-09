from datetime import datetime
import numpy as np
import math


## Reqquired functions to calcilar the fuel consumption/CO2 emmisions

## Retrive elevation values from an open soure - up to 100000 values per day
# def generate_parms(one_track,s,e):
#     lats= list(one_track[s:e]['geometry'].y)
#     lngs = list(one_track[s:e]['geometry'].x)
#     track_coords = [c for c in zip(lats, lngs)]
#     format_str=list(map(lambda x : str(x[0])+','+str(x[1])+'|', track_coords))
#     concat_str = ''.join(format_str)
#     return concat_str
#
# def request(link):
#     elevation = req.request('GET',link)
#     results = elevation.json()['results']
#     h = list(map(lambda x : x['elevation'], results))
#     return h

def get_interval_time(time1, time2):
    """ Calculate time difference in seconds between two points in time

    Parameters
    time1: str
    time2: str
    Expected format is 2020-07-10T07:14:51
    """

    return abs(datetime.strptime(time1, '%Y-%m-%dT%H:%M:%S') -
               datetime.strptime(time2, '%Y-%m-%dT%H:%M:%S')).total_seconds()


def calc_efficiency(res, res_max, res_min, eff_max, eff_min):
    """ Estimate efficiency by linear interpolation """

    return np.interp(res, [res_min, res_max], [eff_min, eff_max])

