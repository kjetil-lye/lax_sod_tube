import subprocess
import os
import numpy as np
import sys
sys.path.append('../')
import config
if __name__ == '__main__':
    if not os.path.exists("libsobol.so"):
        raise Exception("You need to compile the library from https://github.com/kjetil-lye/qmc_generators")

    for base in config.bases.keys():
        xml_name = '../runs/{}/sodshock_{}_{}.xml'.format(
            config.folder(base, config.resolutions[0]),
            base,
            config.resolutions[0])
        outname = "parameters_{}".format(base)
        subprocess.run(["generate_parameters",
                        xml_name,
                        outname], check=True)
                   

                                     

    
