from math import exp

def sigm(x):
    """Bounded sigmoid function."""
    return 1. / (1. + exp(-max(min(x, 20.), -20.)))