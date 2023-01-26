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

f_2 = open('policy_2.json')
data_2 = json.load(f_2)
f_2.close()

def policy(state, list_policy = data):
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

def update_state(player_state, player_card, list_policy_2 = data_2):
    player_score = player_state[0]
    show_card = player_state[1]
    usable_ace = player_state[2]
    
    new_player_score = player_score
    new_usable_ace = usable_ace
    new_card = give_card()
    player_card.append(new_card)
    num_aces = player_card.count(1)
    if num_aces == 0:
        new_player_score += new_card
        return (new_player_score, show_card, new_usable_ace), player_card
    else:
        sum_with_11 = sum(player_card) + 10
        state_with_11 = (sum_with_11, show_card, True)
        sum_without_11 = sum(player_card)
        state_without_11 = (sum_without_11, show_card, False)
        if sum_with_11 > 21:
            return state_without_11, player_card
        elif sum_with_11 == 21:
            return state_with_11, player_card
        elif sum_without_11 == 21:
            return state_without_11, player_card
        else:
            if str(state_without_11) in list_policy_2 and str(state_with_11) in list_policy_2:
                if list_policy_2[str(state_without_11)] > list_policy_2[str(state_with_11)]:
                    return state_without_11, player_card
                else:
                    return state_with_11, player_card
            elif str(state_without_11) in list_policy_2 and str(state_with_11)  not in list_policy_2:
                return state_without_11, player_card
            
            elif str(state_without_11) not in list_policy_2 and str(state_with_11) in list_policy_2:
                return state_with_11, player_card


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
            player_new_state, player_new_card = update_state(player_state, player_card)
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
print(f"Winning percentage: {round(cnt*100/NUM_GAMES, 4)}%")
# One should note that the winning percentage of blackjack for player should around 42-43%