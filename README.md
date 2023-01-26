# Blackjack using Reinforcement Learning

In this project, I use Reinforcement Learning to play Blackjack. The methods I use are Monte Carlo with Every-Visit and Epsilon-Greedy Exploration policy.

# Description:
   - Game rule of Blackjack: Blackjack is a card game where the goal is to beat the dealer by obtaining cards that sum to closer to 21 (without going over 21) than the dealers cards. 
   - Face cards (Jack, Queen, King) have a point value of 10. 
   - Aces can either count as 11 (called a 'usable ace') or 1. 
   - Numerical cards (2-9) have a value equal to their number. This game is played with an infinite deck (or with replacement). 
   - The game starts with the dealer having one face up and one face down card, while the player has two face up cards. 
   - The player can request additional cards (hit, action=1) until they decide to stop (stick, action=0) or exceed 21 (bust, immediate loss). 
   - After the player sticks, the dealer reveals their facedown card, and draws until their sum is 17 or greater. 
   - If the dealer goes bust, the player wins. 
   - If neither the player nor the dealer busts, the outcome (win, lose, draw) is decided by whose sum is closer to 21.
   
