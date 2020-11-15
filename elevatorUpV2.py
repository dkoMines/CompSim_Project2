from numpy import random

# BST Stuff
class Node: 
    def __init__(self, key): 
        self.left = None
        self.right = None
        self.val = [key]
    def len():
    	if root == None:
    		return 1
    	return self.left.len()+self.right.len()+1

def insert(root, key): 
    if root is None: 
        return Node([key]) 
    else: 
        if root.val == key:
        	root.val.append(key) 
            return root 
        elif root.val < key: 
            root.right = insert(root.right, key) 
        else: 
            root.left = insert(root.left, key) 
    return root 

def getNextEventNode(node,t):
	if node == None:
		return None
	if node[0].time < t: # event t is too low
		return getNextEvent(node.right, t)
	elif node[0].time == t: # must choose event from here
		return node
	else: # Can choose event from here
		lNode = getNextEvent(node.left, t)
		if lNode == None:
			return Node
		else:
			return lNode

class Elevator():
	def __init__(self):
		self.location = 0
		self.people = []

class Event():
	def __init__(self, time, eventType,extra):
		self.time = time
		self.eventType = eventType
		self.extra = extra
		self.completed = False
	def __lt__(self,other):
		if (self.time < other.time):
			return True
		else:
			return False
	def __eq__(self,other):
		if self.time == other.time:
			return True
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

def doorTime(n):	# Amount of time it takes for an elevator to close its door with n people using it
	return [3,5,7,9,11,13,15,17,19,22][n-1]

def elevatorSpeed(floorStart,floorEnd): # Time it takes for elevator to get from floorStart to floorEnd
	h = abs(floorStart - floorEnd)
	if h == 1:
		return 8
	else:
		return 2*8 + 5*(h-2)

def groupNumber():
	return int( random.random() * 7 + 1 )

def interarrivalTime():
	return int ( random.random()*88 + 2 )

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
				return floor


def run1day(floors, elevatorNum):
	t = 0
	eventQueue = []
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

	eventQueue.append(Event(0,"PedArrival",None))

	verbose = True

	while len(eventQueue) > 0:
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
			gn = groupNumber()
			if gn > peopleToDeliver:
				gn = peopleToDeliver
			if verbose: print(f'Pedestrians Arriving t:{t} Size: {gn}')
			if verbose: print(f'    Going to floors', end=" ")
			for i in range(gn):
				destination = assignFloor(floorCount)
				newRider = Person(t,destination)
				floorCount[destination] -= 1
				peopleToDeliver -= 1
				newRiders.append(newRider)
				if verbose: print(f'{destination}',end=" ")
			print("")
			if len(freeElevators) == 0:
				for rider in newRiders:
					lobby.append(rider)
			elif len(freeElevators) == 1:	
				# Fill the one elevator w/ all people
				elevators[freeElevators[0]].people = newRiders
				# Send elevator up to first floor
				elevators[freeElevators[0]].people.sort()
				destinationFloor = elevators[freeElevators[0]].people[0].destination
				eventQueue.append(Event( t + doorTime(len(elevators[freeElevators[0]].people))+elevatorSpeed(0,destinationFloor), "ElevatorArrive", freeElevators[0]))
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
					# Send elevators up to first floor
					if len(elevators[index].people) > 0:
						elevators[index].people.sort()
						destinationFloor = elevators[index].people[0].destination
						eventQueue.append(Event( t + doorTime(len(elevators[index].people))+elevatorSpeed(0,destinationFloor), "ElevatorArrive", index))
						elevators[index].location = destinationFloor
			# Start another Pedestrian Arrival Event
			if peopleToDeliver > 0:
				eventQueue.append(Event(t+interarrivalTime(), "PedArrival", None))
		elif event.eventType == "ElevatorArrive":
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
					eventQueue.append(Event( t + doorTime(len(elevators[event.extra].people))+elevatorSpeed(elevators[event.extra].location,destinationFloor), "ElevatorArrive", event.extra))
					elevators[event.extra].location = destinationFloor
				if verbose: print(f'Elevator {event.extra} has arrived to Lobby. Bringing {len(elevators[event.extra].people)} people up t:{t}')
			# Not Lobby
			else:
				if verbose: print(f'Elevator {event.extra} has arrived to {elevators[event.extra].location} with {len(elevators[event.extra].people)} people t:{t}')
				# Drop People Off
				count = 0
				for i in range(len(elevators[event.extra].people)):
					if elevators[event.extra].people[0].destination == elevators[event.extra].location:
						elevators[event.extra].people.pop(0)
						count += 1
					else:
						break
				if verbose: print(f'    {count} People got off')
				# If More People, Go Up
				if len(elevators[event.extra].people) > 0:
					destinationFloor = elevators[event.extra].people[0].destination
					eventQueue.append(Event( t + doorTime(count)+elevatorSpeed(elevators[event.extra].location,destinationFloor), "ElevatorArrive", event.extra))
					elevators[event.extra].location = destinationFloor
				# If No People, Go To Lobby
				else:
					destinationFloor = 0
					eventQueue.append(Event( t + doorTime(count)+elevatorSpeed(elevators[event.extra].location,destinationFloor), "ElevatorArrive", event.extra))
					elevators[event.extra].location = -1 # Set to -1 to indicate it is travelling to 0 and people can't get on until it reaches 0



run1day(5,1) # Floors, Elevators