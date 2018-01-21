#!/usr/bin/python
from pyqtgraph.Qt import QtCore, QtGui
from PyQt4.QtCore import pyqtRemoveInputHook
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import argparse
import pdb

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.opts['distance'] = 40
w.show()

gx = gl.GLGridItem()
gx.rotate(90, 0, 1, 0)
#gx.translate(-10, 0, 0)
w.addItem(gx)
gy = gl.GLGridItem()
gy.rotate(90, 1, 0, 0)
#gy.translate(0, -10, 0)
w.addItem(gy)
gz = gl.GLGridItem()
#gz.translate(0, 0, -10)
w.addItem(gz)

x = np.linspace(0,10,3)
n = 100

plt_list = []
xyz_arr = None
y_arr = np.linspace(0, 9, n)
def debug_trace():
    pyqtRemoveInputHook()
    pdb.set_trace()

def shift(xs, n):
    e = np.empty_like(xs)
    if n >= 0:
        e[:n] = np.nan
        e[n:] = xs[:-n]
    else:
        e[n:] = np.nan
        e[:n] = xs[-n:]
    return e

def update():
    global n, plt_list, xyz_arr
    # Read line from stdin
    line = sys.stdin.readline().rstrip()
    # Store number for each column
    cols = line.split(' ')

    print "Cols:" + str(len(cols))
    print cols
    if len(cols) > 1:
        print "A"
        # Convert list of strings to list of floats for y axis
        z = np.array(map(float, cols))  * 30
        y = np.zeros(len(cols))
        x = np.linspace(0, 10, len(cols))
        xyz = np.vstack([x, y, z])

        # If xyz_arr does not exist, create it
        if update.first == True:
            update.first = False
            xyz_arr = np.zeros([n,3,len(cols)])

        # Shift xyz_arr and add xyz to bottom of array
        xyz_arr = shift(xyz_arr, 1)
        xyz_arr[0] = xyz

        # Remove old plots
        for plt in plt_list:
            w.removeItem(plt)

        # Clear plots
        plt_list = []

        # Replace with new y values
        for i in range(len(xyz_arr)):
            xyz_arr[i][1]=[y_arr[i]]*len(cols)

        # Plot new lines
        for xyz_it in xyz_arr:
            xyz_t = xyz_it.transpose()
            plt = gl.GLLinePlotItem(pos=xyz_t, width=1, antialias=True)
            plt_list.append(plt)
            w.addItem(plt)
update.first = True

if __name__ == '__main__':
    import sys
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(1)
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


