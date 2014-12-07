#Chris Cloutier
#Parshva Shah

file = open('inputfile.txt', 'r')

processes = []

numProc = int(file.readline())

for i in range(0, numProc):
	processes.append(file.readline())

print processes