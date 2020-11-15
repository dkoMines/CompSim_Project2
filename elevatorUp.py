from numpy import random

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

def doorTime(n):
	return [3,5,7,9,11,13,15,17,19,22][n-1]

def elevatorSpeed(floorStart,floorEnd):
	h = abs(floorStart - floorEnd)
	if h == 1:
		return 8
	else:
		return 2*8 + 5*(h-2)

def assignFloor(floorCount):
	t = 0
	for i in floorCount:
		if i>0:
			t += 1
	j = int(random.uniform(0.0,t)) + 1
	for floor in range(len(floorCount)):
		if floorCount[floor]>0:
			j -= 1
			if j==0:
				return floor+1



def runOneDay(floors, elevatorNum, randomFile, days2Run):
	# __init__ialize Variables
	t = 0
	eventQueue = []
	pedestrianQueue = []
	ppf = 100 # People per floor
	floorCount = []
	for i in range(floors):
		floorCount.append(ppf)
	ppd = ppf*floors # People per day

	elevators = []
	for i in range(elevatorNum):
		newElevator = Elevator()
		elevators.append(newElevator)

	# Stat variables
	stops = 0
	maxWait = 0
	avgDelay = 0
	sdDelay = 0	

	v = True

	newEvent = Event(0,"PedArrival",0)
	eventQueue.append(newEvent)

	while ppd > 0 and len(eventQueue) > 0:
		eventQueue.sort()
		event = eventQueue[0]
		eventQueue.pop(0)
		t = event.time

		# System Events
		if (event.eventType == "PedArrival"): # A group of pedestrians arrive. They wait for elevator
			if v: print(f'Group of Pedestirans Arrived. Time: {t}')
			groupSize = 1
			for i in range(groupSize):
				targetFloor = assignFloor(floorCount)
				floorCount[targetFloor-1] -= 1
				ppd -= 1
				newPerson = Person(t,targetFloor)
				pedestrianQueue.append(newPerson)
			# if not last pedestrian...
			if ppd > 0:
				interArrivalTime = 5
				newEvent = Event(t+interArrivalTime,"PedArrival",0)
				eventQueue.append(newEvent)
			# If elevator available
			evs = []
			indexAvail = []
			j = 0
			for eI in range(len(elevators)):
				if elevators[eI].location == 0:
					indexAvail.append(eI)
					evs.append([])
			for i in range(len(indexAvail)*10):
				if len(pedestrianQueue) > 0:
					evs[j].append(pedestrianQueue[0])
					pedestrianQueue.pop(0)
					if j < len(indexAvail):
						j += 1
					else:
						j = 0
			for i in indexAvail:
				elevators[i].people = evs[0]
				evs.pop(0)
				newEvent = Event(t+doorTime(len(elevators[i].people)),"ElevatorDoorClosed",i)
				eventQueue.append(newEvent)
					

		elif (event.eventType == "ElevatorArrival"): # The elevator has arrived to a floor. People need to get on or off
			if v: print(f'Elevator Arrived. Time: {t}')
			if len(elevators[event.extra].people)>0: # People need to get off
				numPeople = 0
				elevators[event.extra].people.sort()
				for p in elevators[event.extra].people:
					if p.destination == elevators[event.extra].location:
						numPeople += 1
				for i in range(numPeople):
					elevators[event.extra].people.pop(0)
				newEvent = Event(t+doorTime(numPeople),"ElevatorDoorClosed",event.extra)
				eventQueue.append(newEvent)

			if elevators[event.extra].location==0: # Elevator arrived in lobby
				numPassengers = len(pedestrianQueue) if len(pedestrianQueue) < 10 else 10
				pedestrianQueue.sort()
				for i in range(numPassengers):
					elevators[event.extra].people.append(pedestrianQueue[0])
					pedestrianQueue.pop(0)
				elevators[event.extra].people.sort()
				newEvent = Event(t+doorTime(numPassengers),"ElevatorDoorClosed",event.extra)
				eventQueue.append(newEvent)

		elif (event.eventType == "ElevatorDoorClosed"): # This event is for when people get on or off an elevator
			if v: print(f'Elevator Door Closed. Time: {t}')
			if len(elevators[event.extra].people)>0: # Go to floor w/ next person
				elevators[event.extra].people.sort()
				targetFloor = elevators[event.extra].people[0].destination
				newEvent = Event(t+elevatorSpeed(elevators[event.extra].location,targetFloor),"ElevatorArrival",event.extra)
				eventQueue.append(newEvent)
			else:									# Go back to lobby
				newEvent = Event(t+elevatorSpeed(elevators[event.extra].location,0),"ElevatorArrival",event.extra)
				eventQueue.append(newEvent)

runOneDay(1, 1, "randomFile", 1)