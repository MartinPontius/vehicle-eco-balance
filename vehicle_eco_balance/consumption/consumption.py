import numpy as np
from ..utils import calc_efficiency


class Consumption:

    def __init__(self):
        self.consumption = 0.0
        self.consumption_aggr = 0.0
        self.g = 9.81  # gravitational acceleration in m/s²
        self.rho_air = 1.2  # air mass density in kg/m³
        self.efficiency = 0.0
        self.driving_resistance = 0.0
        self.power = 0.0

    def calculate_consumption(self, speed, acceleration, gradient_angle, vehicle, cr, **kwargs):
        """ Calculate consumption
        Parameters
        ----------
        :param vehicle:
        :param cr:
        :param gradient_angle: in radians
        :param speed: vehicle speed in km/h
        :type speed: numpy array
        :param acceleration: vehicle acceleration in m/s²
        :type acceleration: numpy array
        :param kwargs: efficiency

        Returns
        -------
        :return instantaneous consumption for each sampling point as numpy array
        """

        # TODO: check input type and convert lists to numpy arrays

        mass = vehicle.mass
        cw = vehicle.cw
        A = vehicle.A
        idle_power = vehicle.idle_power
        calorific_value = vehicle.calorific_value

        self.driving_resistance = driving_resistance = self._driving_resistance(speed/3.6, acceleration, gradient_angle, mass, A, cw, cr)

        efficiency = kwargs.get('efficiency', None)
        if efficiency is None:
            efficiency = calc_efficiency(driving_resistance, 2000, -2000, 0.4, 0.1)
        self.efficiency = efficiency

        self.power = power = self._calc_engine_power(speed/3.6, driving_resistance, idle_power)

        self.consumption = power / (calorific_value * efficiency)

        return self.consumption

    def _calc_engine_power(self, speed, driving_resistance, idle_power):
        """ Calculate engine power in kW """

        power = speed * driving_resistance / 1000
        return np.maximum(power, idle_power)

    def _driving_resistance(self, speed, acceleration, gradient_angle, mass, A, cw, cr):
        """ Calculate driving resistance in N """

        # TODO: check units?

        return self._aerodynamic_drag(speed, A, cw) \
               + self._rolling_resistance(gradient_angle, mass, cr) \
               + self._climbing_resistance(gradient_angle, mass) \
               + self._inertial_resistance(acceleration, mass)

    def _aerodynamic_drag(self, speed, A, cw):
        """ Calculate aerodynamic drag in N """
        return 0.5 * cw * A * self.rho_air * np.square(speed)

    def _rolling_resistance(self, gradient_angle, mass, cr):
        """ Calculate rolling resistance in N """
        return mass * self.g * cr * np.cos(gradient_angle)

    def _climbing_resistance(self, gradient_angle, mass):
        """ Calculate climbing resistance in N """
        return mass * self.g * np.sin(gradient_angle)

    def _inertial_resistance(self, acceleration, mass):
        """ Calculate inertial resistance in N """
        return mass * acceleration

    def aggregate(self):
        """ Sum consumption over time series """
        pass
