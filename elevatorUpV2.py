from numpy import random
import numpy as np
import math
from AVL_TREE import AVL_Tree
import collections


class Elevator():
    def __init__(self):
        self.location = 0
        self.people = []

class Event():
    def __init__(self, time, eventType,extra):
        self.time = time
        self.eventType = eventType
        self.extra = extra
    def __lt__(self,other):
        if (self.time < other.time):
            return True
        else:
            return False
    def __eq__(self,other):
        if self.time == other.time:
            return True
        return False
    def __repr__(self):
        return str(self.eventType)+" t:"+str(self.time)

class Person():
    def __init__(self,arrivalTime,destination):
        self.arrivalTime = arrivalTime
        self.destination = destination
        self.destinationTime = 0
    def calcDelay():
        tOpt = 3+3+elevatorSpeed(0,destination)
        t = destinationTime - arrivalTime
        return (t-tOpt)/tOpt
    def __lt__(self,other):
        if (self.destination < other.destination):
            return True
        else:
            return False
    def getDelay(self,t):
        timeTaken = t-self.arrivalTime
        timeOpt = 3+3+elevatorSpeed(0,self.destination)
        return (timeTaken - timeOpt) / timeOpt


def doorTime(n):    # Amount of time it takes for an elevator to close its door with n people using it
    return [3,5,7,9,11,13,15,17,19,22][n-1]

def elevatorSpeed(floorStart,floorEnd): # Time it takes for elevator to get from floorStart to floorEnd
    h = abs(floorStart - floorEnd)
    if h == 1:
        return 8
    else:
        return 2*8 + 5*(h-2)

def groupNumber(u, maxGroupNumber):
    return cdfModificationAndSearch(u,maxGroupNumber)

def interarrivalTime(u):
    return constrainedInversion(u)

def assignFloor(u, floorCount):
    t = 0
    for i in floorCount:
        if i>0:
            t += 1
    j = int(u*t+1)
    for floor in range(len(floorCount)):
        if floorCount[floor]>0:
            j -= 1
            if j==0:
                return floor

def geometricDistribution(x):
    p = 0.65
    return 1-math.pow(p,x+1)

def getFt(d,alpha,beta):
    return ( geometricDistribution(d) - alpha ) / (beta - alpha)

