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

 	def __str__(self):
 		return "Process " + self.letter + " with size " + str(self.frames) + " starting at time " + str(self.arrival[0]) + " and ending at time " + str(self.exit[0])
 	def __repr__(self):
 		return "Process " + self.letter + " with size " + str(self.frames) + " starting at time " + str(self.arrival[0]) + " and ending at time " + str(self.exit[0])

def printMem():
	string = ""
	for i in range(0,1600):
		#print i % 80
		if (i % 80 == 0) and i != 0:
			string += "\n"
		string += memory[i]
	print string

def addFirst(process):
	firstSpace = None
	for space in emptySpaces:
		if space[1] >= process.frames:
			firstSpace = space
			break

	for i in range(firstSpace[0], firstSpace[0] + process.frames):
		memory[i] = process.letter
	process.running = True
	emptySpaces.remove(firstSpace)
	if firstSpace[1]-process.frames > 0:
		emptySpaces.append([firstSpace[0]+process.frames, firstSpace[1]-process.frames])
	process.location = firstSpace[0]

def addProcess(process):
	if algorithm == "first":
		addFirst(process)
	elif algorithm == "best":
		addBest(process)
	elif algorithm == "next":
		addNext(process)
	elif algorithm == "worst":
		addWorst(process)
	print "Adding " + process.letter

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
	print "Removing " + process.letter


if len(sys.argv) == 3:
	if(sys.argv[1] == "-q"):
		print "USAGE: python HW4.py [-q] <input file> { noncontig | first | best | next | worst }"
		sys.exit()
	quiet = False
	inFile = open(sys.argv[1], 'r')
	algorithm = sys.argv[2]
elif len(sys.argv) == 4:
	quiet = True
	inFile = open(sys.argv[2], 'r')
	algorithm = sys.argv[3]
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
		for i in range(memend, memend + process.frames):
			memory[i] = process.letter
		memend += process.frames

emptySpaces.append([memend, 1600-memend])
print emptySpaces

print "Memory at time 0:"
printMem()

time = 0
while processes:
	
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

	for process in shortestProc:
		if not process.running:
			addProcess(process)

	if quiet:
		print "Memory at time " + str(time) + ":"
		printMem()

	#sort empty spaces and combine contiguous small spaces 
	emptySpaces = sorted(emptySpaces, key = lambda spaces: spaces[0])

	print emptySpaces
	
	

