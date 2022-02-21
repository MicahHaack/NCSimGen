from Fuel import Fuel

class Cell():

    def __init__(self, active = False):
        self.active = active

class FuelCell(Cell):

    def __init__(self, fuel, adjacentModeratorLines = 0):
        super().__init__()
        self.fuel = fuel
        self.adjacentModeratorLines = adjacentModeratorLines


class Cooler(Cell):

    def __init__(self, cooling, requirement):
        super().__init__()
        self.cooling = cooling
        self.requirement = requirement

class Moderator(Cell):
    
    def __init__(self, flux, efficiency):
        super().__init__()
        self.flux = flux
        self.efficiency = efficiency

class Reflector(Cell):

    def __init__(self, reflectivity, efficiency):
        super().__init__()
        self.reflectivity = reflectivity
        self.efficiency = efficiency

class Irradiator(Cell):

    def __init__(self, heat, efficiency):
        super().__init__()
        self.heat = heat
        self.efficiency = efficiency

class Shield(Cell):
    
    def __init__(self, heat, efficiency):
        super().__init__()
        self.heat = heat
        self.efficiency = efficiency

class Conductor(Cell):
    
    def __init__(self):
        pass