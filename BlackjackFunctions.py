import random
import streamlit as st
from web3 import Web3
import streamlit
import json
from PIL import Image

# # player_money = crypto implementation

playerIn = True #In the game
dealerIn = True  #In the game
playerDoublesDown = False  # Track if player has chosen to double down
playerSplit = False  # Track if player has chosen to split

# Deck of Cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]


# List of Player & Dealer hands
playerHands = [[]]  
dealerHand = []


# Deals card in the beginning
def dealCard(turn):
    card = random.choice(deck)
    turn.append(card)
    deck.remove(card)

# Function defining card total & face card values
def total(hand):
    """
    Function to calculate the total value of a hand.
    """
    total = 0
    num_aces = 0
    for card in hand:
        if card['rank'] in ['Jack', 'Queen', 'King']: # Converting String Values in dictionary into an int
            total += 10
        elif card['rank'] == 'Ace':
            num_aces += 1
            total += 11 # Ace = 11 first
        else:
            total += int(card['rank']) ### Is Calculating the total based on the value part in the dictionary
    while total > 21 and num_aces:
        total -= 10
        num_aces -= 1 # Converting Ace to 1 if card total > 21 (if bust occurs with Ace in hand)
    return total

# streamlit function to show cards in app

def display_hand(hand, hide_first_card=False):
    """
    Function to display a hand.
    """
    for card in hand:
        if hide_first_card and card == hand[0]:
            st.image('Resources/back.png', width=100)
        else:
            image_path = f"Resources/{card['rank']}_{card['suit']}.png"
            st.image(image_path, width=100)

# Function checking whether split is available
def check_for_split(player_hand):
    return len(player_hand) == 2 and player_hand[0] == player_hand[1]

# Function defining 2 hands for players when chosen to split
def split_hand(player_hand):
    return [[player_hand[0]], [player_hand[1]]]

# Function for checking/ adjusting total wallet for player based on hand (double_down)
def double_down(player_hand, player_money):
    if player_money >= 2:  # Assuming 1 is current bet, check if player has enough to double
        dealCard(player_hand)
        return True  # Player chose to double down
    return False

# Defining the reveal of the dealers hand at end of game
def revealDealerHand():
    if len(dealerHand) >= 2:
        return dealerHand[0], 'X' # 'X' to hide dealer's second card
    elif len(dealerHand) > 2:
        return dealerHand[0], dealerHand[1:]
    
def deal_initial_cards():
    global playerHands, dealerHand
    
    # Clear hands from previous rounds
    playerHands = [[]]
    dealerHand.clear()
    
    # Deal 2 cards to dealer and player
    for _ in range(2):
        dealCard(dealerHand)
        for hand in playerHands:
            dealCard(hand)
    
    # Displaying cards on Streamlit
    st.subheader("Dealer's Hand:")
    st.write(f'{dealerHand[1]}')
    display_hand(dealerHand,hide_first_card=True)
    st.subheader("Player's Hand(s):")
    for hand in playerHands:
        st.write(f"{hand}")
        display_hand(hand,hide_first_card=False)

def hit_or_stay():
    hit_button = st.button("Hit")
    stay_button = st.button("Stay")

    if hit_button:
        return 'Hit'
    elif stay_button:
        return 'Stay'
    else:
        return None

def player_turn():
    global playerHands
    
    # Continue player's turn until they choose to stay or bust
    while True:
        decision = hit_or_stay()
        if decision == 'Hit':
            for hand in playerHands:
                dealCard(hand)
            st.subheader("Player's Hand(s):")
            for hand in playerHands:
                st.write(f"{hand}")
                display_hand(hand, hide_first_card=False)
            total_value = total(playerHands[0])  # Assuming only one player for simplicity
            if total_value > 21:
                st.write("Bust! Player's hand total exceeds 21.")
                break
        else:
            break