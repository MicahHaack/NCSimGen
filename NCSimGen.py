
from Fuel import Fuel
from Cell import FuelCell
from Cell import Moderator
from Cell import Shield
from Cell import Irradiator
from Cell import Cooler

from Reactor import Reactor

def main():
    
    print('============ Starting NCSG ============')

    tbu = Fuel()
    
    reactor = Reactor(2, 7, 7, 'Test Reactor')
    
    fc = FuelCell(tbu)
    reactor.grid[1][1][1] = fc
    mod = Moderator(10, 10)
    reactor.grid[0][0][0] = mod
    cool = Cooler(100, None)
    reactor.grid[1][0][1] = cool
    
    reactor.printGrid()

if __name__ == "__main__":
    main()