
from Fuel import Fuel
from Cell import FuelCell
from Cell import Moderator
from Cell import Shield
from Cell import Irradiator
from Cell import Cooler
from Cell import Conductor

from Reactor import Reactor

def main():
    
    print('============ Starting NCSG ============')

    leu233 = Fuel(name='LEU-233 OX', efficiency=1.1, heat=216, criticality=78)
    
    reactor = Reactor(6, 6, 6, 'Test Reactor')
    
    fc = FuelCell(leu233)
    reactor.grid[0][0][0] = fc
    mod = Moderator(36, 1)
    reactor.grid[0][0][1] = mod
    mod2 = Moderator(10, 1.1)
    reactor.grid[0][0][2] = mod2
    mod3 = Moderator(22, 1.05)
    reactor.grid[0][0][3] = mod3
    mod4 = Moderator(10, 1.1)
    reactor.grid[0][0][4] = mod4
    fc2 = FuelCell(leu233)
    reactor.grid[0][0][5] = fc2
    cond = Conductor()
    reactor.grid[0][1][0] = cond
    reactor.grid[0][1][1] = cond
    reactor.grid[0][1][2] = cond
    reactor.grid[0][1][3] = cond
    reactor.grid[0][1][4] = cond
    reactor.grid[0][1][5] = cond
    #cool = Cooler(100, None)
    #reactor.grid[1][0][1] = cool
    
    reactor.printGrid()
    print(reactor.getNumValidClusters())

if __name__ == "__main__":
    main()