def cdfModificationAndSearch(u,b):
    # Get a number between 1 and 8
    a = 1
    alpha = geometricDistribution(a-1)
    beta = geometricDistribution(b)
    # TODO check if its b+a or b-a
    d = int((b+a)//2)
    if getFt(d,alpha,beta) <= u:
        while getFt(d,alpha,beta) <= u:
            d += 1
    elif getFt(b,alpha,beta) >= u:
        while getFt(d-1,alpha,beta) > u:
            d -= 1
    else:
        d = a
    return d

def exponentialDistribution(x):
    mu = 10
    return 1-math.pow(math.e,(-x/mu))


def idfExponential(u):
    mu = 10
    rv = -mu*np.log(1-u)
    return rv


def constrainedInversion(u):
    a = 2
    b = 90
    alpha = exponentialDistribution(a)
    beta = 1.0-exponentialDistribution(b)
    u = (u * (1-beta-alpha)) + alpha
    d = idfExponential(u)
    return d

def getRandom():
    return 0.70
    global uniforms
    line = uniforms.readline()
    try:
        return float(line)
    except:
        print("Random Uniform was not found.")
        exit(1)


def run1day(floors, elevatorNum, uniformFileName, days):
    global uniforms
    try:
        uniforms = open(uniformFileName,"r")
    except:
        print("Random File not found")
        exit(1)

    verbose = True
    khVerbose = False

    # Stat collections
    stops = 0
    maxq = 0
    avgDelay = 0
    vDelay = 0
    statCounter = 0

    for day in range(days):
        # Helper Variables
        t = 0
        lobby = []
        peoplePerFloor = 100
        floorCount = [0]
        for i in range(floors):
            floorCount.append(peoplePerFloor)
        peopleToDeliver = peoplePerFloor * floors

        elevators = []
        for i in range(elevatorNum):
            newElevator = Elevator()
            elevators.append(newElevator)

        currentEvents = []

        # EVENT QUEUE SET UP
        nextEvent = Event(interarrivalTime(getRandom()),"PedArrival",None)
        eventQueue = []
        eventQueue.append(nextEvent)
        tree = AVL_Tree()
        root = None
        root = tree.insert(root, t, len(eventQueue)-1)

        # while root != None:
        while len(eventQueue) > 0:
            # for index in currentEvents:
            #     if eventQueue[index].time == 2078:
            #         print("LOOK HERE ===============================================================")
            #         print(eventQueue[index].eventType)
            # if len(currentEvents) == 0:
            #     node = tree.getSmallestRoot(root)
            #     if node.val == 2078: print("2078 NODE")
            #     for index in node.index:
            #         currentEvents.append(index)
            #     root = tree.delete(root, node.val)



            # event = eventQueue[currentEvents[0]]
            # currentEvents.pop(0)
            # t = event.time

            eventQueue.sort()
            event = eventQueue[0]
            eventQueue.pop(0)
            t = event.time

            if event.eventType == "PedArrival":
                freeElevators = []
                for i in range(len(elevators)):
                    if elevators[i].location == 0:
                        freeElevators.append(i)
                newRiders = []
                gn = groupNumber(getRandom(),8 if peopleToDeliver >= 8 else peopleToDeliver)
                if verbose: print(f'Pedestrians Arriving t:{t/60} Size: {gn}')
                if khVerbose: print(f'     {t/60}m arrival->lift ped 1 arrival {t/60}m destination floor 15')
                if verbose: print(f'    Going to floors', end=" ")
                for i in range(gn):
                    destination = assignFloor(getRandom(), floorCount)
                    newRider = Person(t,destination)
                    floorCount[destination] -= 1
                    peopleToDeliver -= 1
                    newRiders.append(newRider)
                    if verbose: print(f'{destination}',end=" ")
                if verbose: print("")
                if len(freeElevators) == 0:
                    for rider in newRiders:
                        lobby.append(rider)
                elif len(freeElevators) == 1:   
                    # Fill the one elevator w/ all people
                    elevators[freeElevators[0]].people = newRiders
                    # Send elevator up to first floor
                    elevators[freeElevators[0]].people.sort()
                    destinationFloor = elevators[freeElevators[0]].people[0].destination
                    newEvent = Event( t + doorTime(len(elevators[freeElevators[0]].people))+elevatorSpeed(0,destinationFloor), "ElevatorArrive", freeElevators[0])
                    eventQueue.append(newEvent)
                    root = tree.insert(root, newEvent.time, len(eventQueue)-1)
                    elevators[freeElevators[0]].location = destinationFloor
                else:
                    while len(newRiders) > 0: # Fill the elevators with people RR style
                        for index in freeElevators:
                            if len(newRiders) > 0:
                                elevators[index].people.append(newRiders[0])
                                newRiders.pop(0)
                            else:
                                break
                    for index in freeElevators:
                        # Send elevators up to floor
                        if len(elevators[index].people) > 0:
                            elevators[index].people.sort()
                            destinationFloor = elevators[index].people[0].destination
                            newEvent = Event( t + doorTime(len(elevators[index].people))+elevatorSpeed(0,destinationFloor), "ElevatorArrive", index)
                            eventQueue.append(newEvent)
                            root = tree.insert(root, newEvent.time, len(eventQueue)-1)
                            elevators[index].location = destinationFloor
                # Start another Pedestrian Arrival Event
                if peopleToDeliver > 0:
                    newEvent = Event(t+interarrivalTime(getRandom()), "PedArrival", None)
                    eventQueue.append(newEvent)
                    root = tree.insert(root, newEvent.time, len(eventQueue)-1)
                if maxq < len(lobby):
                    maxq = len(lobby)
            elif event.eventType == "ElevatorArrive":
                stops += 1
                # If at lobby, check if people are in line
                if elevators[event.extra].location==-1:
                    elevators[event.extra].location = 0
                    if len(lobby) > 0:
                        for i in range(10):
                            if len(lobby) > 0:
                                elevators[event.extra].people.append(lobby[0])
                                lobby.pop(0)
                        elevators[event.extra].people.sort()
                        destinationFloor = elevators[event.extra].people[0].destination
                        newEvent = Event( t + doorTime(len(elevators[event.extra].people))+elevatorSpeed(elevators[event.extra].location,destinationFloor), "ElevatorArrive", event.extra)
                        eventQueue.append(newEvent)
                        root = tree.insert(root, newEvent.time, len(eventQueue)-1)
                        elevators[event.extra].location = destinationFloor
                        if verbose: print(f'Elevator {event.extra} has arrived to Lobby. Bringing {len(elevators[event.extra].people)} people up to {elevators[event.extra].location} t:{t/60}')
                    else:
                        if verbose: print(f'Elevator {event.extra} has arrived to Lobby. No one in queue. t:{t/60}')
                # Not Lobby
                else:
                    if verbose: print(f'Elevator {event.extra} has arrived to {elevators[event.extra].location} with {len(elevators[event.extra].people)} people t:{t/60}')
                    # Drop People Off
                    count = 0
                    humanBeans = []
                    for i in range(len(elevators[event.extra].people)):
                        if elevators[event.extra].people[0].destination == elevators[event.extra].location:
                            humanBeans.append(elevators[event.extra].people.pop(0))
                            count += 1
                        else:
                            break
                    dt = doorTime(count)
                    for human in humanBeans:
                        # Calculate delay stats here
                        delay = human.getDelay(t+dt)
                        # if verbose: print(f'    delay={delay}')
                        statCounter += 1
                        # Welford's Standard Deviation
                        # vi     =   vi-1   + i-1/i                           * (x - x_bar-1)**2
                        vDelay = vDelay + (statCounter - 1) / statCounter * (delay-avgDelay)**2
                        # Welford's Average
                        # xi     =  xi-1    + 1/i            *   x       - x_bar-1
                        avgDelay = avgDelay + (1/statCounter) * (delay - avgDelay)
                    if verbose: print(f'    {count} People got off')
                    # If More People, Go Up
                    if len(elevators[event.extra].people) > 0:
                        destinationFloor = elevators[event.extra].people[0].destination
                        newEvent = Event( t + doorTime(count)+elevatorSpeed(elevators[event.extra].location,destinationFloor), "ElevatorArrive", event.extra)
                        eventQueue.append(newEvent)
                        root = tree.insert(root, newEvent.time, len(eventQueue)-1)
                        elevators[event.extra].location = destinationFloor
                    # If No People, Go To Lobby
                    else:
                        destinationFloor = 0
                        newEvent = Event( t + doorTime(count)+elevatorSpeed(elevators[event.extra].location,destinationFloor), "ElevatorArrive", event.extra)
                        eventQueue.append(newEvent)
                        root = tree.insert(root, newEvent.time, len(eventQueue)-1)
                        elevators[event.extra].location = -1 # Set to -1 to indicate it is travelling to 0 and people can't get on until it reaches 0
        if verbose: print(f'==== Day {day+1} Complete ====')

    print(f'OUTPUT stops  {stops/days/elevatorNum}')
    print(f'OUTPUT max qsize {maxq}')
    print(f'OUTPUT average delay {avgDelay}')
    print(f'OUTPUT stddev delay {math.sqrt(vDelay/statCounter)}')

# run1day(20,4,"uniform-0-1-00.dat", 1) # Floors, Elevators, random file, days
def runProgram(floors, elevators, randomFileName, days):
    run1day(floors, elevators, randomFileName, days)



