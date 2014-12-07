#Chris Cloutier
#Parshva Shah

class process:
	def __init__(self, letter, frames, arrival, exit):
 		self.letter = letter
 		self.frames = frames
 		self.arrival = arrival
 		self.exit = exit

 	def __str__(self):
 		return "Process " + self.letter + " with size " + self.frames + " starting at time " + self.arrival[0] + " and ending at time " + self.exit[0]
 	def __repr__(self):
 		return "Process " + self.letter + " with size " + self.frames + " starting at time " + self.arrival[0] + " and ending at time " + self.exit[0]

def printMem():
	string = ""
	for i in range(0,1600):
		#print i % 80
		if (i % 80 == 0) and i != 0:
			string += "\n"
		string += memory[i]
	print string

file = open('inputfile.txt', 'r')

processes = []

numProc = int(file.readline())

for i in range(0, numProc):
	line = file.readline()
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
		for i in range(memend, memend + process.frames):
			memory[i] = process.letter
		memend += process.frames

print "Memory at time 0:"
printMem()




