"""
Created by namhainguyen2803 in 26/01/2023
"""
import numpy as np
import gym
from collections import defaultdict
import random
import json

environment = gym.make("Blackjack-v1")

"""
Description: 
    Game rule of Blackjack: Blackjack is a card game where the goal is to beat the dealer by obtaining cards 
    that sum to closer to 21 (without going over 21) than the dealers cards.
    Face cards (Jack, Queen, King) have a point value of 10.
    Aces can either count as 11 (called a 'usable ace') or 1.
    Numerical cards (2-9) have a value equal to their number.
    This game is played with an infinite deck (or with replacement). 
    The game starts with the dealer having one face up and one face down card, while the player has two face up cards.
    The player can request additional cards (hit, action=1) until they decide to stop (stick, action=0) 
    or exceed 21 (bust, immediate loss). After the player sticks, the dealer reveals their facedown card, 
    and draws until their sum is 17 or greater. If the dealer goes bust, the player wins. 
    If neither the player nor the dealer busts, the outcome (win, lose, draw) is decided by whose sum is closer to 21.
    
Terminology:
    Action space: there are two actions: stick(0) or hit(1)
    State space: 3-D tuple including the player's current sum, the value of the dealer's one showing card (1-10 where 1 is ace),
    the player holds a usable ace (0 or 1).
    Rewards: win game: +1; lose game: -1; draw game: 0
"""

# hyper params:
NUM_EPISODES = 100000
NUM_STATES = 32 * 11 * 2
NUM_ACTIONS = 2
EPSILON = 0.9
MIN_EPSILON = 0.03
GAMMA = 1
ALPHA = 0.03

def epsilon_greedy_policy(Q_value, state, epsilon, num_actions = NUM_ACTIONS):
    """ Policy function based on episilon greedy. The function maps states to actions
    Args:
        Q_value (dictionary): Q value of all states and actions
        state (3-D tuple): the player's current sum, the value of the dealer's one showing card (1-10 where 1 is ace), 
        the player holds a usable ace (0 or 1).
        epsilon (float): probability to decide whether policy plays greedy(exploitation) or non-greedy(exploration)
    """
    opt_action = np.argmax(Q_value[state])
    other_actions = np.array([i for i in range(num_actions) if i != opt_action])
    if random.random() > epsilon:
        # exploitation
        return opt_action
    else:
        # exploration
        return np.random.choice(other_actions)


def generate_episodes(Q_value, epsilon):
    """ Function to generate episodes(data) for RL
    Args:
        Q_value (dictionary): Q value of all states and actions
        epsilon (float): probability to decide whether policy plays greedy(exploitation) or non-greedy(exploration)
    """
    state = environment.reset()
    episodes = list()
    state = state[0]
    while True:
        action = epsilon_greedy_policy(Q_value, state, epsilon)
        next_step = environment.step(action)
        next_state = next_step[0]
        reward = next_step[1]
        done_yet = next_step[2]
        episodes.append([state, action, reward])
        if done_yet == True:
            break
        state = next_state
    
    return episodes

def Monte_Carlo_Every_visit(num_actions, num_episodes, epsilon, epsilon_min, alpha, gamma):
    Q_value = defaultdict(lambda: np.zeros(num_actions))
    policy = dict()

    for episode in range(num_episodes):
        epsilon = max(epsilon_min, epsilon * 0.8)
        
        # generate states, actions, rewards from generate_episode
        states, actions, rewards = zip(*generate_episodes(Q_value, epsilon))
        num_states = len(states)
        for ind, state in enumerate(states):
            discount_factor = np.array([gamma**i for i in range(len(rewards[ind:]))])
            returns = sum(discount_factor * np.array(rewards[ind:]))

            # update Q_value:
            Q_value[state][actions[ind]] += alpha * (returns - Q_value[state][actions[ind]])

    for state, Q_value_per_state in Q_value.items():
        policy.update([(str(state), int(np.argmax(Q_value_per_state)))])
    
    return Q_value, policy

if __name__ == "__main__":
    Q, P= Monte_Carlo_Every_visit(NUM_ACTIONS, NUM_EPISODES, EPSILON, MIN_EPSILON, ALPHA, GAMMA)
    print(P)
    print(len(P))
    json = json.dumps(P)
    f = open("policy.json","w")
    f.write(json)
    f.close()