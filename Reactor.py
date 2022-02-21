"""
@author Micah Haack

width, length, and height here refer to the reactor internal

"""
import numpy as np

from Cell import Cell
from Cell import FuelCell
from Cell import Moderator
from Cell import Reflector
from Cell import Shield
from Cell import Cooler
from Cell import Irradiator
from Cell import Conductor

from Cluster import Cluster

class Reactor:

    def __init__(self, rows, cols, height, name='Reactor'):

        self.rows = rows
        self.cols = cols
        self.height = height

        self.output = 0
        self.efficiency = 0

        self.grid = [[[Cell for h in range(height)] for w in range(rows)] for l in range(cols)]
        
        self.name = name
    
    def iterClusterSearch(self, layerNum, rowNum, cellNum, visited, cluster):
        
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
            cluster.addCell(cell)
            # if so search the surrounding cells, if any hit a wall record that
            
            if self.iterClusterSearch(layerNum + 1, rowNum, cellNum, visited, cluster):
                foundWall = True
            if self.iterClusterSearch(layerNum - 1, rowNum, cellNum, visited, cluster):
                foundWall = True
            if self.iterClusterSearch(layerNum, rowNum + 1, cellNum, visited, cluster):
                foundWall = True
            if self.iterClusterSearch(layerNum, rowNum - 1, cellNum, visited, cluster):
                foundWall = True
            if self.iterClusterSearch(layerNum, rowNum, cellNum + 1, visited, cluster):
                foundWall = True
            if self.iterClusterSearch(layerNum, rowNum, cellNum - 1, visited, cluster):
                foundWall = True

        return foundWall
    
    # returns isLineValid, fluxSum, lineEff
    def checkModLine(self, layerNum, rowNum, cellNum, layerWalk, rowWalk, cellWalk, totalChecked, fluxSum, lineEff):
        
        if layerNum < 0 or layerNum >= self.height or rowNum < 0 or rowNum >= self.rows or cellNum < 0 or cellNum >= self.cols:
            return 0, 0, 0
        
        cell = self.grid[layerNum][rowNum][cellNum]
        # if we are at the end of the mod line, check for a valid end component
        # TODO: implement reflectors (length counts twice!)
        # TODO: implement end of line Irradiator
        if totalChecked == 4:
            if isinstance(cell, FuelCell):
                # valid moderator line
                return 1, fluxSum, lineEff
        
        # otherwise, check if the current cell is a valid moderator (or shield)
        if isinstance(cell, Moderator):
            # then continue walking along the path
            fluxSum += cell.flux
            lineEff += cell.efficiency
            return self.checkModLine(layerNum + layerWalk, rowNum + rowWalk, cellNum + cellWalk,
                               layerWalk, rowWalk, cellWalk, totalChecked + 1, fluxSum, lineEff)
        elif isinstance(cell, Shield):
            return self.checkModLine(layerNum + layerWalk, rowNum + rowWalk, cellNum + cellWalk,
                               layerWalk, rowWalk, cellWalk, totalChecked + 1, fluxSum, lineEff)
        # check if we ended the path early
        elif totalChecked != 0 and isinstance(cell, FuelCell):
            return 1, fluxSum, lineEff / totalChecked
        elif isinstance(cell, FuelCell):
            # starter case
            return self.checkModLine(layerNum + layerWalk, rowNum + rowWalk, cellNum + cellWalk,
                               layerWalk, rowWalk, cellWalk, totalChecked, fluxSum, lineEff)
        elif isinstance(cell, Irradiator):
            return 1, 0, 0
        # check reflector
        elif isinstance(cell, Reflector):
            if totalChecked <= 2:
                return 1, fluxSum * 2 * cell.reflectivity, (lineEff / totalChecked) * cell.efficiency
        
        # otherwise, invalid moderator line, return a flux of 0
        return 0, 0, 0
            
    
    # assuming all are primed with a perfect
    # Cf-252 source for now (1.0 efficiency)
    def checkFuelCell(self, layerNum, rowNum, cellNum):
        
        # need to check the in-line components for valid moderator lines,
        # and sum up the neutron flux
        # TODO: implement reflectors -> might be done?
        # TODO: implement shields -> might be done?
        # TODO: implement priming
        
        # count adjacent (valid!) moderator lines
        validModLines = 0
        totalFlux = 0
        positionalEff = 0
        
        checkLine = 0
        lineFlux = 0
        lineEff = 0
        
        # vertical dim
        checkLine, lineFlux, lineEff = self.checkModLine(layerNum, rowNum, cellNum,
                            1, 0, 0, 0, 0, 0)
        validModLines += checkLine
        totalFlux += lineFlux
        positionalEff += lineEff
        checkLine, lineFlux, lineEff = self.checkModLine(layerNum, rowNum, cellNum,
                            -1, 0, 0, 0, 0, 0)
        validModLines += checkLine
        totalFlux += lineFlux
        positionalEff += lineEff
        
        # horiz dim 1 (row)
        checkLine, lineFlux, lineEff = self.checkModLine(layerNum, rowNum, cellNum,
                            0, 1, 0, 0, 0, 0)
        validModLines += checkLine
        totalFlux += lineFlux
        positionalEff += lineEff
        checkLine, lineFlux, lineEff = self.checkModLine(layerNum, rowNum, cellNum,
                            0, -1, 0, 0, 0, 0)
        validModLines += checkLine
        totalFlux += lineFlux
        positionalEff += lineEff
            
        # horiz dim 2 (cell)
        checkLine, lineFlux, lineEff = self.checkModLine(layerNum, rowNum, cellNum,
                            0, 0, 1, 0, 0, 0)
        validModLines += checkLine
        totalFlux += lineFlux
        positionalEff += lineEff
        checkLine, lineFlux, lineEff = self.checkModLine(layerNum, rowNum, cellNum,
                            0, 0, -1, 0, 0, 0)
        validModLines += checkLine
        totalFlux += lineFlux
        positionalEff += lineEff
    
        return validModLines, totalFlux, positionalEff
    
    def getValidClusters(self):
        
        # start by looking for fuel cells
        # all the following components connected to the fuel cell
        # or other components along the way there belong to the cluster
        
        # fuel cell
        # conductor
        # -> this is an odd case: clusters can form with conductors and nothing else,
        # but they won't be valid
        
        # shield?
        # reflector?
        # cooler
        
        # I think moderators do not contribute to clusters
        # -> correct
        
        # I'm going to start by making a boolean copy of the reactor to keep track of
        # already visited components
        
        visited = np.zeros_like(self.grid, dtype=bool)
        
        clusters = []
        
        clusterCount = 0
        for layerNum, layer in enumerate(self.grid):
            
            for rowNum, row in enumerate(layer):
                
                for cellNum, cell in enumerate(row):
                    
                    # check visited list and skip if already visited
                    if visited[layerNum][rowNum][cellNum] == True:
                        continue
                    # if we see a fuel cell start checking the cluster
                    if isinstance(cell, FuelCell):
                        # check if fuel cell is valid
                        tempCluster = Cluster()
                        numLines, totalFlux, lineEff = self.checkFuelCell(layerNum, rowNum, cellNum)
                        if numLines > 0 and totalFlux >= cell.fuel.criticality:
                            # TODO: check self-priming fuels
                            # mark that the fuel cell is active and adjust the moderator line count
                            cell.active = True
                            cell.adjacentModeratorLines = numLines                            
                            # if we hit a wall then increment the cluster count and attatch the cluster
                            if self.iterClusterSearch(layerNum, rowNum, cellNum, visited, tempCluster):
                                clusterCount += 1
                                clusters.append(tempCluster)

        return clusterCount, clusters
    
        
        
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