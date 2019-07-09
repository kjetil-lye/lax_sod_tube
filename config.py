import numpy as np
resolutions = 2**np.arange(4,13)
bases = {'sobol':'sobol/lax_sod_tube.xml',
         'mc': 'mc/lax_sod_tube.xml'}
samples = 2*8192

def folder(base, resolution):
    return "{}_{}".format(base, resolution)
