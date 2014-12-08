#Chris Cloutier
#Parshva Shah

import sys

class process:
	def __init__(self, letter, frames, arrival, exit):
 		self.letter = letter
 		self.frames = frames
 		self.arrival = arrival
 		self.exit = exit
 		self.running = False
 		self.location = 0
 		self.memorySizes = []

 	def __str__(self):
 		return "process " + self.letter + " with size " + str(self.frames) + " starting at time " + str(self.arrival[0]) + " and ending at time " + str(self.exit[0])
 	def __repr__(self):
 		return "process " + self.letter + " with size " + str(self.frames) + " starting at time " + str(self.arrival[0]) + " and ending at time " + str(self.exit[0])

def printMem():
	string = ""
	for i in range(0,1600):
		#print i % 80
		if (i % 80 == 0) and i != 0:
			string += "\n"
		string += memory[i]
	print string

def sortSpaces(emptySpaces):
	emptySpaces = sorted(emptySpaces, key = lambda spaces: spaces[0])
	i = 0
	while i < len(emptySpaces):
		if i < len(emptySpaces) - 1:
			if emptySpaces[i][0] + emptySpaces[i][1] == emptySpaces[i+1][0]:
				emptySpaces[i] = [emptySpaces[i][0], emptySpaces[i][1] + emptySpaces[i+1][1]]
				emptySpaces.pop(i+1)
			else:
				i+= 1
		else:
			i+=1
	return emptySpaces

def defragment(process, emptySpaces):
	print "Performing defragmentation..."
	relocated = 0
	global memory
	memory = ['.' for x in range(0,1600)]

	for i in range(0,80):
		memory[i] = '#'

	memend = 80

	for temp in processes:
		if temp.running:
			if temp.location != memend:
				temp.location = memend
				relocated += 1
			for i in range(memend, memend + temp.frames):
				memory[i] = temp.letter
			memend += temp.frames

	emptySpaces = []
	emptySpaces.append([memend, 1600-memend])

	if emptySpaces[0][1] > process.frames:
		print "Degragmentation completed."
		print "Relocated %d processes to create a free memory block of %d units (%.2f%% of total memory)." %(relocated, emptySpaces[0][1], emptySpaces[0][1]/16.0)
		process.letter
		emptySpaces = addProcess(process, emptySpaces)
		return emptySpaces
	else:
		print "Error: OUT-OF-MEMORY"
		sys.exit()

def addFirst(process, emptySpaces):
	firstSpace = None
	for space in emptySpaces:
		if space[1] >= process.frames:
			firstSpace = space
			break
	if firstSpace:
		for i in range(firstSpace[0], firstSpace[0] + process.frames):
			memory[i] = process.letter
		process.running = True
		emptySpaces.remove(firstSpace)
		if firstSpace[1]-process.frames > 0:
			emptySpaces.append([firstSpace[0]+process.frames, firstSpace[1]-process.frames])
		process.location = firstSpace[0]
		return emptySpaces
	else:
		return defragment(process, emptySpaces)
def addBest(process, emptySpaces):
	bestSpace = None
	currentBest = float("inf")
	for space in emptySpaces:
		if space[1] >= process.frames:
			if space[1] <= currentBest:
				bestSpace = space
				currentBest = space[1]
			
	if bestSpace:
		for i in range(bestSpace[0], bestSpace[0] + process.frames):
			memory[i] = process.letter
		process.running = True
		emptySpaces.remove(bestSpace)
		if bestSpace[1]-process.frames > 0:
			emptySpaces.append([bestSpace[0]+process.frames, bestSpace[1]-process.frames])
		process.location = bestSpace[0]
		return emptySpaces
	else:
		return defragment(process, emptySpaces)

def addWorst(process, emptySpaces):
	worseSpace = None
	currentworse = 0
	for space in emptySpaces:
		if space[1] >= process.frames:
			if space[1] >= currentworse:
				worseSpace = space
				currentworse = space[1]
			
	if worseSpace:
		for i in range(worseSpace[0], worseSpace[0] + process.frames):
			memory[i] = process.letter
		process.running = True
		emptySpaces.remove(worseSpace)
		if worseSpace[1]-process.frames > 0:
			emptySpaces.append([worseSpace[0]+process.frames, worseSpace[1]-process.frames])
		process.location = worseSpace[0]
		return emptySpaces
	else:
		return defragment(process, emptySpaces)


