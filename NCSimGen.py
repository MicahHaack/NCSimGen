
from Cell import FuelCell
from Fuel import Fuel
from Reactor import Reactor

def main():

    tbuOX = Fuel()
    fC = FuelCell(tbuOX)

    rctr = Reactor(3, 3, 3)
    rctr.grid[0][0][0] = fC

    print(rctr.grid)

if __name__ == "__main__":
    main()