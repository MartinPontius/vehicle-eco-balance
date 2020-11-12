import numpy as np
from vehicle_eco_balance.utils import calc_efficiency


class ConsumptionPhys:
    """ Physical (load-based) consumption model.
    It is based on "Stefan Pischinger und Ulrich Seiffert. Vieweg Handbuch Kraftfahrzeugtechnik. Springer, 2016." (page 62)

    Parameters
    ----------
    consumption_type: str
        'energy' or 'fuel'
    g¹: float
        gravitational acceleration in m/s² (default 9.81)
    rho_air²: float
        air mass density in kg/m³ (default 1.225)


    Attributes
    ----------
    consumption_type: str
        'energy' or 'fuel'
    consumption : numpy array
        consumption in l/h if consumption_type is 'fuel' and in kW if consumption_type is 'energy'
    power: numpy array
        power in kW
    driving_resistance: numpy array
        driving resistance in N
    efficiency: numpy array
        efficiency (dimensionless)
    g¹: float
        gravitational acceleration in m/s² (default 9.81)
    rho_air²: float
        air mass density in kg/m³ (default 1.225)

    References for default values:
    ¹ Martin Treiber and Arne Kesting. “Traffic flow dynamics.” In: Traffic Flow Dynamics: Data, Models and Simulation,
      Springer-Verlag Berlin Heidelberg (2013). Page 395.
    ² Stefan Pischinger und Ulrich Seiffert. Vieweg Handbuch Kraftfahrzeugtechnik. Springer, 2016. Page 63.
    """

    def __init__(self, consumption_type, g=9.81, rho_air=1.225):
        self.consumption_type = consumption_type
        self.consumption = None
        self.power = None
        self.driving_resistance = None
        self.efficiency = None
        self.g = g
        self.rho_air = rho_air

    def calculate_consumption(self, speed, acceleration, gradient_angle, vehicle, cr=0.02, **kwargs):
        """ Calculate energy/fuel consumption

        Parameters
        ----------
        speed: numpy array
            vehicle speed in km/h
        acceleration: numpy array
            vehicle acceleration in m/s²
        gradient_angle: numpy array
            gradient angle (of the road) in radians
        vehicle : class Vehicle
            vehicle containing parameters like mass, air drag coefficient, etc.
        cr¹: float or numpy array
            rolling resistance coefficient (default 0.02)
        kwargs: dictionary
            efficiency: float or numpy array

        Returns
        -------
        self.consumption: numpy array
            instantaneous consumption for each sampling point (in l/h if consumption_type is 'fuel', in kW if consumption_type is 'energy')

        References for default values:
        ¹ Martin Treiber and Arne Kesting. “Traffic flow dynamics.” In: Traffic Flow Dynamics: Data, Models and Simulation,
          Springer-Verlag Berlin Heidelberg (2013). Page 395.
        """

        # TODO: check input type and convert lists to numpy arrays?
        # TODO: check units?
        # TODO: check NaN?

        if len(speed) != len(acceleration) or len(speed) != len(gradient_angle) or len(acceleration) != len(
                gradient_angle):
            raise Exception("The arrays speed, acceleration and gradient_angle must have the same length!")

        # Extract parameters from vehicle
        mass = vehicle.mass
        cw = vehicle.cw
        cross_section = vehicle.cross_section
        idle_power = vehicle.idle_power
        calorific_value = vehicle.calorific_value
        fuel_type = vehicle.fuel_type
        min_efficiency = vehicle.min_efficiency
        max_efficiency = vehicle.max_efficiency

        self.driving_resistance = self._driving_resistance(speed / 3.6, acceleration, gradient_angle, mass, cross_section, cw, cr)

        efficiency = kwargs.get('efficiency', None)
        if efficiency is None:
            efficiency = calc_efficiency(self.driving_resistance, -2000, 2000, min_efficiency, max_efficiency)
        self.efficiency = efficiency

        self.power = self._calc_engine_power(speed / 3.6, self.driving_resistance, idle_power, fuel_type)
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

    def _driving_resistance(self, speed, acceleration, gradient_angle, mass, cross_section, cw, cr):
        """ Calculate driving resistance in N """

        return self._aerodynamic_drag(speed, cross_section, cw) \
               + self._rolling_resistance(gradient_angle, mass, cr) \
               + self._climbing_resistance(gradient_angle, mass) \
               + self._inertial_resistance(acceleration, mass)

    def _aerodynamic_drag(self, speed, cross_section, cw):
        """ Calculate aerodynamic drag in N """
        return 0.5 * cw * cross_section * self.rho_air * np.square(speed)

    def _rolling_resistance(self, gradient_angle, mass, cr):
        """ Calculate rolling resistance in N """
        return mass * self.g * cr * np.cos(gradient_angle)

    def _climbing_resistance(self, gradient_angle, mass):
        """ Calculate climbing resistance in N """
        return mass * self.g * np.sin(gradient_angle)

    def _inertial_resistance(self, acceleration, mass):
        """ Calculate inertial resistance in N """
        return mass * acceleration


