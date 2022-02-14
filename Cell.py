
class Cell:

    def __init__():
        pass

class FuelCell(Cell):

    def __init__(self, fuel):
        super()
        self.fuel = fuel


class Cooler(Cell):

    def __init__(self, cooling, requirement):
        super()
        self.cooling = cooling
        self.requirement = requirement

class Moderator(Cell):
    
    def __init__(self, flux, efficiency):
        super()
        self.flux = flux
        self.efficiency = efficiency

class Reflector(Cell):

    def __init__(self, reflectivity, efficiency):
        super()
        self.reflectivity = reflectivity
        self.efficiency = efficiency

class Irradiator(Cell):

    def __init__(self, heat, efficiency):
        super()
        self.heat = heat
        self.efficiency = efficiency

class Shield(Cell):
    
    def __init__(self, heat, efficiency):
        super()
        self.heat = heat
        self.efficiency = efficiency

class Conductor(Cell):
    
    def __init__(self):
        super()