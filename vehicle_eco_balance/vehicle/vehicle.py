fuel_types = {
    'electric': {
        'calorific_value': None
    },
    'gasoline': {
        'calorific_value': 8.8
    },
    'diesel': {
        'calorific_value': 9.9
    }
}


class Vehicle:
    def __init__(self, mass):
        self.mass = mass


class Car(Vehicle):
    def __init__(self, mass=1500, car_cross_sectional=2.6, air_drag_coefficient=0.3, fuel_type='gasoline', idle_power=2):
        super().__init__(mass)
        self.fuel_type = fuel_type
        self.A = car_cross_sectional    # in m²
        self.cw = air_drag_coefficient  # dimensionless
        self.calorific_value = fuel_types.get(self.fuel_type).get('calorific_value')  # in kWh/l
        self.idle_power = idle_power    # in kW


class Airplane(Vehicle):
    pass


class Ship(Vehicle):
    pass
