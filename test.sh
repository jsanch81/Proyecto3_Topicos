#!/bin/bash

#SBATCH --job-name=mpi
#SBATCH --output=output.txt
#SBATCH --time=00:01:60
#SBATCH --partition=estudiantes
#SBATCH --ntasks=10



mpirun -np 4 python ./paralelo.py data2/
