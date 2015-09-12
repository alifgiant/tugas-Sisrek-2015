from GUI import GUI
from Tkinter import Tk
from Function import Function
__author__ = 'maakbar'


def main():
    root = Tk()
    root.geometry("800x600+0+0")#w x h + posx + posy
    function = Function()
    app = GUI(root, function)
    function.addGUI(app)
    root.mainloop()

if __name__ == '__main__':
    main() #show the GUI


def check_difference(fdata, idata, x, y):
    dif = 0

    w = idata.shape[0]
    h = idata.shape[1]

    # Check pixels in top, with height of 2
    for i in range(0, w):
        dif += abs(fdata[x * w + i][y * h - 1] - idata[i][0])

    # Check pixels in left, with width of 2
    for i in range(0, h):
        dif += abs(fdata[x * w - 1][y * h + i] - idata[0][i])

    return dif