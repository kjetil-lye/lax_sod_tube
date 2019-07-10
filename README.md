# Generating QMC and MC data for the Lax Sod Shock Tube

This initial data is a stochastic initial data for the Burgers' equation that encapsulates both the Sod Shock Tube and the Lax Shock Tube.

To checkout this repository, do

    git clone --recursive git@github.com:kjetil-lye/sod_lax_tube.git

make sure your ssh keys are added to github!

After running all the scripts in this repository, you should end up with the following important files:

 * ```parameters/parameters_<base>_X.txt``` a list of all the Sobol/QMC or MC points points. Each line corresponds to one point. Can be read in python with ```numpy.loadtxt('parameters/parameters_<base>_X.txt')```

 * ```functionals/average_functionals_<base>_<n>.txt``` are the 6 functional values (header describes what they are). Can be read with ```numpy.loadtxt('functionals/average_functionals_<base>_<n>.txt')```. Here ```<n>``` is the mesh resolution between 16 and 4096. The functionals are:
    - ```q<k>``` average density over the given interval
    - ```EK<k>``` average kinetic energy over the given interval

Each parameter line in ```parameters_<base>_X.txt``` corresponds to the functional value at the same line in each of the functional files.
  

These experiments can be run without docker, but on say Windows, it is a a bit hard to compile alsvinn, therefore, we reocmmend using Docker, described below.

To run these experiments, you need to run in order (I recommend to run this in Docker, see further below):

1) Generate the samples in ```runs``` (run ```python run_configurations.py```)
    

2) Generate functionals in ```functionals``` (run ```python generate_functionals.py```)

3) Generate parameters in ```parameters``` (run ```python generate_parameters.py```)
    

## Using docker to run these experiments

The ```Dockerfile``` in this folder can be used to generate a docker image that can be used run all experiments.

To run the experiments you need to know your user id for the current computer (see below)

### Getting Docker

[Consult the online documentation](https://docs.docker.com/install/). Install the CE (Community Edition) version.

These files were last tested with

    Docker version 18.09.1-ce, build 4c52b901c6

### Getting your user id
For other operating system, search online for "user id <Operating system name>".

#### Linux

On Linux, you do

    userid=$(id -u)

#### OS X

On Mac OS X, you do

    userid=$(id -u)

### Building the docker container

Use

    docker build . -t sodshocktube


### Generating runs

Here ```${PATH_TO_GIT_REPO}``` refers to the absolute path to the base folder of this
git repsitory, so that ```${PATH_TO_GIT_REPO}/README.md``` is this file.

In BASH you can set this at the beginnning as eg.

    export PATH_TO_GIT_REPO=$(pwd)

in other shells you can do something similar, or just manually replace ${PATH_TO_GIT_REPO} with the full path

First generate samples

    docker run --user ${userid} --rm  -v ${PATH_TO_GIT_REPO}:/sodshocktube_for_ml \
       sodshocktube /sodshocktube_for_ml/runs/run_configurations_from_docker.sh


Then generate functionals

    docker run --user ${userid} --rm  -v ${PATH_TO_GIT_REPO}:/sodshocktube_for_ml \
       sodshocktube /sodshocktube_for_ml/functionals/generate_functionals_from_docker.sh

Then generate parameters

    docker run --user ${userid} --rm  -v ${PATH_TO_GIT_REPO}:/sodshocktube_for_ml \
       sodshocktube /sodshocktube_for_ml/parameters/generate_parameters_from_docker.sh

## Running in singularity
This section is especially relevant for the [ETHZ cluster EULER](https://scicomp.ethz.ch/wiki/Main_Page). 

The [EULER wiki contains a section on using singularity.](https://scicomp.ethz.ch/wiki/Singularity)

On Euler, you want to load the proxy module first before running these commands:

    module load eth_proxy 

### Getting the image

I have uploaded a standalone image to dockerhub that can be downloaded from Singularity. 

On Euler, you can get the image by
   

    bsub -n 1 -R light -R singularity "singularity pull docker://kjetilly/sodshocktube:latest"

and wait until the job finishes. Check output of ```lsf.o<job id>``` for results and check for any errors. 


*IMPORTANT* by default, all images on dockerhub are public.

### Generating the data

First generate samples (this is the slow way, see below for a more effiecient way)

    bsub -n 1  -R singularity "singularity exec -B $(pwd):/sodshocktube_for_ml \
       docker://kjetilly/sodshocktube:latest /bin/bash /sodshocktube_for_ml/runs/run_configurations_from_docker.sh"

and wait for it to finish (use ```bjobs``` to see current status of jobs).

### Generating the runs in parallel

It is probably a good idea to generate the data in parallel. To do so, you can submit one job per resolution/sampling method:

    bsub -W 24:00 -n 1  -R singularity "singularity exec -B $(pwd):/sodshocktube_for_ml \
       docker://kjetilly/sodshocktube:latest /bin/bash /sodshocktube_for_ml/runs/run_configurations_from_docker.sh <RESOLUTION> <SAMPLING_METHOD>"

eg.

    bsub -W 24:00 -n 1  -R singularity "singularity exec -B $(pwd):/sodshocktube_for_ml \
       docker://kjetilly/sodshocktube:latest /bin/bash /sodshocktube_for_ml/runs/run_configurations_from_docker.sh 512 sobol"

To submit them all do 

    for sampling_method in "mc" "sobol";
    do
        for resolution in 32 64 128 256 512 1024 2048 4096;
        do
            bsub -W 24:00 -n 1  -R singularity "singularity exec -B $(pwd):/sodshocktube_for_ml \
                docker://kjetilly/sodshocktube:latest /bin/bash /sodshocktube_for_ml/runs/run_configurations_from_docker.sh ${resolution} ${sampling_method}"
        done
    done

*NOTE* It is also possible to do parallelization between samples and spatially, see the alsvinn documentation for more information.

### Generating the functionals

After all runs have finished, run

    bsub -W 24:00 -n 1  -R singularity "singularity exec -B $(pwd):/sodshocktube_for_ml \
        docker://kjetilly/sodshocktube:latest /bin/bash /sodshocktube_for_ml/functionals/generate_functionals_from_docker.sh"

### Extracting the parameters

Do 

    bsub -n 1  -R singularity "singularity exec -B $(pwd):/sodshocktube_for_ml \
        docker://kjetilly/sodshocktube:latest /bin/bash /sodshocktube_for_ml/parameters/generate_parameters_from_docker.sh"

### Submitting everything at once with job chaining

You can submit every script at once by the use of [job chaining](https://scicomp.ethz.ch/wiki/Job_chaining). See ```submit_on_euler.sh``` .


### Generating your own image

You can generate your own image by first making an account on [hub.docker.com](https://hub.docker.com), then on your own computer do


    docker build . -t <your dockerhub username>/<name of container>:latest
    docker push <your dockerhub username>/<name of container>:latest

and on Euler replace "kjetilly/sodshocktube:latest" with <your dockerhub username>/<name of container>:latest in the commands above.

It would also be possible to generate a native singularity image, though I doubt this would be worth it. The good thing about Docker images is that 
they are compatible with singularity and shifter (and docker). CSCS uses Shifter, not Singularity, for instance.

