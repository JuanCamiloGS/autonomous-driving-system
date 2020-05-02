#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import sys
import argparse
import socket
import driver
import threading
from threading import Thread
from pyqtgraph.Qt import QtGui, QtCore
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import pyqtgraph as pg
import csv
import timeit
from PyQt4 import QtGui,QtCore
import Design
from skfuzzy.control.visualization import FuzzyVariableVisualizer
import time
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 21
plt.rcParams['text.antialiased']=True
plt.rcParams['figure.facecolor'] = '0.95'

global d, thread2, isGUI, isFuzzyView

isGUI = False
isFuzzyView = False

class ThreadA(threading.Thread):
    def __init__(self, threadID, name, counter): #Constructor. El valor counter no tiene importancia.
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        global d, thread2, sheet, win, app
        # Configure the argument parser
        parser = argparse.ArgumentParser(description = 'Python client to connect to the TORCS SCRC server.')

        parser.add_argument('--host', action='store', dest='host_ip', default='localhost',
                            help='Host IP address (default: localhost)')
        parser.add_argument('--port', action='store', type=int, dest='host_port', default=3001,
                            help='Host port number (default: 3001)')
        parser.add_argument('--id', action='store', dest='id', default='SCR',
                            help='Bot ID (default: SCR)')
        parser.add_argument('--maxEpisodes', action='store', dest='max_episodes', type=int, default=1,
                            help='Maximum number of learning episodes (default: 1)')
        parser.add_argument('--maxSteps', action='store', dest='max_steps', type=int, default=100000,
                            help='Maximum number of steps (default: 100000)')
        parser.add_argument('--track', action='store', dest='track', default=None,
                            help='Name of the track')
        parser.add_argument('--stage', action='store', dest='stage', type=int, default=2,
                            help='Stage (0 - Warm-Up, 1 - Qualifying, 2 - Race, 3 - Unknown)')

        arguments = parser.parse_args()

        # Print summary
        print 'Connecting to server host ip:', arguments.host_ip, '@ port:', arguments.host_port
        print 'Bot ID:', arguments.id
        print 'Maximum episodes:', arguments.max_episodes
        print 'Maximum steps:', arguments.max_steps
        print 'Track:', arguments.track
        print 'Stage:', arguments.stage
        print '*********************************************'

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
        except socket.error, msg:
            print 'Could not make a socket.'
            sys.exit(-1)

        # one second timeout
        sock.settimeout(1.0)

        shutdownClient = False
        curEpisode = 0

        verbose = False

        d = driver.Driver(arguments.stage)
        
        if isGUI:
            thread2.start() #Comienza el segundo hilo.

        while not shutdownClient:
            while True:
                print 'Sending id to server: ', arguments.id
                buf = arguments.id + d.init()
                print 'Sending init string to server:', buf
                
                try:
                    sock.sendto(buf, (arguments.host_ip, arguments.host_port))
                    print 'si'
                except socket.error, msg:
                    print "Failed to send data...Exiting..."
                    sys.exit(-1)
                sockdata = str()
                    
                try:
                    buf, addr = sock.recvfrom(1000)
                    
                except socket.error, msg:
                    print "didn't get response from server..."
            
                if buf.find('***identified***') >= 0:
                    print 'Received: ', buf
                    break

            currentStep = 0
            
            #threadLock.release()
            while True:
                # wait for an answer from server
                buf = None
                try:
                    buf, addr = sock.recvfrom(1000)
                except socket.error, msg:
                    print "didn't get response from server..."
                
                if verbose:
                    print 'Received: ', buf
                
                if buf != None and buf.find('***shutdown***') >= 0:                  
                    d.onShutDown()
                    shutdownClient = True
                    print 'Client Shutdown'
                    app.closeAllWindows()
                    thread2.stopFlag.set()
                    #win.close()
                    #thread2.stop()
                    break
                
                if buf != None and buf.find('***restart***') >= 0:
                    d.onRestart()
                    print 'Client Restart'
                    app.closeAllWindows()
                    thread2.stopFlag.set()
                    break
                
                currentStep += 1
                if currentStep != arguments.max_steps:
                    if buf != None:
                        buf = d.drive(buf)
                else:
                    buf = '(meta 1)'
                
                if verbose:
                    print 'Sending: ', buf
                
                if buf != None:
                    try:
                        sock.sendto(buf, (arguments.host_ip, arguments.host_port))
                    except socket.error, msg:
                        print "Failed to send data...Exiting..."
                        sys.exit(-1)
            
            curEpisode += 1
            
            if curEpisode == arguments.max_episodes:
                shutdownClient = True

        sock.close()
        
