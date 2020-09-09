import numpy as np
from geopy import distance


def calc_gradient_angle(point1, point2):
    """ Calculate the gradient angle between two points on the earth's surface

    Parameters
    ----------
    :param point1: first coordinate
    :type point1: tuple (latitude, longitude, altitude)
    :param point2: second coordinate
    :type point2: tuple (latitude, longitude, altitude)

    Returns
    -------
    :return gradient angle in radians
    """

    coord1, alt1 = point1[:-1], point1[-1]
    coord2, alt2 = point2[:-1], point2[-1]

    dist = calc_distance(coord1, coord2)

    if dist != 0:
        return np.arctan((alt2 - alt1) / dist)
    else:
        return 0.0


def calc_distance(coord1, coord2, distance_type="geodetic", ellipsoid="WGS-84"):
    """ Calculate distance between two points on the earth's surface using geopy

    Great-circle distance is calculated using Vincenty's formula.
    Default ellipsoid of the geodetic distance is WGS-84.

    Parameters
    ----------
    :param coord1: first coordinate
    :type coord1: tuple (latitude, longitude)
    :param coord2: second coordinate
    :type coord2: tuple (latitude, longitude)
    :param distance_type: geodetic or great-circle (default geodetic)
    :type distance_type: str
    :param ellipsoid: ellipsoid for geodetic distance (default WGS-84)
    :type ellipsoid: str

    Returns
    -------
    :return distance in meters
    """

    if distance_type == "geodetic":
        return distance.geodesic(coord1, coord2, ellipsoid=ellipsoid).km * 1000
    elif distance_type == "great-circle":
        return distance.great_circle(coord1, coord2).km * 1000
    else:
        print("distance_type " + distance_type + " is unknown!")


def get_elevation():
    # loop through the dataframe and get the elevation from open source for each record in each routes
    for i in range(0, n):
        one_track_id = track_df['track.id'].unique()[i]
        one_track = track_df[track_df['track.id'] == one_track_id]
        # estimate the len of data
        batch = [int(len(one_track) / 100), len(one_track) % 100]
        elevation = []
        # get elevation
        for i in range(batch[0] + 1):
            # create requeest 100 parameter
            s = i * 100
            e = (i + 1) * 100
            if i < batch[0] + 1:
                --e
            else:
                e = e + batch[1]
            # check the parameters (s) not excced the lenght of the track
            if s >= len(one_track):
                break
            # creat the request
            parms = generate_parms(one_track, s, e)
            # send the request and get the results
            access = url + parms
            part = request(access)
            if part == None:
                part = [np.nan] * (e + 1 - s)
            # put the results in a list
            elevation.extend(part)
            time.sleep(1)
        one_track['elevation'] = elevation
        # Filterout the null value and use GPS altitude to fill them
        temp = one_track[one_track['elevation'].isnull() == True]
        if len(temp) > 0:
            for i in temp.index:
                one_track.loc[i, 'elevation'] = one_track.loc[i, 'GPS Altitude.value']


def get_cr():
    # Match the graph with osm and get maxspeed & surface attriubutes
    ox.settings.useful_tags_way = ["maxspeed", "surface"]
    for i in one_track.index:
        lat = one_track.loc[i, 'geometry'].y
        lng = one_track.loc[i, 'geometry'].x
        x = (ox.get_nearest_edge(G, (lat, lng)))
        p = [x[0], x[1]]
        a = ox.utils_graph.get_route_edge_attributes(G, p)
        dic = a[0]
        # check if the edge has maximum speed value if not then use the value of previous point
        if "maxspeed" in dic:
            one_track.loc[i, "maxspeed"] = dic["maxspeed"]
        else:
            if i > 0:
                m = one_track.loc[i - 1, "maxspeed"]
                one_track.loc[i, "maxspeed"] = m

        # check if the edge has a surface value, if not then use the value of previous point
        if "surface" in dic:
            one_track.loc[i, "surface"] = dic["surface"]
        else:
            if i > 0:
                s = one_track.loc[i - 1, "surface"]
                one_track.loc[i, "surface"] = s

        # get the rolling resistance cofficient
        if one_track.loc[i, 'surface'] == "asphalt":
            one_track.loc[i, 'rolling_resistance'] = 0.02  # source: engineeringtoolbox.com
        elif one_track.loc[i, 'surface'] == "cobblestone":
            one_track.loc[i, 'rolling_resistance'] = 0.015  # source: engineeringtoolbox.com
        elif one_track.loc[i, 'surface'] == "paving_stones":
            one_track.loc[i, 'rolling_resistance'] = 0.033  # source: The Automotive Chassis book
        else:
            one_track.loc[i, 'rolling_resistance'] = 0.02
