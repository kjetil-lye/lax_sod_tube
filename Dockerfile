FROM alsvinn/alsvinn_cuda_git
COPY qmc_generators /qmc_generators

RUN cd /qmc_generators &&\
    mkdir build &&\
    cd build &&\
    cmake .. -DCMAKE_BUILD_TYPE=Release &&\
    make sobol dryrun &&\
    cp sobol/libsobol.so /usr/lib/ && \
    cp dryrun/dryrun /usr/bin/dryrun

# we want python3.7
RUN apt-get update &&\
    apt-get --yes install software-properties-common&&\
    add-apt-repository ppa:deadsnakes/ppa &&\
    apt-get update && apt-get --yes install python3.7
    
# Manually download and install pip for 3.7
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py &&\
    python3.7 get-pip.py&&\
    rm get-pip.py
    
RUN pip3.7 install netCDF4 numpy dicttoxml matplotlib
ENTRYPOINT ["/bin/bash"]