class GUI(QtGui.QMainWindow, Design.Ui_MainWindow):
    def __init__(self, parent=None):
        global d, imgFlag
        pg.setConfigOption('background', 'w') #before loading widget
        super(GUI, self).__init__(parent)
        self.setupUi(self)
        V = d.getvector()
        self.FuzzyDet.setBackground(None)
        self.FuzzyDet.setAspectLocked(False)
        self.FuzzyDet.hideAxis('left')
        self.FuzzyDet.hideAxis('bottom')
        self.FuzzyAccel = pg.ImageItem()
        self.FuzzyDet.addItem(self.FuzzyAccel)
        
        self.FuzzyDet_2.setBackground(None)
        self.FuzzyDet_2.setAspectLocked(False)
        self.FuzzyDet_2.hideAxis('left')
        self.FuzzyDet_2.hideAxis('bottom')
        self.FuzzyBrake = pg.ImageItem()
        self.FuzzyDet_2.addItem(self.FuzzyBrake)
        
        imgFlag = True
        
        self.VelView.plotItem.showGrid(True, True, 0.7)
        self.VelView.setTitle("Velocity")
        self.VelView.setLabel('left','(Km)')
        self.VelView.setBackground(None)
        
        self.ATView.plotItem.showGrid(True, True, 0.7)
        self.ATView.setLabel('left','(Rad)')
        self.ATView.setTitle("Angle")
        self.ATView.setBackground(None)
        
        self.ATView_2.plotItem.showGrid(True, True, 0.7)
        self.ATView_2.setTitle("Track Position")
        self.ATView_2.setLabel('left','(%)')
        self.ATView_2.setYRange(-1,1)
        self.ATView_2.setBackground(None)
        
        self.BAView.plotItem.showGrid(True, True, 0.7)
        self.BAView.setTitle('<html><head/><body><p><span style=" color:blue">Accel</span> VS <span style=" color:green">Brake</span></p></body></html>')
        self.BAView.setLabel('left','(%)')
        self.BAView.setYRange(0,1)
        self.BAView.setBackground(None)
        
        self.Steering.plotItem.showGrid(True, True, 0.7)
        self.Steering.setTitle("Steering")
        self.Steering.setLabel('left','(%)')
        self.Steering.setYRange(-1,1)
        self.Steering.setBackground(None)
        
        self.VelPlot = self.VelView.plot(V[0], pen=(0,125,0))
        self.AnglePlot = self.ATView.plot(V[1], pen=(255,0,0))
        self.TPosPlot = self.ATView_2.plot(V[2], pen=(0,0,255))
        self.SteerPlot = self.Steering.plot(V[3], pen=(255,0,0))
        self.AccelPlot = self.BAView.plot(V[4], pen=(0,0,255))
        self.BrakePlot = self.BAView.plot(V[5], pen=(0,125,0))
        
        self.S1.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.S2.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.S3.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.S4.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.S5.setSegmentStyle(QtGui.QLCDNumber.Flat)

        self.S1.setStyleSheet("* { color: darkblue; }")
        self.S2.setStyleSheet("* { color: darkblue; }")
        self.S3.setStyleSheet("* { color: darkblue; }")
        self.S4.setStyleSheet("* { color: darkblue; }")
        self.S5.setStyleSheet("* { color: darkblue; }")

        self.x = np.linspace(0.0, 60, num=600)

    def update(self):
        global d, imgFlag
        V = d.getvector()
        size = V[0].size
        self.VelPlot.setData(self.x[:size],V[0])
        self.AnglePlot.setData(self.x[:size],V[1])
        self.TPosPlot.setData(self.x[:size],V[2])
        self.SteerPlot.setData(self.x[:size],V[3])
        self.AccelPlot.setData(self.x[:size],V[4])
        self.BrakePlot.setData(self.x[:size],V[5])
        
        self.S1.display(d.izq)
        self.S2.display(d.front)
        self.S3.display(d.der)
        self.S4.display(d.trasIzq)
        self.S5.display(d.trasDer)
        self.ST.display(d.trackfront)
        
        if imgFlag == False:
            self.pic()
            imgFlag = True
            
        
    def pic(self):
        global AccelImg, BrakeImg
        try:
            self.FuzzyBrake.setImage(BrakeImg, autoDownsample=True)
            self.FuzzyAccel.setImage(AccelImg, autoDownsample=True)
        except:
            print "Not ready"
        
        

