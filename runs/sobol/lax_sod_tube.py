epsilon = 0.5

def scale(y, a, b):
    return a*(1-y) + (b-a)*y


def G(y):
    return 2*y - 1
if x < epsilon * G(X[0]):
    rho = scale(X[1], 0.3, 1.2)
    ux = X[2]
    p = scale(X[3], 0.9, 4.1)
else:
    rho = scale(X[4], 0.1, 0.7)
    ux = 0
    p = scale(X[5], 0.05, 0.7)