class ConsumptionStat:
    """ Statistical consumption model.

    consumption = a + b * speed^3 + c * speed * cos(grad_angle) + d * speed * sin(grad_angle) + e * speed * acceleration

    Parameters
    ----------
    a : float
        first coefficent (default 1.41)
    b : float
        second coefficent (default 0.000134)
    c : float
        third coefficent (default 0.0670)
    d : float
        fourth coefficent (default 1.90)
    e : float
        fifth coefficent (default 0.197)

    Attributes
    ----------
    consumption : numpy array
        consumption in l/h
    idle_consumption: float
        idle consumption in l (default 1.5)
    a : float
        first coefficent (default 1.41)
    b : float
        second coefficent (default 0.000134)
    c : float
        third coefficent (default 0.0670)
    d : float
        fourth coefficent (default 1.90)
    e : float
        fifth coefficent (default 0.197)

    """

    def __init__(self, a=1.41, b=0.000134, c=0.0670, d=1.90, e=0.197, idle_consumption=1.5):
        self.consumption = None
        self.idle_consumption = idle_consumption
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def calculate_consumption(self, speed, acceleration, gradient_angle):
        """ Calculate fuel consumption

        Parameters
        ----------
        gradient_angle: numpy array
            gradient angle (of the road) in radians
        speed: numpy array
            vehicle speed in km/h
        acceleration: numpy array
            vehicle acceleration in m/s²

        Returns
        -------
        self.consumption: numpy array
            instantaneous consumption for each sampling point in l/h
        """

        self.consumption = self.a + self.b * np.power(speed / 3.6, 3) + self.c * speed / 3.6 * np.cos(gradient_angle) + \
                           self.d * speed / 3.6 * np.sin(gradient_angle) + self.e * speed / 3.6 * acceleration

        self.consumption = np.maximum(self.consumption, self.idle_consumption)

        return self.consumption


def accumulate_consumption(consumption, dt):
    """ Sum instantaneous consumption values over a whole track

    Parameters
    ----------
    consumption : numpy array
        instantaneous consumption in l/h or kW
    dt : numpy array
        interval times between measurements

    Returns
    -------
    accumulated consumption in l or kWh depending on input
    """

    # equation is applicable for both consumption types:
    # units: kW * s = kW * 1/3600 h = kWh / 3600
    # units: l/h * s = l/(3600 s) * s = l / 3600
    return np.sum(consumption * dt / 3600)


def consumption_per100km(consumption, dt, distance):
    """ Sum instantaneous consumption values over a whole track

    Parameters
    ----------
    consumption : numpy array
        instantaneous consumption in l/h or kW
    dt : numpy array
        interval times between measurements
    distance: float
        total trajectory distance in km

    Returns
    -------
    accumulated consumption in l or kWh depending on input
    """

    return 100 * accumulate_consumption(consumption, dt) / distance
