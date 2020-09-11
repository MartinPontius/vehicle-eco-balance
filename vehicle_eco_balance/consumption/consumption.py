import numpy as np
from ..utils import calc_efficiency


class Consumption:
    """ Consumption

    Parameters
    ----------
    consumption_type: str
        'energy' or 'fuel'

    Attributes
    ----------
    consumption : numpy array
        consumption in l/h if consumption_type is 'fuel' and in kW if consumption_type is 'energy'
    consumption_aggr: float
        aggregated consumption in l if consumption_type is 'fuel' and in kWh if consumption_type is 'energy'
    driving_resistance: numpy array
        driving resistance in N
    power: numpy array
        power in kW
    efficiency: numpy array
        efficiency (dimensionless)
    g: float
        gravitational acceleration in m/s²
    rho_air: float
        air mass density in kg/m³
    """

    def __init__(self, consumption_type):
        self.consumption = None
        self.consumption_aggr = None
        self.g = 9.81
        self.rho_air = 1.2
        self.efficiency = None
        self.driving_resistance = None
        self.power = None
        self.consumption_type = consumption_type

    def calculate_consumption(self, speed, acceleration, gradient_angle, vehicle, cr, **kwargs):
        """ Calculate energy/fuel consumption

        Parameters
        ----------
        vehicle : class Vehicle
            vehicle containing parameters like mass, air drag coefficient, etc.
        cr: float or numpy array
            rolling resistance coefficient
        gradient_angle: numpy array
            gradient angle (of the road) in radians
        speed: numpy array
            vehicle speed in km/h
        acceleration: numpy array
            vehicle acceleration in m/s²
        kwargs: dictionary
            efficiency: float or numpy array

        Returns
        -------
        self.consumption: numpy array
            instantaneous consumption for each sampling point (in l/h if consumption_type is 'fuel', in kW if consumption_type is 'energy')
        """

        # TODO: check input type and convert lists to numpy arrays?
        # TODO: check units?
        # TODO: check NaN?

        if len(speed) != len(acceleration) or len(speed) != len(gradient_angle) or len(acceleration) != len(gradient_angle):
            raise Exception("The arrays speed, acceleration and gradient_angle must have the same length!")

        # Extract parameters from vehicle
        mass = vehicle.mass
        cw = vehicle.cw
        A = vehicle.A
        idle_power = vehicle.idle_power
        calorific_value = vehicle.calorific_value
        fuel_type = vehicle.fuel_type

        self.driving_resistance = self._driving_resistance(speed/3.6, acceleration, gradient_angle, mass, A, cw, cr)

        efficiency = kwargs.get('efficiency', None)
        if efficiency is None:
            efficiency = calc_efficiency(self.driving_resistance, 2000, -2000, 0.4, 0.1)
        self.efficiency = efficiency

        self.power = self._calc_engine_power(speed/3.6, self.driving_resistance, idle_power, fuel_type)
        if self.consumption_type == 'energy':
            self.consumption = self.power / efficiency
        else:
            self.consumption = self.power / (calorific_value * efficiency)

        return self.consumption

    def _calc_engine_power(self, speed, driving_resistance, idle_power, fuel_type):
        """ Calculate engine power in kW """

        power = speed * driving_resistance / 1000
        # Allow negative consumption for electric cars
        if fuel_type == 'electric':
            return power
        else:
            return np.maximum(power, idle_power)

    def _driving_resistance(self, speed, acceleration, gradient_angle, mass, A, cw, cr):
        """ Calculate driving resistance in N """

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

    def aggregate(self, dt):
        """ Sum instantaneous consumption values

        Parameters
        ----------
        dt : numpy array
            interval times between measurements

        Returns
        -------
        self.consumption_aggr:
            aggregated consumption (in l if consumption_type is 'fuel', in kWh if consumption_type is 'energy')
        """

        self.consumption_aggr = np.sum(self.consumption * dt / 3600)
        # equation is applicable for both consumption types:
        # units: kW * s = kW * 1/3600 h = kWh / 3600
        # units: l/h * s = l/(3600 s) * s = l / 3600

        return self.consumption_aggr
