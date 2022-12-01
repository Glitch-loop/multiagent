'''
M2. Integradora


Authors:
Luis Alberto Alcántara Cabrales A01634185
Alexa Serrano Negrete A01654063
Renet de Jesús Pérez Gómez A01640555
Vicente Javier Viera Guízar A01639784

Date:
11/28/2022
'''

#Model
import agentpy as ap
import random


#Visualization
import matplotlib.pyplot as plt

import json

from flask import Flask

app = Flask(__name__)

parameters = {
    # Cantidad de carros
    'K': 5, 
    # Tamaño de ciudad
    'citySize': 60,
    # Origen de spwan
    'originSpawn': [],
    # Duración simulación
    'steps': 300,
}


class CarAgent(ap.Agent):
    def setup(self): 
        '''
        0 = left 
        1 = right
        2 = top
        3 = botton
        '''       
        self.idType = 0
        # self.idType = random.choice([0,1])
        self.initialIdType = 0
        self.carChoseAWay = 0
        self.wayChosen = 0
        self.activated = 1

    def determinateType(self, arrSpawmn):
        self.idType = random.choice(arrSpawmn)
        self.initialIdType = self.idType

class StreetAgent(ap.Agent):
    def setup(self):
       self.idType = 0

class TrafficLightAgent(ap.Agent):
    def setup(self):
        self.idType = 0
        self.timeCounterState = 0
        self.timeCounterWait = 0
        self.timeToStop = 10
        self.actualState = 0

    def determinateTime(self):
        if self.idType == 2 or self.idType == 3:
            self.timeCounterWait = self.timeToStop

    def updateState(self):
        self.actualState = 2 # Go
        if self.timeCounterWait > 0:
            #Time to wait
            self.timeCounterWait -= 1
            self.actualState = 4 # Stop
        else:
            #Time to work             
            if self.timeCounterState >= self.timeToStop - 3 and self.timeCounterState <= self.timeToStop - 1:
                self.actualState = 3 # Caution
            elif self.timeCounterState >= self.timeToStop:
                self.actualState = 4 # Stop
                self.timeCounterState = 0
                self.timeCounterWait = self.timeToStop
            self.timeCounterState += 1
        

    def currentState(self):
        return self.actualState
        
def initialPositionStreetsAndAssignType(self):
    # Assign type of street
    aux = 0
    typeOfStreet = 0
    for street in self.streets:
        if aux <= self.endEnviroment:
            street.idType = typeOfStreet
            aux += 1
        else:
            typeOfStreet += 1
            street.idType = typeOfStreet
            aux = 1

    # Get initial position
    position = []
    
    for i in range(self.endEnviroment):
        position.append((self.leftSideStreet, i))    
    position.append((self.leftSideStreet, self.endEnviroment))    

    for i in range(self.endEnviroment):
        position.append((self.rightSideStreet, i))
    position.append((self.rightSideStreet, self.endEnviroment))        
    
    for i in range(self.endEnviroment):
        position.append((i, self.rightSideStreet))
    position.append((self.endEnviroment, self.rightSideStreet))
    
    for i in range(self.endEnviroment):
        position.append((i, self.leftSideStreet))
    position.append((self.endEnviroment, self.leftSideStreet))
    
    return position

