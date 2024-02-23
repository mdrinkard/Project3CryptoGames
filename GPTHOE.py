import random
import streamlit as st
from PIL import Image

# Deck of Cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]

# Function to deal a card
def dealCard():
    card = random.choice(deck)
    deck.remove(card)
    return card

# Function to calculate the total value of a hand
def total(hand):
    total_val = 0
    num_aces = 0
    for card in hand:
        if card['rank'] in ['Jack', 'Queen', 'King']:
            total_val += 10
        elif card['rank'] == 'Ace':
            num_aces += 1
            total_val += 11
        else:
            total_val += int(card['rank'])

    while total_val > 21 and num_aces > 0:
        total_val -= 10
        num_aces -= 1

    return total_val

# Function to display a hand
def display_hand(hand, hide_first_card=False):
    for card in hand:
        if hide_first_card and card == hand[0]:
            st.image('Project3CryptoGames/Resources/back.png', width=100)
        else:
            image_path = f"Project3CryptoGames/Resources/{card['rank']}_{card['suit']}.png"
            st.image(image_path, width=100)

# Initial setup
dealerHand = []
playerHand = []

# Initial dealing
for _ in range(2):
    dealerHand.append(dealCard())
    playerHand.append(dealCard())

# Streamlit App
st.title('Blackjack')

st.write('Dealer\'s Hand:')
display_hand(dealerHand, hide_first_card=True)

st.write('Your Hand:')
display_hand(playerHand)

# Game logic
player_total = total(playerHand)
dealer_total = total(dealerHand)

if player_total == 21:
    st.write('Blackjack! You win!')
elif player_total > 21:
    st.write('You bust! Dealer wins!')
else:
    st.write('Select your move:')
    move = st.radio('', ('Hit', 'Stand'))
    while move == 'Hit':
        if move == 'Hit':
            playerHand.append(dealCard())
            st.write('Your Hand:')
            display_hand(playerHand)

            player_total = total(playerHand)
            if player_total > 21:
                st.write('You bust! Dealer wins!')
                break
            elif player_total == 21:
                st.write('Blackjack! You win!')
                break
            else:
                st.write('Select your move:')
                move = st.radio('', ('Hit', 'Stand'))
        else:
            break
    if move == 'Stand':  # Stand
        st.write('Your final hand:')
        display_hand(playerHand)

        st.write('Dealer\'s turn:')
        st.write('Dealer\'s Hand:')
        display_hand(dealerHand)

        # Dealer's turn
        while total(dealerHand) < 17:
            dealerHand.append(dealCard())
            st.write('Dealer hits:')
            st.write('Dealer\'s Hand:')
            display_hand(dealerHand)

        dealer_total = total(dealerHand)

        if dealer_total > 21:
            st.write('Dealer busts! You win!')
        elif dealer_total > player_total:
            st.write('Dealer wins!')
        elif dealer_total < player_total:
            st.write('You win!')
        else:
            st.write('It\'s a tie!')
