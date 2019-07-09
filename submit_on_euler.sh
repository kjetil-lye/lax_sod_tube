#!/bin/bash

# Aborts the script on the first error
set -e

# Get the proxy settings
module load eth_proxy


# Get the image
bsub -J "singularity_pull" -n 1 -R light -R singularity "singularity pull docker://kjetilly/sodshocktube:latest"

# Generate the runs
all_jobs=""
for sampling_method in "mc" "sobol";
do
    for resolution in 32 64 128 256 512 1024 2048 4096;
    do
	# See also https://www-01.ibm.com/support/docview.wss?uid=isg3T1013867
	jobname=${sampling_method}_${resolution}
        bsub -J "${jobname}" -w "done(singularity_pull)" -W 120:00 -n 1  -R singularity "singularity exec -B $(pwd):/lax_sod_tube_for_ml docker://kjetilly/sodshocktube:latest /bin/bash /lax_sod_tube_for_ml/runs/run_configurations_from_docker.sh ${resolution} ${sampling_method}"

	if [ -z "${all_jobs}" ]; # First time, all_jobs is the empty string
	then
	    all_jobs="done(${jobname})"
	else

	    all_jobs="${all_jobs}&&done(${jobname})"
	fi;
    done
done

# Compute the functionals
bsub -w "${all_jobs}" -W 24:00 -n 1  -R singularity "singularity exec -B $(pwd):/lax_sod_tube_for_ml docker://kjetilly/sodshocktube:latest /bin/bash /lax_sod_tube_for_ml/functionals/generate_functionals_from_docker.sh"


# Extract the parameters
bsub -w "${all_jobs}" -n 1  -R singularity "singularity exec -B $(pwd):/lax_sod_tube_for_ml docker://kjetilly/sodshocktube:latest /bin/bash /lax_sod_tube_for_ml/parameters/generate_parameters_from_docker.sh"
