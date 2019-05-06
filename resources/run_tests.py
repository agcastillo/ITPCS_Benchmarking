import fileinput
import sys
import os
import subprocess
import re

# Directories where your .it files can be found, each directory should only have *one* .it file and *one* .map file
# Results from the tests will be stored in the respective directory as well
test_directories = ["ITPCS_Benchmarking/Test1/"]#, "ITPCS_Benchmarking/Test2/", "ITPCS_Benchmarking/Test3/", "ITPCS_Benchmarking/Test4/", "ITPCS_Benchmarking/Test5/"]

# Number of Tests you want to conduct
num_iterations = 3

# Array dimensions you want to test with, assuming your .it file takes a dim_matrix variable
dim_matrix = [80000, 160000, 240000, 320000,400000,480000, 560000, 640000, 720000] 
 
# Node count and max job time for each slurm job submission
node_count = "20"
time_allowance = "00:05:00"


# Check if we need to make the compiler
# If not, just make sure gompi module is loaded
exists = os.path.isfile('sicc')
if (exists):
	os.system("module load gompi/5.4.0_2.1.5")
else:
	os.system("make -f MakeFile-Compiler clean")
	os.system("module load gompi/5.4.0_2.1.5")
	os.system("make -f MakeFile-Compiler")



subprocess.call(["cp" ,"ITPCS_Benchmarking/resources/parse_results.py", "."])
for test_directory in test_directories:
	
	if not test_directory.endswith("/"):
		test_directory += "/"
	# Replace Tests path with ITPCS_Benchmarking
	#subprocess.call(["cp" ,"ITPCS_Benchmarking/resources/parse_results.py", test_directory])
	
	subprocess.call(["mkdir", test_directory + "slurm_files"])
	subprocess.call(["mkdir", test_directory + "output_files"])
	file_name = None
	map_name = None
	for file in os.listdir(test_directory):
    		if file.endswith(".it"):
			file_name = file
			print(file_name)
		elif file.endswith(".map"):
			map_name = file
			print(map_name)
	if (file_name) is None:
		print("No file with .it extension found in " + test_directory)
		continue
	elif map_name is None:
		print("No file with .map extension found in " + test_directory)
		continue

	# Replace the Tests paths with ITPCS_Benchmarking/			
	subprocess.call(["make", "clean", "-f", "MakeFile-Executable"])
	subprocess.call(["./sicc",test_directory + file_name,"ITPCS_Benchmarking/resources/rivana-cluster.ml", "ITPCS_Benchmarking/resources/rivana-cluster.cn", test_directory + map_name]) 
	subprocess.call(["make", "-f", "MakeFile-Executable"])
	subprocess.call(["mv","bin/it-program.o",test_directory])
	
	for i in range(num_iterations):
		for dim in dim_matrix:
			prefix = file_name[:-3] + "_" + str(dim) + "_" + str(i)
			slurm_file = open(prefix + ".slurm",'w')
			slurm_file.write("#!/bin/bash"
					+"\n#SBATCH --nodes="+node_count
					+"\n#SBATCH --ntasks="+ node_count
					+"\n#SBATCH --cpus-per-task=20"
					+"\n#SBATCH --exclusive"
					+"\n#SBATCH --time=" + time_allowance
					+"\n#SBATCH --partition=parallel"
					+"\n#SBATCH --account=crosscampusgrid"
					+"\n#SBATCH --output=" + test_directory + "output_files/slurm_" + str(dim) + "_" + str(i) + ".out"
					+"\nmodule load gompi/5.4.0_2.1.5"
					+"\nmodule load gcc"
					+"\nmodule load openmpi"
					+"\nmpirun " + test_directory + "it-program.o matrix_dim=" + str(dim) 
					+"\n")
			slurm_file.close()
			subprocess.call(["sbatch", prefix + ".slurm"])			
			subprocess.call(["mv", prefix + ".slurm", test_directory + "slurm_files/"])

parse_file = open("parse_info.txt", 'w')
dims = ""
directories = ""
for dim in dim_matrix:
	dims += str(dim) + ","

for d in test_directories:
	directories += d + ","
parse_file.write(str(num_iterations) + "\n" + dims + "\n" + directories)
parse_file.close()
print("Successfully submitted jobs for " + file_name)	
