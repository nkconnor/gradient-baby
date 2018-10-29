from math import sqrt, log

import numpy as np
from math import exp
from utils import sigm
import random

class StochasticGOptimizer():
    def pull(self, choices):
        rand = sum(map(lambda x: x[1], choices)) * random.random()
        ind = 0
        for item, score in choices:  # no need to sort (probably)
            ind += score
            if ind > rand:
                return (item, score)

class EpsilonGreedyOptimizer:
    def __init__(self, epsilon):
        self.epsilon = epsilon

    # expects tuple (lever, score)
    def pull(self, choices):
        # Choose the highest expected payout
        if random.random() >= self.epsilon:
            return max(choices, key=lambda x: x[1])[0]

        # Else pick at random amongst all levers
        return random.choice(choices)[0]