class MyModel(ap.Model):
    
    def setup(self):
        # Find special coordinates
        # Fundamental coordinates
        self.leftSideStreet = int(self.p.citySize / 2)
        self.rightSideStreet = self.leftSideStreet + 1
        self.endEnviroment = self.p.citySize - 1

        # Find the coordinates of center 
        self.centerCoordinates = [
            [self.rightSideStreet, self.leftSideStreet],
            [self.leftSideStreet, self.rightSideStreet],
            [self.leftSideStreet, self.leftSideStreet],
            [self.rightSideStreet, self.rightSideStreet],
        ]

        # Find crosswalk
        self.crosswalkCoordinates = [
            [self.rightSideStreet, self.leftSideStreet - 2],
            [self.leftSideStreet, self.rightSideStreet + 2],
            [self.leftSideStreet - 2, self.leftSideStreet],
            [self.rightSideStreet + 2, self.rightSideStreet],
        ]

        # Find initial positions
        self.initialPositionCoordinates = [
            [self.rightSideStreet, 0],
            [self.leftSideStreet, self.endEnviroment],
            [0, self.leftSideStreet],
            [self.endEnviroment, self.rightSideStreet]
        ]

        # Find final positions
        self.finalPositionCoordinates = [
            [self.rightSideStreet, self.endEnviroment],
            [self.leftSideStreet, 0],
            [self.endEnviroment, self.leftSideStreet],
            [0, self.rightSideStreet]
        ]
        
        # Store type of movement
        self.move = [
            [0, 1], [0, -1], [1, 0], [-1, 0],
            [-1, 1], [1, -1], [1, 1], [-1, -1]
        ]

        # We store this to query in the semaphore (This is the only decision that you can ignore the state of the semaphore)
        self.rightSides = [2, 3, 1, 0]

        self.leftSides = [3, 2, 0, 1]

        # Create agents
        self.cars = ap.AgentList(self, self.p.K, CarAgent)
        self.streets = ap.AgentList(self, int(self.p.citySize * 4), StreetAgent)
        self.trafficLights = ap.AgentList(self, 4, TrafficLightAgent)
        

        # Create enviroment
        self.area = ap.Grid(self, [self.p.citySize] * 2)


        # Add agents to the enviroment
        # Cars 
        # Determinate type of car
        for car in self.cars:
            car.determinateType(self.p.originSpawn)

        # Determinate positions
        positionCars = []
        for car in self.cars:
            positionCars.append(self.initialPositionCoordinates[car.idType])
            
        self.area.add_agents(self.cars, positionCars)
        
        # Street
        positionStreet = initialPositionStreetsAndAssignType(self)
        # self.area.add_agents(self.streets, positionStreet)
        
        #trafficLights - fix the positions
        '''
            The position in the grid of the traffic light doesn't import 
            it's more about decoration. The position in the "array" 
            is what really really
        '''
        positionTrafficLight = [
            [self.crosswalkCoordinates[3][0] - 1, self.crosswalkCoordinates[3][1] + 2], # Traffic light for street 0
            [self.crosswalkCoordinates[2][0] + 1, self.crosswalkCoordinates[2][1] - 2], # Traffic light for street 1
            [self.crosswalkCoordinates[0][0] + 2, self.crosswalkCoordinates[0][1] + 1], # Traffic light for street 2
            [self.crosswalkCoordinates[1][0] - 2, self.crosswalkCoordinates[1][1] - 1], # Traffic light for street 3
        ]

        self.area.add_agents(self.trafficLights, positionTrafficLight)
        
        #Assign the type of traffic light and its time to works
        counterTrafficLight = 0
        for trafficLight in self.trafficLights:
            trafficLight.idType = counterTrafficLight
            trafficLight.determinateTime()
            counterTrafficLight += 1


        # Define type of agent
        self.cars.agent_type = 0
        self.streets.agent_type = 1
        for trafficLight in self.trafficLights:
            if trafficLight.idType == 0 or trafficLight.idType == 1:
                trafficLight.agent_type = 2 # That type of traffic light start in "Green"
            elif trafficLight.idType == 2 or trafficLight.idType == 3:
                trafficLight.agent_type = 4 # That type of traffic light start in "Red"      

    def step(self):
        # Update state of the traffic lights
        for trafficLight in self.trafficLights:
            trafficLight.updateState()
            trafficLight.agent_type = trafficLight.currentState()
            self.record("TL" + str(trafficLight.id), {"state": trafficLight.agent_type})

        for car in self.cars:
            [crossY, crossX] = self.crosswalkCoordinates[car.initialIdType]
            [yCar, xCar] = self.area.positions[car]
            trafficLightState = self.trafficLights[car.initialIdType].currentState()
            stop = 0
            carInFront = 0
            diagonalMovement = 1
            
            # If the current agent (car) reach the crosswalk, then, it going to choose a way
            if (self.crosswalkCoordinates[car.initialIdType][0] == yCar
                and self.crosswalkCoordinates[car.initialIdType][1] == xCar
                and car.carChoseAWay == 0):
                    if car.initialIdType == 0:
                        car.wayChosen = random.choice([0, 2, 3])
                        
                    if car.initialIdType == 1:
                        car.wayChosen = random.choice([1, 2, 3])
                        
                    if car.initialIdType == 2:
                        car.wayChosen = random.choice([0, 1, 2])
                        
                    if car.initialIdType == 3:
                        car.wayChosen = random.choice([0, 1, 3])
                        
                    car.carChoseAWay = 1 # This attribute helps us prevent the car from choose a way again

            # Check if it is necessary for the agent to stop
            # The agent is at the crosswalk, the traffic light is stopped and the agent won't go to the "right"
            if(yCar == crossY and crossX == xCar and trafficLightState != 2 
            and self.rightSides[car.initialIdType] != car.wayChosen):
                stop = 1
            
            # Verify if the car reach the center (and the agent won't go to the left)
            [yCoor, xCoor] = self.centerCoordinates[car.initialIdType]
            if yCoor == yCar and xCoor == xCar and self.leftSides[car.initialIdType] != car.wayChosen:
                car.idType = car.wayChosen # Change direction

            if stop == 0:
                # Verify if there's a neighbor type car    
                for neighbor in self.area.neighbors(car):
                    # Verify if there's a neighbor car
                    if neighbor.agent_type == 0:   
                        [yNeighbor, xNeighbor] = self.area.positions[neighbor]
                        # Calculate "value movement" of the car
                        posY = yNeighbor - yCar
                        posX = xNeighbor - xCar 
                        [movY, movX] = self.move[car.idType] # Get value movement
                        
                        # Check forward movement
                        if (movY == posY and movX == posX):
                            carInFront = 1
                        
                        # Check left movement (special if the agent can do a diagonal movement)
                        [movY, movX] = self.move[car.idType + 4] # Get the rate value of the movement
                        if (movY == posY and movX == posX):
                            # Agent can't do a diagonal movememnt becasue there is another agent
                            diagonalMovement = 0 
                        else:
                            # Agent can do a diagonal movement because there isn't an agent 
                            diagonalMovement = 1

                # In case that the car is in the center and has a decision to go to the left
                if yCoor == yCar and xCoor == xCar and self.leftSides[car.initialIdType] == car.wayChosen:
                    [movY, movX] = self.move[car.idType + 4]
                    if diagonalMovement == 1: # Diagonal movement
                        self.area.move_by(car, self.move[car.idType + 4])                        
                    else: # "L" movement
                        # Check if there is an agent in front of our current car
                        if carInFront == 0:
                            self.area.move_by(car, self.move[car.idType])
                    car.idType = car.wayChosen # Change direction
                    carInFront = 1 
                    
                # Move the car (towards and right option)
                if carInFront == 0:   
                    self.area.move_by(car, self.move[car.idType])

            [y, x] = self.area.positions[car]
            self.record(car.id, {'x': x, 'y': y, 'activated': car.activated} )

            # Verify if the car reached the destination coordinates 
            [currentY, currentX] = self.area.positions[car]
            [destinationY, destinationX] = self.finalPositionCoordinates[car.idType]
            if currentY == destinationY and destinationX == currentX:
                car.agent_type = 1
                car.activated = 0
 
        # If there's not an agent car of type 0 then we finish the simulation
        finishSimulation = 1
        for car in self.cars: 
            if car.agent_type == 0:
                finishSimulation = 0
                break
        if finishSimulation == 1:
            self.stop()
            
