import numpy as np
import netCDF4
import sys
sys.path.append('../')
from config import resolutions, bases
import config

class Data(object):
    def __init__(self, f, sample_number):
        self.rho = f.variables['sample_{}_rho'.format(sample_number)][:,0,0]
        self.mx = f.variables['sample_{}_mx'.format(sample_number)][:,0,0]
        self.E = f.variables['sample_{}_E'.format(sample_number)][:,0,0]

        
class AreaAverage(object):
    def __init__(self, interval, f = lambda u: u.rho):
        self.interval = interval
        self.f = f

    def __call__(self, x, u):
        a = self.interval[0]
        b = self.interval[1]
        D = (x >= a) * (x <= b)
        return np.sum(self.f(u) * D)/np.sum(D)

def apply_functional(input_file, functional):
    values = []
    with netCDF4.Dataset(input_file) as f:
        sample = 0
        while 'sample_{}_rho'.format(sample) in f.variables.keys():
            data = Data(f, sample)
            N = data.rho.shape[0]
            x = np.linspace(-5, 5, N)
            values.append(functional(x, data))
            sample += 1
    return values


if __name__ == '__main__':

    
    intervals = [[-1.5, -0.5],
                 [0.8, 1.8],
                 [2, 3]]

    bases = [k for k in bases.keys()]

    for base in bases:
        for r in resolutions:
            print("{}: {}".format(base, r))
            folder = config.folder(base, r)
            name = '../runs/{}/sodshock_{}_{}_1.nc'.format(folder, base, r)
            values_all = []
            for interval in intervals:
                functional = AreaAverage(interval)
                values_all.append(apply_functional(name, functional))

            for interval in intervals:
                # Kinda kinect energy
                functional = AreaAverage(interval, f= lambda u: u.mx*u.mx/u.rho)
                values_all.append(apply_functional(name, functional))

            values_to_save = np.array(values_all).T

            # Text file comment:
            functional_names = ["q{} = {}".format(i+1, intervals[i]) for i in range(len(intervals))]
            functional_names.extend(["EK{} = {}".format(i+1, intervals[i]) for i in range(len(intervals))])
            header = ", ".join(functional_names)

            
            np.savetxt('average_functionals_{}_{}.txt'.format(base, r), values_to_save,
                       header=header)

            
    
    
    
