#!/usr/bin/python
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import argparse
import pdb

app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="PipePlot")
win.resize(1000,600)
win.setWindowTitle('PipePlot')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

plot = win.addPlot(title="PipePlot")
pencolors=['b','g','r','c','m','y','k','w']

curves = []
data = np.empty(0)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--names', metavar='N', type=str, nargs='+', help='Column names')
parser.add_argument('--xlimit', type=int, nargs='?', default='1000', help='Buffer size')
parser.add_argument('--interval', type=int, nargs='?', default='10', help='Update interval in ms')
parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()

def shift(xs, n):
    e = np.empty_like(xs)
    if n >= 0:
        e[:n] = np.nan
        e[n:] = xs[:-n]
    else:
        e[n:] = np.nan
        e[:n] = xs[-n:]
    return e

def readlines():
    global curves, data, plot
    line = sys.stdin.readline()
    cols = line.split(' ')
    if args.verbose:
        #print  ' '.join(cols)
        sys.stdout.write(' '.join(cols))
    if readlines.first:
        plot.addLegend()
        readlines.first = False
        data = np.empty([len(cols), args.xlimit])
        pencolorsel=0
        for i in range(len(cols)):
            if i < len(args.names):
                plotName = args.names[i]
            else:
                plotName = "-"
            curves.append(plot.plot(pen=pencolors[pencolorsel%8], name=plotName))
            pencolorsel = pencolorsel + 1

    for i in range(len(cols)):
        try:
            data[i] = shift(data[i], 1)
            data[i][0] = float(cols[i])
        except ValueError:
            print "ValueError:", cols
readlines.first = True

def update():
    global curves, data
    readlines()

    for i in range(len(curves)):
		curves[i].setData(data[i])

if __name__ == '__main__':
    import sys
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(args.interval)
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

