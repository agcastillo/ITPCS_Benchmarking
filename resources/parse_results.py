import sys
import fileinput
import os

iterations = 0
dim_matrix = []

# Get parsing information from parse_info.txt
f = open('parse_info.txt','r')
line_split = f.read().split('\n')
iterations = int(line_split[0])
dim_matrix = [int(x) for x in line_split[1].split(',')[:-1]]
paths = line_split[2].split(',')[:-1]
paths = [x + "output_files/" for x in paths]


print("Parsing results for " + str(iterations) + " iterations of the following dimensions: ")
print(dim_matrix)

f = open("results.txt", 'w')
for path in paths:
	f.write("***********************************************************************\n")
	f.write("Test Location: " + path[:-13] + "\n")
	f.write("***********************************************************************\n")
	for i in range(iterations):
		f.write( "Test Iteration: " + str(i)+ "\n") 
		for dim in dim_matrix:

			# These arrays will hold all the start_time and end_time printf statements from each execution of our IT files
			start_times = []
			end_times = []

			filename = path  + "slurm_" + str(dim) + "_" + str(i) + ".out"				
			exists = os.path.isfile(filename)
			if exists:
				for line in open( filename, 'r'):
					# Appent to either array based on which they belong to, handle error where two printfs occured on top of each other	
					if "Start Time:" in line:
						try:
							line = line[11:-1]
							line.strip()
							start_times.append(int(line))
						except Exception:
							continue 
					elif "End Time:" in line:
						try:
							line = line[9:-1]
							line.strip()
							end_times.append(int(line))
						except Exception:
							continue
				# Get average of each array and print the diffence between the start time and end time (in milliseconds)
				if (len(start_times) != 0) & (len(end_times) != 0):
					avg_start = sum(start_times)/len(start_times) 
					avg_end = sum(end_times)/len(end_times)
					delta = avg_end - avg_start 
					f.write("\t| Dim = " + str(dim) + ", Time (ms) = " + str(delta)+ "\n")
				else:
				# If the job was aborted or didn't have any valid output for some reason, print NA for that dimension
					f.write("\t| Dim = " + str(dim) + ", Time (ms) = NA"+ "\n")

			else:
				print( filename + " was not found")
		f.write("\n")



