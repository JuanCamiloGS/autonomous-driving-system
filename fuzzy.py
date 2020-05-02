import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np

class Fuzzy(object):

	def __init__(self):
		# New Antecedent/Consequent objects hold universe variables and membership
                # functions
                frontS = ctrl.Antecedent(np.arange(0,201,1),'frontS')
                velocity = ctrl.Antecedent(np.arange(0, 131, 1), 'velocity')
                accelC = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'accelC')
                brake = ctrl.Consequent(np.arange(0,1.1,0.1),'brake')
                self.BrakeUniverse = brake
                self.AccelUniverse = accelC
                # Auto-membership function population is possible with .automf(3, 5, or 7)
                #service.automf(3)

                # Custom membership functions can be built interactively with a familiar,
                # Pythonic API
                frontS['muy cerca']  = fuzz.trimf(frontS.universe,[0,0,20])
                frontS['cerca']      = fuzz.trimf(frontS.universe,[20,30,50])
                frontS['intermedio'] = fuzz.trimf(frontS.universe,[30,90,150]) #OK
                frontS['lejos']      = fuzz.trimf(frontS.universe,[90,200,200]) #OK

                velocity['baja'] = fuzz.trimf(velocity.universe,[0,0,40])
                velocity['media'] = fuzz.trimf(velocity.universe,[40,60,90]) 
                velocity['alta']= fuzz.trimf(velocity.universe,[70,90,110]) #OK
                velocity['muy alta']=fuzz.trimf(velocity.universe,[90,130,130]) #OK

                accelC['no gas'] = fuzz.trimf(accelC.universe,[0,0,0.3]) #OK
                accelC['mid gas'] = fuzz.trimf(accelC.universe, [0.1, 0.2, 0.5]) #OK
                accelC['gas'] = fuzz.trimf(accelC.universe,[0.3,0.4,0.7]) #OK
                accelC['full gas'] = fuzz.trapmf(accelC.universe, [0.5, 0.8, 1,1]) #OK
                #ACCEL IS OK

                brake['no brake'] = fuzz.trimf(brake.universe,[0,0,0.1]) #OK
                brake['mid brake'] = fuzz.trimf(brake.universe, [0,0.3,0.5]) #OK
                brake['full brake'] = fuzz.trapmf(brake.universe, [0.3, 0.8,1,1]) #OK

                rule1 = ctrl.Rule(frontS['lejos']|frontS['intermedio'], accelC['full gas'])
                rule2 = ctrl.Rule(frontS['lejos'] & (velocity['muy alta'] | velocity['alta']), accelC['mid gas'])
                rule3 = ctrl.Rule((frontS['lejos']|frontS['intermedio']),brake['no brake'])
                
                rule4 = ctrl.Rule(frontS['intermedio'] & velocity['alta'] ,accelC['mid gas'])
                rule5 = ctrl.Rule(frontS['intermedio'] & velocity['muy alta'], accelC['gas'])
                
                            
                rule6 = ctrl.Rule(frontS['intermedio'] & velocity['muy alta'], brake['mid brake'])
                
                rule7 = ctrl.Rule( (frontS['cerca'] | frontS['muy cerca']), accelC['gas'])
                rule8 = ctrl.Rule((frontS['cerca'] | frontS['muy cerca']) & (velocity['alta'] | velocity['muy alta']), accelC['no gas'])
                
                
                rule9 = ctrl.Rule((frontS['cerca'] | frontS['muy cerca']), brake['no brake'])
                rule10 = ctrl.Rule(frontS['cerca'] & velocity['alta'], brake['mid brake'])
                rule11 = ctrl.Rule(frontS['cerca'] & velocity['muy alta'], brake['full brake'])
                
                
                rule12 = ctrl.Rule(frontS['muy cerca'] & (velocity['muy alta']|velocity['alta']), brake['full brake'])
                rule13 = ctrl.Rule(frontS['muy cerca'] & velocity['media'], brake['mid brake'])
                

                """

                Control System Creation and Simulation
                ---------------------------------------

                Now that we have our rules defined, we can simply create a control system
                via:-
                """
                self.accel_ctrl = ctrl.ControlSystem([rule1, rule2,rule4,rule5,rule7,rule8])
                self.brake_ctrl = ctrl.ControlSystem([rule3,rule6,rule9,rule10,rule11,rule12,rule13])
                self.Acc = None
                self.Brk = None

        def PredictPedals(self, frontS, velocity):
                acceleration = ctrl.ControlSystemSimulation(self.accel_ctrl)
                brakes = ctrl.ControlSystemSimulation(self.brake_ctrl)
                acceleration.input['frontS'] = frontS
                brakes.input['frontS'] = frontS
                acceleration.input['velocity'] = velocity
                brakes.input['velocity'] = velocity
                
                self.Acc = acceleration
                self.Brk = brakes
                
                acceleration.compute()
                brakes.compute()
                
                valA = acceleration.output['accelC']
                valB = brakes.output['brake']
                return [valA, valB]