def addNext(process, emptySpaces):
	nextSpace = None
	lastSpace = None

	for space in emptySpaces:
		if space[0] < addNext.cursor:
			lastSpace = space
	if lastSpace:
		if lastSpace[1] - (addNext.cursor - lastSpace[0]) > process.frames:
			emptySpaces.remove(lastSpace)
			oldSize = lastSpace[1]
			lastSpace = [lastSpace[0], addNext.cursor - lastSpace[0]]
			nextSpace = [addNext.cursor, oldSize-lastSpace[1]]
			
			emptySpaces.append(nextSpace)
			emptySpaces.append(lastSpace)
			emptySpaces = sorted(emptySpaces, key = lambda spaces: spaces[0])
	
	if nextSpace == None:
		for space in emptySpaces:
			if space[0] >= addNext.cursor:
				nextSpace = space
				break
	if nextSpace == None:
		nextSpace = emptySpaces[0]

	firstSpace = None
	for space in emptySpaces[emptySpaces.index(nextSpace):]:
		if space[1] >= process.frames:
			firstSpace = space
			break
	if firstSpace == None:
		for space in emptySpaces[:emptySpaces.index(nextSpace)]:
			if space[1] >= process.frames:
				firstSpace = space
				break

	if firstSpace:
		for i in range(firstSpace[0], firstSpace[0] + process.frames):
			memory[i] = process.letter
		process.running = True
		emptySpaces.remove(firstSpace)
		if firstSpace[1]-process.frames > 0:
			emptySpaces.append([firstSpace[0]+process.frames, firstSpace[1]-process.frames])
		process.location = firstSpace[0]
		addNext.cursor = firstSpace[0] + process.frames
		return emptySpaces
	else:
		return defragment(process, emptySpaces)

addNext.cursor = 0

def addProcess(process, emptySpaces):
	
	if algorithm == "first":
		emptySpaces = addFirst(process, emptySpaces)
	elif algorithm == "best":
		emptySpaces = addBest(process, emptySpaces)
	elif algorithm == "next":
		emptySpaces = addNext(process, emptySpaces)
	elif algorithm == "worst":
		emptySpaces = addWorst(process, emptySpaces)
	return emptySpaces

def removeProcess(process):
	for i in range(process.location, process.location + process.frames):
		memory[i] = '.'
	process.running = False
	emptySpaces.append([process.location, process.frames])
	process.location = 0
	process.arrival.pop(0)
	process.exit.pop(0)
	if not process.arrival:
		processes.remove(process)



if len(sys.argv) == 3:
	if(sys.argv[1] == "-q"):
		print "USAGE: python HW4.py [-q] <input file> { noncontig | first | best | next | worst }"
		sys.exit()
	quiet = False
	inFile = open(sys.argv[1], 'r')
	algorithm = sys.argv[2]
	if algorithm != "first" and algorithm != "best" and algorithm != "next" and algorithm != "worst":
		print "USAGE: python HW4.py [-q] <input file> { noncontig | first | best | next | worst }"
		sys.exit()
elif len(sys.argv) == 4:
	quiet = True
	inFile = open(sys.argv[2], 'r')
	algorithm = sys.argv[3]
	if algorithm != "first" and algorithm != "best" and algorithm != "next" and algorithm != "worst":
		print "USAGE: python HW4.py [-q] <input file> { noncontig | first | best | next | worst }"
		sys.exit()
else:
	print "USAGE: python HW4.py [-q] <input file> { noncontig | first | best | next | worst }"
	sys.exit()



processes = []
emptySpaces = []

numProc = int(inFile.readline())

for i in range(0, numProc):
	line = inFile.readline()
	lineArray = line.split()
	letter = lineArray.pop(0)
	frames = int(lineArray.pop(0))
	starts = []
	ends = []
	while lineArray:
		starts.append(int(lineArray.pop(0)))
		ends.append(int(lineArray.pop(0)))

	processes.append(process(letter, frames, starts, ends))

memory = ['.' for x in range(0,1600)]

for i in range(0,80):
	memory[i] = '#'

memend = 80

for process in processes:
	if int(process.arrival[0]) == 0:
		process.running = True
		process.location = memend
		if memend + process.frames < 1600:
			for i in range(memend, memend + process.frames):
				memory[i] = process.letter
			memend += process.frames
		else:
			print "Error: OUT-OF-MEMORY"
			sys.exit()

emptySpaces.append([memend, 1600-memend])
#print emptySpaces

print "Memory at time 0:"
printMem()

time = 0
timer = -1
if not quiet:
	timer = int(raw_input("Enter time until print:"))
while processes:
	if timer == 0:
		break
	emptySpaces = sorted(emptySpaces, key = lambda spaces: spaces[0])

	shortest = float("inf")
	shortestProc = []
	for process in processes:
		if process.running:
			if process.exit[0] < shortest:
				shortest = process.exit[0]
				shortestProc = []
				shortestProc.append(process)
			elif process.exit[0] == shortest:
				shortestProc.append(process)
		else:
			if process.arrival[0] < shortest:
				shortest = process.arrival[0]
				shortestProc = []
				shortestProc.append(process)
			elif process.arrival[0] == shortest:
				shortestProc.append(process)
	time = shortest

	#print shortestProc
	for process in shortestProc:
		#print process
		if process.running:
			removeProcess(process)
			shortestProc.remove(process)
	#print shortestProc

	#sort empty spaces and combine contiguous small spaces 
	emptySpaces = sortSpaces(emptySpaces)


	for process in shortestProc:
		if not process.running:
			emptySpaces = addProcess(process, emptySpaces)


	if quiet:
		print "Memory at time " + str(time) + ":"
		printMem()
	elif time >= timer:
		print "Memory at time " + str(time) + ":"
		printMem()
		timer = int(raw_input("Enter time for next print:"))
	

	emptySpaces = sorted(emptySpaces, key = lambda spaces: spaces[0])
	
	
