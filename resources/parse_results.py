import sys
import fileinput
import os

iterations = 0
dim_matrix = []

f = open('parse_info.txt','r')
parse_info = f.read().split(',')
iterations = int(parse_info[0])
dim_matrix = [int(x) for x in parse_info[1:-1]]
print("Parsing results for " + str(iterations) + " iterations of the following dimensions: ")
print(dim_matrix)

for i in range(iterations):
	f = open("results" + "_" + str(i) + ".txt",'w')
	
	for dim in dim_matrix:
		start_times = []
		end_times = []
		filename = "slurm_" + str(dim) + "_" + str(i) + ".out"
		
		exists = os.path.isfile("output_files/" + filename)
		if exists:
			for line in open("output_files/" + filename, 'r'):
				
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
                                f.write(str(dim) + "," + str(delta)+ "\n")
                        else:
                                f.write(str(dim) + ",NA" + "\n")

		else:
			print(filename + " was not found in /output_files/")



