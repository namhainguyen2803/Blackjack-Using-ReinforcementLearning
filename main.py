"""
Created by namhainguyen2803 in 26/01/2023
"""
import numpy as np
import gym
from collections import defaultdict
import random
import json

f = open('policy.json')
data = json.load(f)
f.close()
def policy(state, list_policy = data):
    global cntt
    score = state[0]
    if str(state) in list_policy:
        return list_policy[str(state)]
    else:
        if score < 21:
            if random.random() > 0.5:
                return 1
            else:
                return 0
        else:
            return 0

def update_state(player_state, player_card, action):
    player_score = player_state[0]
    show_card = player_state[1]
    usable_ace = player_state[2]
    new_player_score = player_score
    new_usable_ace = usable_ace
    if action == 1:
        new_usable_ace = False
        new_card = give_card()
        player_card.append(new_card)
        if new_card == 1:
            if player_score <= 11:
                new_usable_ace = True
                new_player_score += 10
            else:
                new_usable_ace = False
        else:
            new_player_score = player_score + new_card
    return (new_player_score, show_card, new_usable_ace), player_card

def check_win(player_score, dealer_score):
    if player_score == 21:
        return True
    elif player_score > 21:
        return False
    else:
        if dealer_score == 21:
            return False
        elif dealer_score > 21:
            return True
        else:
            if player_score > dealer_score:
                return True
            elif player_score < dealer_score:
                return False
            else:
                return "Draw"

def give_card():
    deck = list(range(1,11)) + [10,10,10]
    return np.random.choice(deck)

def dealer_turn(dealer_card):
    dealer_score = sum(dealer_card)
    if 1 in dealer_card:
        if dealer_score <= 11:
            dealer_score += 10
    
    while dealer_score < 17:
        new_card = give_card()
        dealer_card.append(new_card)
        if new_card == 1:
            if dealer_score <= 11:
                dealer_score += 10
        else:
            dealer_score += new_card
    return dealer_score, dealer_card

def gamePlay():
    dealer_card = list()
    player_card = list()
    for i in range(2):
        dealer_card.append(give_card())
    for i in range(2):
        player_card.append(give_card())
    
    show_card = np.random.choice(dealer_card)
    player_score = np.sum(player_card)
    dealer_score = np.sum(dealer_card)

    usable_ace = False
    if 1 in player_card:
        if player_score <= 11:
            usable_ace = True
            player_score += 10
        else:
            usable_ace = False
    
    player_state = (player_score, show_card, usable_ace)
    
    if player_score == 21:
        print(f"Player's deck: {player_card}, player's score: {player_score}")
        print(f"Dealer's deck: {dealer_card}, dealer's score: {dealer_score}")
        return True
    elif player_score > 21:
        print(f"Player's deck: {player_card}, player's score: {player_score}")
        print(f"Dealer's deck: {dealer_card}, dealer's score: {dealer_score}")
        return False
    else:
        # Player's turn:
        while policy(player_state) == 1:
            player_action = policy(player_state)
            player_new_state, player_new_card = update_state(player_state, player_card, player_action)
            player_card = player_new_card
            player_state = player_new_state
        player_final_score = player_state[0]

        if player_final_score == 21:
            print(f"Player's deck: {player_card}, player's score: {player_final_score}")
            print(f"Dealer's deck: {dealer_card}, dealer's score: {dealer_score}")
            return True
        
        elif player_final_score > 21:
            print(f"Player's deck: {player_card}, player's score: {player_final_score}")
            print(f"Dealer's deck: {dealer_card}, dealer's score: {dealer_score}")
            return False
        else:
            # Dealer's turn:
            dealer_final_score, dealer_card = dealer_turn(dealer_card)
            print(f"Player's deck: {player_card}, player's score: {player_final_score}")
            print(f"Dealer's deck: {dealer_card}, dealer's score: {dealer_final_score}")
            return check_win(player_final_score, dealer_final_score)
        
cnt = 0
NUM_GAMES = 1000
for i in range(NUM_GAMES):
    result = gamePlay()
    if result == True:
        print("AI wins")
        cnt += 1
    elif result == False:
        print("Dealer wins")
    else:
        print("Draw")

print(cnt)
print(f"Winning percentage: {round(cnt/NUM_GAMES, 4) * 100}%")
# One should note that the winning percentage of blackjack for player should around 42-43%