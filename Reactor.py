"""
@author Micah Haack

width, length, and height here refer to the reactor internal

"""

import numpy as np
from sklearn import cluster
from zmq import curve_keypair

from Cell import Cell
from Cell import FuelCell
from Cell import Moderator
from Cell import Reflector
from Cell import Shield
from Cell import Cooler
from Cell import Irradiator
from Cell import Conductor

class Reactor:

    def __init__(self, rows, cols, height, name='Reactor'):

        self.rows = rows
        self.cols = cols
        self.height = height

        self.output = 0
        self.efficiency = 0

        self.grid = [[[Cell for h in range(height)] for w in range(rows)] for l in range(cols)]
        
        self.name = name
    
    def iterClusterSearch(self, layerNum, rowNum, cellNum, visited):
        
        # check current bounds to see if we hit a wall
        if layerNum <= -1 or layerNum >= self.height:
            return True
        if rowNum <= -1 or rowNum >= self.rows:
            return True
        if cellNum <= -1 or cellNum >= self.cols:
            return True
        
        # if we have visited this already return false and exit
        if visited[layerNum][rowNum][cellNum]:
            return False
        
        # otherwise, at current position, change visited state to True
        visited[layerNum][rowNum][cellNum] = True
        
        cell = self.grid[layerNum][rowNum][cellNum]
        
        foundWall = False
        # check current location and see if it is a valid cluster component
        if isinstance(cell, FuelCell) or isinstance(cell, Conductor) or isinstance(cell, Cooler):
            
            # if so search the surrounding cells, if any hit a wall record that
            
            if self.iterClusterSearch(layerNum + 1, rowNum, cellNum, visited):
                foundWall = True
            if self.iterClusterSearch(layerNum - 1, rowNum, cellNum, visited):
                foundWall = True
            if self.iterClusterSearch(layerNum, rowNum + 1, cellNum, visited):
                foundWall = True
            if self.iterClusterSearch(layerNum, rowNum - 1, cellNum, visited):
                foundWall = True
            if self.iterClusterSearch(layerNum, rowNum, cellNum + 1, visited):
                foundWall = True
            if self.iterClusterSearch(layerNum, rowNum, cellNum - 1, visited):
                foundWall = True

        return foundWall
    
    def getNumValidClusters(self):
        
        # start by looking for fuel cells
        # all the following components connected to the fuel cell
        # or other components along the way there belong to the cluster
        
        # fuel cell
        # conductor
        # shield?
        # reflector?
        # cooler
        
        # I think moderators do not contribute to clusters
        
        # I'm going to start by making a boolean copy of the reactor to keep track of
        # already visited components
        
        visited = np.zeros_like(self.grid, dtype=bool)
        
        
        clusterCount = 0
        for layerNum, layer in enumerate(self.grid):
            
            for rowNum, row in enumerate(layer):
                
                for cellNum, cell in enumerate(row):
                    
                    # check visited list and skip if already visited
                    if visited[layerNum][rowNum][cellNum] == True:
                        continue
                    
                    # if we see a fuel cell start checking the cluster
                    if isinstance(cell, FuelCell):
                        
                        # if we hit a wall then increment the cluster count
                        if self.iterClusterSearch(layerNum, rowNum, cellNum, visited):
                            clusterCount += 1

        return clusterCount
    
        
        
    def printGrid(self):
        
        # print layers
        
        print('Reactor: ' + self.name)
        
        layerIndex = 0
        for layer in self.grid:
            
            print('============ LAYER ' + str(layerIndex) + ' ============')
            rowString = '  '
            for num in range(self.rows):
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
                    elif isinstance(r, Conductor):
                        rowString += '+ '
                    else:
                        rowString += 'E '
                print(rowString)
                rowNum += 1
                
            layerIndex += 1