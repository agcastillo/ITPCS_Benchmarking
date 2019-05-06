import fileinput
import sys
import os
filedata = None
with open('test.sh','r') as file:
	filedata = file.read()


dim_matrix = [80000, 160000, 240000, 320000,400000,480000, 560000, 640000, 720000] 
# 800000, 880000, 960000, 1040000, 1120000, 1200000, 1280000, 2560000, 5120000]
for i in range(3):
	for dim in dim_matrix:
		filedata = filedata.replace("DIM=\"1000\"", "DIM=\"" + str(dim) + "\"")
		filedata = filedata.replace("#SBATCH --output=slurm.out", "#SBATCH --output=Tests/Test4/slurm_"+str(i) + "_" + str(dim) + ".out")
		with open('test.sh','w') as file:
			file.write(filedata)
		print("Submitting job with DIM=" + str(dim))
		os.system('./test.sh')
		print(filedata)
		filedata = filedata.replace( "DIM=\"" + str(dim) + "\"", "DIM=\"1000\"")
		filedata = filedata.replace("#SBATCH --output=Tests/Test4/slurm_" + str(i) + "_" + str(dim) + ".out", "#SBATCH --output=slurm.out")
		with open('test.sh','w') as file:
			file.write(filedata)	
