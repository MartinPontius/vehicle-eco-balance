import numpy as np


def calc_acceleration(speed, dt):
    """ Calculate acceleration from speed and time
    Parameters
    ----------
    speed: numpy array
       speed in km/h
    dt: numpy array
       sampling time in seconds
    Returns
    -------
    acceleration as numpy array
    """

    # Check if arrays are of same length
    if len(speed) != len(dt):
        print("Error")

    # Convert speed from km/h to m/s
    speed = speed / 3.6

    # Calculate acceleration
    acceleration = np.zeros(len(speed))
    for i in range(1, len(speed)):
        if dt[i] is not 0.0:
            acceleration[i] = ((speed[i] - speed[i-1]) / dt[i])

    return acceleration
