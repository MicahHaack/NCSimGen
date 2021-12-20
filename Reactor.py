"""
@author Micah Haack

width, length, and height here refer to the reactor internal

"""

from Cell import Cell
from Cell import FuelCell
from Cell import Moderator
from Cell import Reflector
from Cell import Shield
from Cell import Cooler
from Cell import Irradiator

class Reactor:

    def __init__(self, width, length, height):

        self.width = width
        self.length = length
        self.height = height

        self.output = 0
        self.efficiency = 0

        self.grid = [[[Cell for h in range(height)] for w in range(width)] for l in range(length)]
        