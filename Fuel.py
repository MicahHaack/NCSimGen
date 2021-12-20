"""
@author Micah Haack

The goal of this object is to store all important
fuel type information in a single place for reference

fuelType is an enum, and is either
OX - Oxygen
NI - Nitrogen
ZA - Zirconium

TODO: Look into if we need to add a way to implement more 
of these

heat is in heat per tick
"""

from enum import Enum

class FuelType(Enum):
    OX = 'OX'
    NI = 'NI'
    ZA = 'ZA'

FT = FuelType


class Fuel:

    def __init__(self, 
    fuelType = FT.OX,
    name = 'TBU',
    efficiency = 125,
    heat = 40,
    criticality = 234,
    selfPriming = False):

        self.fuelType = fuelType
        self.name = name
        self.efficiency = efficiency
        self.heat = heat
        self.criticality = criticality
        self.selfPriming = selfPriming