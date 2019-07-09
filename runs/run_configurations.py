import matplotlib
matplotlib.use("Agg")
import alsvinn
import shutil
import numpy as np
import os
import sys
sys.path.append('../')
from config import resolutions, bases, samples
import config

if __name__ == '__main__':
    



    if len(sys.argv) > 1:
        resolutions_to_run = [int(sys.argv[1])]
    else:
        resolutions_to_run = resolutions

    if len(sys.argv) > 2:
        bases_to_run = [sys.argv[2]]
    else:
        bases_to_run = [k for k in bases.keys()]

    for base in bases_to_run:


        for r in resolutions_to_run:
            output_folder = config.folder(base, r)
            if not os.path.exists(output_folder):
                os.mkdir(output_folder)
            os.chdir(output_folder)
            shutil.copyfile('../libsobol.so', 'libsobol.so')
            
            print("{}: {}".format(base, r))
            name = 'sodshock_{}_{}'.format(base, r)
            alsvinn.run(name, base_xml=os.path.join('..', bases[base]),
                        dimension=[r,1,1],
                        number_of_saves=1, uq=True, samples=samples)
    
