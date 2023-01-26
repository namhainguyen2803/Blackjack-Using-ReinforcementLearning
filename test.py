import numpy as np
import gym
from collections import defaultdict
import random
import blackjack

environment = gym.make("Blackjack-v1")
state = environment.reset()

Q = defaultdict(lambda: np.zeros(2))

print(blackjack.generate_episodes(Q, 0.7))