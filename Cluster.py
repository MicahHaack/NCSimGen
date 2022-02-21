
from Cell import FuelCell
from Cell import Cooler
from Cell import Conductor

class Cluster:
    
    def __init__(self):
        
        self.fuelCells = []
        self.coolers = []
        self.netHeat = 0
        
    def addCell(self, cell):
        
        if isinstance(cell, FuelCell):
            self.fuelCells.append(cell)
            self.updateHeat()
        elif isinstance(cell, Cooler):
            self.coolers.append(cell)
            self.updateHeat()
        else:
            return False
        
    def updateHeat(self):
        
        total = 0
        # sum total heat
        for fc in self.fuelCells:
            if fc.active:
                total += fc.adjacentModeratorLines * fc.fuel.heat
                
        # sum total cooling
        for cooler in self.coolers:
            if cooler.active:
                total -= cooler.cooling
                
        self.netHeat = total