class ThreadB(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.stopFlag = threading.Event()
        self.thread3 = ThreadC(3, "Thread-3", 3, self.stopFlag)
        

    def run(self):
        global app
        app = QtGui.QApplication(sys.argv)
        form = GUI()
        form.show()
        timer = pg.QtCore.QTimer() #Tomado del segundo ejemplo de PyQtGraph 
        timer.timeout.connect(form.update)
        timer.start(100)
        
        if isFuzzyView:
            self.thread3.start()
        app.exec_()
        
class ThreadC(threading.Thread):
    def __init__(self, threadID, name, counter, event):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.stopped = event
        self.stage = 1

    def run(self):
        global form, AccelImg, BrakeImg, imgFlag
        AccelImg = None
        BrakeImg = None
        while d.Fuzzy.Brk == None or d.Fuzzy.Acc == None:
            self.stopped.wait(0.1)
        while not self.stopped.is_set():
            if imgFlag:
                FigB, AxB = FuzzyVariableVisualizer(d.Fuzzy.BrakeUniverse).view(sim=d.Fuzzy.Brk)
                self.stopped.wait(0.1)
                FigA, AxA = FuzzyVariableVisualizer(d.Fuzzy.AccelUniverse).view(sim=d.Fuzzy.Acc)
                self.stopped.wait(0.1)
                FigB.tight_layout(pad=0)
                AxB.yaxis.label.set_visible(False)
                AxB.xaxis.label.set_visible(False)
                AxB.set_yticklabels([])
                FigB.canvas.draw()
                self.stopped.wait(0.1)
                FigA.tight_layout(pad=0)
                AxA.xaxis.label.set_visible(False)
                FigA.canvas.draw()
                self.stopped.wait(0.1)
                BrakeImg2 = np.fromstring(FigB.canvas.tostring_rgb(), dtype='uint8')
                self.stopped.wait(0.1)
                AccelImg2 = np.fromstring(FigA.canvas.tostring_rgb(), dtype='uint8')
                self.stopped.wait(0.1)
                BrakeImg2 = BrakeImg2.reshape(FigB.canvas.get_width_height()[::-1] + (3,))
                BrakeImg = np.rot90(BrakeImg2,3)
                self.stopped.wait(0.1)
                AccelImg2 = AccelImg2.reshape(FigA.canvas.get_width_height()[::-1] + (3,))
                AccelImg = np.rot90(AccelImg2,3)
                self.stopped.wait(0.1)
                plt.close('all')
                imgFlag = False
                self.stopped.wait(0.1)

threadLock = threading.Lock()
threads = []

# Create new threads
thread1 = ThreadA(1, "Thread-1", 1)
thread2 = ThreadB(2, "Thread-2", 2)

# Start new Threads
thread1.start()
#thread2.start()

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"