#Server
'''
If an empty array is passed, an array with all the options is automatically passed.
If you pass an invalid option, then ignore it.
Also, if a number is repeated then ignore it.
'''
@app.route('/<carAmount>&<originSpwan>')
def principal(carAmount, originSpwan):
    carAmount = int(carAmount)
    originSpwan = json.loads(originSpwan)

    if carAmount < 5:
        carAmount = 5

    parameters['K'] = carAmount
    
    parameters['originSpawn'] = []

    for i in originSpwan:
        if(i == 0 or i == 1 or i == 2 or i == 3):
            append = 1
            for repited in parameters['originSpawn']:
                if i == repited:
                    append = 0 
            if append == 1:
                parameters['originSpawn'].append(i)
    
    if parameters['originSpawn'] == []:
        parameters['originSpawn'] = [0, 1, 2, 3]
    
    model = MyModel(parameters)
    result = model.run()

    carsMovements = {}

    # Get number of variables (cars)
    totalCars = 0 
    for i in result.variables.MyModel:
        totalCars += 1

    totalCars -= 4 # Substract 4 that are the 4 traffic light
    carsMovements["totalCars"] = totalCars
    carsMovements["trafficLights"] = {}
    carsMovements["cars"] = {}

    trafficLights = 0
    for i in result.variables.MyModel:
        if trafficLights < 4:
            carsMovements["trafficLights"][i] = []
        else:
            carsMovements["cars"][i] = []
        for movement in result.variables.MyModel[i]:
            if trafficLights < 4:
                carsMovements["trafficLights"][i].append(movement)
            else:
                carsMovements["cars"][i].append(movement)
        trafficLights += 1
        #a
    return str(carsMovements)

# Run server command:
# If you want to run the server locally go to the level of the dir "server" and execute the comand below: 
# flask --app integradora_2.py run
