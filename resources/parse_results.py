import sys
import fileinput
import os

iterations = 0
dim_matrix = []

f = open('parse_info.txt','r')
line_split = f.read().split('\n')
iterations = line_split[0]
dim_matrix = [int(x) for x in line_split[1].split(',')[:-1]]
paths = line_split[2].split(',')[:-1]
paths = [x + "output_files/" for x in paths]


print("Parsing results for " + str(iterations) + " iterations of the following dimensions: ")
print(dim_matrix)

f = open("results.txt", 'w')
for path in paths:
	for i in range(iterations):
		f.write( "\nTEST LOCATION: " + path + "\nTEST ITERATION: " + str(i)) 
		for dim in dim_matrix:
			start_times = []
			end_times = []
			filename = "slurm_" + str(dim) + "_" + str(i) + ".out"
			
			exists = os.path.isfile(path + "output_files/" + filename)
			if exists:
				for line in open(path + "output_files/" + filename, 'r'):
					
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
				if (len(start_times) != 0) & (len(end_times) != 0):
					avg_start = sum(start_times)/len(start_times) 
					avg_end = sum(end_times)/len(end_times)
					delta = avg_end - avg_start 
					f.write("\n\t" + str(dim) + "," + str(delta))
				else:
					f.write("\n\t" + str(dim) + ",NA")

			else:
				print(filename + " was not found in /output_files/")



