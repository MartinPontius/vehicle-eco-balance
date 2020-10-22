fuel_types = {
    'electric': {
        'calorific_value': None,
        'min_efficiency': 0.9,
        'max_efficiency': 0.9
    },
    'gasoline': {
        'calorific_value': 8.8,
        'min_efficiency': 0.1,
        'max_efficiency': 0.4
    },
    'diesel': {
        'calorific_value': 9.9,
        'min_efficiency': 0.1,
        'max_efficiency': 0.43
    }
}


class Vehicle:
    def __init__(self, mass):
        self.mass = mass


class Car(Vehicle):
    def __init__(self, mass=1500, car_cross_section=2.6, air_drag_coefficient=0.3, fuel_type='gasoline', idle_power=2):
        super().__init__(mass)
        self.fuel_type = fuel_type
        self.A = car_cross_section      # in m²
        self.cw = air_drag_coefficient  # dimensionless
        self.calorific_value = fuel_types.get(self.fuel_type).get('calorific_value')  # in kWh/l
        self.idle_power = idle_power    # in kW
        self.min_efficiency = fuel_types.get(self.fuel_type).get('min_efficiency')
        self.max_efficiency = fuel_types.get(self.fuel_type).get('max_efficiency')

    def __str__(self):
        return "Car properties: \n fuel_type: {} \n A: {} \n cw: {} \n calorific_value: {} \n idle_power: {} \n min_efficiency: {} \n max_efficiency: {}".format(
            self.fuel_type, self.A, self.cw, self.calorific_value, self.idle_power, self.min_efficiency, self.max_efficiency)

class Airplane(Vehicle):
    pass


class Ship(Vehicle):
    pass
