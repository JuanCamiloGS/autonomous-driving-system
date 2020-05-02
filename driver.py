import msgParser
import carState
import carControl
import neuro
import fuzzy
import os 
import numpy as np
import serial, time
import timeit
import serial, time
import usb
from operator import truediv
import xlsxwriter
import math 

global isExperiment

isExperiment= False
wheel = 0

busses = usb.busses()
for bus in busses:      
  devices = bus.devices   
  for dev in devices:
    if dev.idVendor == 0x046d and dev.idProduct == 0xc29a:
      print "Found Wheel, testing various settings (press enter to advance to next)"
      wheel = dev

if wheel == 0:
  print "Wheel not found"
  #exit(0)

# Get a device handler for the usb device and detach it from the kernel
try:
    dh = wheel.open()
    try:
        dh.detachKernelDriver(0)
    except:
        print("No")
    dh.claimInterface(0)
except: 
    dh=0


print "Clearing previous effect"

class Driver(object):
    '''
    A driver object for the SCRC
    '''
    
    def __init__(self, stage):
        '''Constructor'''
        self.WARM_UP = 0
        self.QUALIFYING = 1
        self.RACE = 2
        self.UNKNOWN = 3
        self.stage = stage
        
        self.parser = msgParser.MsgParser()
        
        self.state = carState.CarState()
        
        self.control = carControl.CarControl()
        
        self.steer_lock = 0.785398
        self.max_speed = 90
        self.prev_rpm = None

        self.Neuro = neuro.Neuro()
        self.Fuzzy = fuzzy.Fuzzy()

        self.vector1 = np.array([])
        self.vector2 = np.array([])
        self.vector3 = np.array([])
        self.vector4 = np.array([])
        self.vector5 = np.array([])
        self.vector6 = np.array([])
        self.izq = 0
        self.front = 0
        self.der = 0
        self.trasIzq = 0
        self.trasDer = 0
        self.trackfront = 0
        self.matrix = [[0, 0, 0]]
        self.cont = 0
        self.maxCont = 5

        #self.arduino = serial.Serial("/dev/ttyACM4", 9600)

        

    def init(self): 
        '''Return init string with rangefinder angles'''
        self.angles = [0 for x in range(19)]
        
        for i in range(5):
            self.angles[i] = -90 + i * 15
            self.angles[18 - i] = 90 - i * 15
        
        for i in range(5, 9):
            self.angles[i] = -20 + (i-5) * 5
            self.angles[18 - i] = 20 - (i-5) * 5
        self.bdIntersection=0
        self.timetoStop = 0
        self.maxTSpeed = 0
        self.secureDistOp = 0
        self.secureDistOb = 0
        self.CarDamage = 0
        self.origD = self.state.damage
        self.effortCar = 0
        self.samples = 0
        self.oriaccel = self.control.getAccel()
        self.oribrake = self.control.getBrake()
        self.oriRPM = self.state.getRpm()
        self.distanceaffected = 30

        return self.parser.stringify({'init': self.angles})
    
    def drive(self, msg):
        self.state.setFromMsg(msg)
        self.steer()
        self.gear()
        self.speed()
        #print "Opponent distance ", self.state.opponents[16], self.state.opponents[17], self.state.opponents[18], self.state.opponents[19]
        #print self.state.opponents[18]

        
        if(self.state.distFromStart>self.distanceaffected and self.cont == self.maxCont):
            self.samples +=1
            if(self.state.damage>self.origD):
                self.origD = self.state.damage
                self.CarDamage+=1
        if(self.cont==self.maxCont):
            self.matrix = np.vstack((self.matrix,[self.control.getSteer(),self.control.getAccel(),self.control.getBrake()]))
            if self.vector1.size >= 600:
                self.vector1 = np.delete(self.vector1, 0)
                self.vector2 = np.delete(self.vector2, 0)
                self.vector3 = np.delete(self.vector3, 0)
                
            self.vector1 = np.append(self.vector1, self.state.speedX)
            self.vector2 = np.append(self.vector2, self.state.angle)
            self.vector3 = np.append(self.vector3, self.state.trackPos)
            
            self.cont=0
        self.cont +=1   
        return self.control.toMsg()
        
    
    def steer(self):
        '''
        angle = self.state.angle
        #print angle
        dist = self.state.trackPos
        
        steerp = (angle - dist*0.5)/self.steer_lock
        '''
        self.front = min(self.state.opponents[16], self.state.opponents[17], self.state.opponents[18],self.state.opponents[19], self.state.opponents[20])
        self.izq = min(self.state.opponents[8],self.state.opponents[9], self.state.opponents[10], self.state.opponents[11], self.state.opponents[12],self.state.opponents[13], self.state.opponents[14],self.state.opponents[15],self.state.opponents[16])
        self.der = min(self.state.opponents[20],self.state.opponents[21],self.state.opponents[22], self.state.opponents[23], self.state.opponents[24],self.state.opponents[25], self.state.opponents[26],self.state.opponents[27],self.state.opponents[28])
        self.trasIzq = min(self.state.opponents[4],self.state.opponents[5],self.state.opponents[6],self.state.opponents[7],self.state.opponents[8])
        self.trasDer = min(self.state.opponents[28],self.state.opponents[29],self.state.opponents[30],self.state.opponents[31],self.state.opponents[32])
        SV = np.divide(np.array([self.izq, self.front, self.der, self.trasIzq, self.trasDer]), 200.0)
        P = [SV[0], SV[1], SV[2], SV[3], SV[4], self.state.angle,self.state.trackPos]
        rounded = self.Neuro.PredictSteer(P)
        
        #print der*200, rounded[1]
        prediction = rounded[0]
        self.control.setSteer(prediction)
        if(self.state.distFromStart>self.distanceaffected and self.cont == self.maxCont):
            minSensors = min(self.state.track[0],self.state.track[18])
            if(self.state.speedX>truediv(np.sqrt(minSensors*0.7*9.8)*3600,1000) and np.absolute(prediction>0.25)):
                self.maxTSpeed+=1
            if(self.state.speedX==0):
                doppS = 5
            else:
                doppS = round(2.01*math.log(self.state.speedX)-4.66)

            if(any(self.state.opponents[x]<=doppS for x in range(14,23))or any(self.state.opponents[y]<=doppS for y in range(4,14))or any(self.state.opponents[z]<=doppS for z in range(23,32))or any(self.state.opponents[t]<3 for t in range(32,36)or any(self.state.opponents[u]<3 for u in range(0,5)))):
                self.secureDistOp+=1
            if(np.absolute(self.state.trackPos)>1 or (self.state.track[9]<self.state.speedX*0.15)):
                self.secureDistOb+=1

        if self.cont == self.maxCont:
            if self.vector4.size >= 600:
                self.vector4 = np.delete(self.vector4, 0)
            self.vector4 = np.append(self.vector4, prediction)
             
        if(dh!=0):
            if(round(prediction*100) in range(-100,-5)):
                command = '\x11\x08\x5C\x00\x00\x00\x00'
                dh.bulkWrite(0x01, command, len(command))
                
            elif(round(prediction*100) in range(-5,5)):
                command = '\x11\x0D\x06\x06\x80\x00\x00'
                dh.bulkWrite(0x01, command, len(command))
            else:
                command = '\x11\x08\x9E\x00\x00\x00\x00'
                dh.bulkWrite(0x01, command, len(command))    
    
    def gear(self):
        
        rpm = self.state.getRpm()
        gear = self.state.getGear()
        if self.prev_rpm == None:
            up = True
        else:
            if (self.prev_rpm - rpm) < 0:
                up = True
            else:
                up = False
        
        if up and rpm > 6000:
            gear += 1
        
        if(not up) and rpm < 3000 and gear != 1:
            gear -= 1
        if(self.state.distFromStart>self.distanceaffected and self.cont == self.maxCont):
            if(self.oriaccel>2*self.control.getAccel()):
                self.oriaccel=self.control.getAccel()
                self.effortCar+=1
            if(self.oribrake>2*self.control.getBrake()):
                self.oribrake=self.control.getBrake()
                self.effortCar+=1
        
        self.prev_rpm = rpm
        
        self.control.setGear(gear)
        
    
    def speed(self):
        val = self.Fuzzy.PredictPedals(min(self.state.track[9]-2, min(self.state.opponents[17],self.state.opponents[18],self.state.opponents[19])+3), self.state.getSpeedX())
        self.control.setAccel(val[0])
        self.control.setBrake(val[1])
        
        if(self.state.distFromStart>self.distanceaffected and self.cont == self.maxCont):
            rd = 0.011477*np.square([self.state.speedX,2])+0.6938*self.state.speedX+0.0763
            if(self.state.track[9]<rd[0] and val[1]>0.25):
                self.bdIntersection+=1
            
            if(self.state.speedX>70 and val[1]>0.25):
                self.timetoStop+=1
        if self.cont == self.maxCont:
            self.trackfront = self.state.track[9]
            if self.vector5.size >= 600:
                self.vector5 = np.delete(self.vector5, 0)
                self.vector6 = np.delete(self.vector6, 0)
            self.vector5 = np.append(self.vector5, val[0])
            self.vector6 = np.append(self.vector6, val[1])
            
    def getvector(self):
        return[self.vector1,self.vector2,self.vector3,self.vector4,self.vector5,self.vector6]
    def getsafetyptage(self):
        return self.safetyPTAGE
    def onShutDown(self):
        if(isExperiment==True):
            vectorExp=[self.bdIntersection,self.timetoStop,self.maxTSpeed,self.secureDistOp,self.secureDistOb,self.CarDamage,self.effortCar,self.samples]
            vectorName=["Brake distance before int","Time to Stop","Max Turn Speed","Secure Distance Opp","Secure Distance Obst","Damage","Effort Car","Samples"]
            workbook = xlsxwriter.Workbook(os.getcwd()+"/Experiments/ExpertiseEval"+"_date_"+time.strftime("%d_%m_%Y_%H_%M")+".xlsx")
            worksheet = workbook.add_worksheet()
            # Add a bold format to use to highlight cells.
            bold = workbook.add_format({'bold': True})
            centered = workbook.add_format({'align':'center','border':1})
            bcenter  = workbook.add_format({'align':'center','bold':True,'border':1})
            bcenterTitle  = workbook.add_format({'align':'center','bold':True,'border':1,'fg_color':'da6e03'})
            border = workbook.add_format({'border':1,'align':'center'})
            # Create a format to use in the merged range.
            merge_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': '007fff'})
            # Merge 3 cells.
            worksheet.merge_range('A1:C1', 'Experimento #'+str(len(os.listdir(os.getcwd()+"/Experiments"))+1), merge_format)
            trackname= raw_input("Ingrese nombre de pista: ")
            carname= raw_input("Ingrese nombre de carro: ")
            caracters = raw_input("Ingrese caracteristicas de la prueba: ")  
            worksheet.merge_range('B2:C2', trackname,border)
            worksheet.merge_range('B3:C3',carname,border)
            worksheet.merge_range('B4:C4',caracters,border)
            worksheet.write('A2', 'Track: ',bcenter)
            worksheet.write('A3', 'Car: ',bcenter)
            worksheet.write('A4','Caracteristicas:',bcenter)
            
            worksheet.write('A5','Parameter Name',bcenterTitle)
            worksheet.write('B5','Number of samples',bcenterTitle)
            worksheet.write('C5','Percentage',bcenterTitle)
            worksheet.set_column(0,0,30)
            worksheet.set_column(1,2,20)
            for j in range(8):
                worksheet.write('A'+str(6+j),vectorName[j],bcenter)
                worksheet.write('B'+str(6+j),vectorExp[j],centered)
                worksheet.write('C'+str(6+j),truediv(vectorExp[j]*100,self.samples),centered)
                
            worksheet.write_formula('C13','{=100-SUM(C6:C12)}',centered)
            workbook.close()
            np.savetxt("Experimento_1B.csv", self.matrix, delimiter=",")
        pass
    
    def onRestart(self):
        pass
