
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

    tbu = Fuel()
    
    reactor = Reactor(5, 5, 5, 'Test Reactor')
    
    fc = FuelCell(tbu)
    reactor.grid[0][0][0] = fc
    mod = Moderator(10, 10)
    reactor.grid[0][0][1] = mod
    mod2 = Moderator(10, 10)
    reactor.grid[0][0][2] = mod2
    mod3 = Moderator(10, 10)
    reactor.grid[0][0][3] = mod3
    fc2 = FuelCell(tbu)
    reactor.grid[0][0][4] = fc2
    cond = Conductor()
    reactor.grid[0][1][0] = cond
    reactor.grid[0][1][1] = cond
    reactor.grid[0][1][2] = cond
    reactor.grid[0][1][3] = cond
    reactor.grid[0][1][4] = cond
    #cool = Cooler(100, None)
    #reactor.grid[1][0][1] = cool
    
    reactor.printGrid()
    print(reactor.getNumValidClusters())

if __name__ == "__main__":
    main()