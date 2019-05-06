import sys
import fileinput
import os

dim_matrix = [80000, 160000, 240000, 320000,400000,480000, 560000, 640000, 720000, 800000, 880000]
#, 960000, 1040000, 1120000, 1200000, 1280000, 2560000, 5120000]

filedata = None
for i in range(0,3):
	with open('results_' + str(i) + '.txt','w') as f:
		for dim in dim_matrix:
			start_times = []
			end_times = []
			exists = os.path.isfile("slurm_" + str(i) + "_" + str(dim) + ".out")
			if exists:
				for line in open("slurm_" + str(i) + "_"+ str(dim) + ".out",'r'):
					if "Start Time:" in line:
						line = line[11:-1]
						line.strip()
						start_times.append(int(line))
					elif "End Time:" in line:
						line = line[9:-1]
						line.strip()
						end_times.append(int(line))
				if (len(start_times) != 0) & (len(end_times) != 0):
					avg_start = sum(start_times)/len(start_times) 
					avg_end = sum(end_times)/len(end_times)
					delta = avg_end - avg_start 
					f.write(str(delta) + "," + str(dim) + "\n")
				else:
					f.write("NA," + str(dim) + "\n")
			else:
				print("slurm_" + str(i) + "_" + str(dim) + ".out does not exist") 
