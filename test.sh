#!/bin/bash

#SBATCH --time=00:00:20
#SBATCH --nodes=4
# Memory per node specification is in MB. It is optional.
# The default limit is 3000MB per core.
#SBATCH --job-name="hello_test"
#SBATCH --output=test-srun.out

mpirun -np 2 python ./paralelo.py folder/
