"""
@author Micah Haack

width, length, and height here refer to the reactor internal

"""

from numpy import isin
from Cell import Cell
from Cell import FuelCell
from Cell import Moderator
from Cell import Reflector
from Cell import Shield
from Cell import Cooler
from Cell import Irradiator

class Reactor:

    def __init__(self, width, length, height, name='Reactor'):

        self.width = width
        self.length = length
        self.height = height

        self.output = 0
        self.efficiency = 0

        self.grid = [[[Cell for h in range(height)] for w in range(width)] for l in range(length)]
        
        self.name = name
        
    def printGrid(self):
        
        # print layers
        
        print('Reactor: ' + self.name)
        
        layerIndex = 0
        for layer in self.grid:
            
            print('============ LAYER ' + str(layerIndex) + ' ============')
            rowString = '  '
            for num in range(self.length):
                rowString += str(num)
                rowString += ' '
            print(rowString)
            
            rowNum = 0
            for row in layer:
                
                rowString = str(rowNum) + ' '
                for r in row:
                    if isinstance(r, FuelCell):
                        rowString += 'F '
                    elif isinstance(r, Moderator):
                        rowString += 'M '
                    elif isinstance(r, Reflector):
                        rowString += 'R '
                    elif isinstance(r, Shield):
                        rowString += 'S '
                    elif isinstance(r, Cooler):
                        rowString += 'C '
                    elif isinstance(r, Irradiator):
                        rowString += 'I '
                    else:
                        rowString += 'E '
                print(rowString)
                rowNum += 1
                
            layerIndex += 1