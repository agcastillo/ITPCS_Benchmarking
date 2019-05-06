#!/bin/bash

DIM="1000"
FILE="test.slurm"

/bin/cat << EOM > $FILE
#!/bin/bash
#SBATCH --nodes=20
#SBATCH --ntasks=20
#SBATCH --cpus-per-task=20
#SBATCH --exclusive
#SBATCH --time=00:05:00
#SBATCH --partition=parallel
#SBATCH --account=crosscampusgrid
#SBATCH --output=slurm.out
module load gompi/5.4.0_2.1.5
module load gcc
module load openmpi

mpirun bin/it-program.o matrix_dim=$DIM 


EOM
sbatch $FILE
