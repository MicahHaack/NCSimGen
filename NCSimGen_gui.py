
from tkinter import *
from tkinter import ttk

from Cell import FuelCell
from Fuel import Fuel
from Reactor import Reactor

def main():

    tbuOX = Fuel()
    fC = FuelCell(tbuOX)

    rctr = Reactor(4, 5, 3)
    rctr.grid[0][0][0] = fC

    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    #ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    
    for h in range(rctr.height):
        for r in range(rctr.length):
            for c in range(rctr.width):
                ttk.Label(frm, text=f'{r}{c}{h}', padding=10).grid(column=rctr.width*h+c+h, row=r)
    
    root.mainloop()

if __name__ == "__main__":
    main()