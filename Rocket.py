"""
Rocket Simulator
by Nicholas Gower

This program allows the user to enter initial conditions for a rocket launch, and draws a graph
showing the altitude of the rocket over time.

To Do:
Air resistance
Parachutes
More planet options

"""
import time as timeLib
import numpy
import matplotlib.pyplot as plt
# -*- coding: utf-8 -*-

def cleanPrompt(prompt,length,fillChar=" "): #Delivers a prompt to the user
    #while (len(prompt)<length):prompt+=" "
    prompt=uniform(prompt,length,fillChar)+">>>"
    toReturn=""
    while (toReturn==""): #Asks for input until input is given
        toReturn=input(prompt)
    while (toReturn[0]==" "): #Removes spaces from beginning of string until no spaces are at beginning
        toReturn=toReturn[1:len(toReturn)]
    while ((toReturn[len(toReturn)-1])==" "): #Removes spaces from end of string until no spaces are at end
        toReturn=toReturn[0:len(toReturn)-1]
    return toReturn
    
def uniform(string,length,fillChar=" "): #Adds fillChar to string until string is "length" long
   #while (len(string)<length):string+=" "
    return string+fillChar*(length-len(string)) 
    
def inputBool(string): #Converts multiple ways of expressing bool in string to bool
    trueList=["yes","y","1","true","t"] #List of acceptable true statements
    falseList=["no","n","0","false","f"] #List of acceptable false statements
    
    if (string in trueList): #Checks if input string equals any strings in trueList
        return True
    elif (string in falseList):
        return False
    else:
        return False
#Rocket ship

fuel={'energy':5000,'mass':1} #energy measured in Newtons, mass in kg
#planet={'diameter':}
def vectorSum(vec1,vec2): #Both vectors must have same number of dimensions
    out=[]
    for x in range(len(vec1)):
        out.append(vec1[x]+vec2[x])
    return out

def vectorEval(vec1,vec2,operator="+"):
    out=[]
    for x in range(len(vec1)):
        out.append(eval('vec1[x]{}vec2[x]'.format(operator)))
    return out
def celcius(temp):
    return temp+273.15
class rocket:
    def __init__(self):
        self.position=[0,0,0] #meters
        self.velocity=[0,0,0] #meters/second
        self.acceleration=[0,0,0] #meters/mecond^2
        self.fuel=0.0 #seconds of fuel left
        self.isBurning=False
        self.emptyMass=100 #Mass in kg when rocket has no fuel
        self.temp=celcius(20)
        self.HP=1000.0 #Hit Points
        self.gravity=[0,0,-9.8]
        self.localGravity=self.gravity[2]*(6371009/(6371009+self.position[2]))
        self.interpolateTimer=0
        self.historyZ=[]
        self.historyT=[]
        self.time=0
    def refuel(self,value):
        self.fuel+=value
    
    def update(self, deltaTime,elapsedTime):
        self.time=elapsedTime
        self.interpolateTimer+=deltaTime
        if self.interpolateTimer>1:   
            self.interpolateTimer=0
            self.localGravity=self.gravity[2]*(6371009/(6371009+self.position[2])) #Updates local gravity once per second
        self.mass=self.emptyMass+self.fuel*fuel['mass'] #As fuel burns, rocket gets lighter, meaning acceleration increases
        self.thrust=fuel['energy']/self.mass #m kg/s^2
        self.velocity=vectorEval(self.velocity,vectorEval([deltaTime,deltaTime,deltaTime],self.acceleration,'*')) #velocity=velocity+acceleration
        self.position=vectorEval(self.position,vectorEval([deltaTime,deltaTime,deltaTime],self.velocity,'*')) #position=position+velocity
        if self.position[2]<0:
            self.position[2]=0
            self.velocity[2]=0
        if self.fuel>0 and self.isBurning:
            self.fuel=self.fuel-deltaTime
            if self.fuel<=0:
                self.isBurning=False
                self.fuel=0
            self.acceleration[2]=self.thrust+self.localGravity
        
        else:
            self.acceleration[2]=self.localGravity
        self.historyZ.append(self.position[2])
        self.historyT.append(self.time)
        
    def dispData(self,elapsedTime):
        
        print('position',self.position)
        print('velocity',self.velocity)
        print('acceleration',self.acceleration)
        print('fuel',self.fuel)
        print('mass',self.mass)
        print("time",elapsedTime)
        
        print(self.isBurning)
    def launch(self):
        self.isBurning=True
    def graphFlightPath(self):
        plt.plot(self.historyT,self.historyZ)
        plt.title('Rocket\'s flight path')
        plt.xlabel('Elapsed Time(s)')
        plt.ylabel('Altitude(m)')
        plt.xlim(xmin=0,xmax=max(self.historyT))
        plt.ylim(ymin=0,ymax=1.1*max(self.historyZ))
        plt.grid(True)
        plt.show()
        
def initialConditions(style='terminal'):
    def prompt(prompt):
        return cleanPrompt(prompt,55)
    conditions={}
    if style=='terminal':
        conditions["mass"]=float(prompt("What is the mass of your rocket?"))
        conditions["fuel"]=float(prompt("How many kg of fuel do you want in your rocket?"))
        conditions["fuelDensity"]=float(prompt("How energy-dense is your fuel, in newtons/kg?"))
        conditions["planet"]=prompt("What planet/moon are you launching from?")
    return conditions
class planet:
    #While this class is called "planet," it can be used to get data about moons as well.
    #Source:https://nssdc.gsfc.nasa.gov/planetary/factsheet/
    def __init__(self,planetName):
        planetData={}
        planetNames="MERCURY VENUS EARTH LUNA MARS JUPITER SATURN URANUS NEPTUNE PLUTO ".split()
        planetDiameter="4879 12104 12756 3475 6792 142984 120536 51118 49528 2370".split() #Diameter measured in km
        planetGravity="3.7 8.9 9.8 1.6 3.7 23.1 9.0 8.7 11.0 0.7".split()
        for x in range(len(planetNames)):
            planetData[planetNames[x]]={'diameter':planetDiameter[x],'gravity':planetGravity[x]}
        if planetName.upper()=="MOON":
            planetName="LUNA"
        planetName=planetName.upper() 
        if planetName not in planetData:
            print("Planet Not Availiable.")
        else:
            planet=planetData[planetName]
            self.diameter=float(planet["diameter"])
            self.gravity=float(planet['gravity'])
        
    
def main():
    initialCondition=initialConditions()
    currentPlanet=planet(initialCondition["planet"])
    fuel["energy"]=initialCondition["fuelDensity"]
    redRocket=rocket() #Creates red rocket
    redRocket.gravity=[0,0,-currentPlanet.gravity]
    redRocket.emptyMass=initialCondition["mass"]
    redRocket.refuel(float(initialCondition["fuel"])) #Adds fuel to Red Rocket
    redRocket.launch() #Launches red rocket
    elapsedTime=0.0
    deltaTime=(1)
    print("Diameter",currentPlanet.diameter)
    print("gravity",currentPlanet.gravity)
    while redRocket.position[2]!=0 or redRocket.fuel>0:
        #tempTime=time
        #time+=time.process_time()
        #deltaTime=time-tempTime
       # timeLib.sleep(deltaTime/1000)
        elapsedTime+=deltaTime
        redRocket.update(deltaTime,elapsedTime)
        
        #redRocket.dispData(elapsedTime)
    #print(redRocket.historyZ)
    redRocket.graphFlightPath()

main()
