import random
import streamlit as st

# Deck of Cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]

# Function to deal a card
def deal_card():
    card = random.choice(deck)
    deck.remove(card)
    return card

# Function to calculate the total value of a hand
def calculate_total(hand):
    total = 0
    num_aces = 0
    for card in hand:
        if card['rank'] in ['Jack', 'Queen', 'King']:
            total += 10
        elif card['rank'] == 'Ace':
            num_aces += 1
            total += 11
        else:
            total += int(card['rank'])
    while total > 21 and num_aces:
        total -= 10
        num_aces -= 1
    return total

# Function to display a hand
def display_hand(hand, hide_first_card=False):
    """
    Function to display a hand.
    """
    for card in hand:
        if hide_first_card and card == hand[0]:
            st.image('Project3CryptoGames/Resources/back.png', width=100)
        else:
            image_path = f"Project3CryptoGames/Resources/{card['rank']}_{card['suit']}.png"
            st.image(image_path, width=100)

# Streamlit app title
st.title("Blackjack")

# Initialize game state variables
player_hand = []
dealer_hand = []

# Deal initial cards
for _ in range(2):
    player_hand.append(deal_card())
    dealer_hand.append(deal_card())

# Main game loop
player_total = calculate_total(player_hand)
dealer_total = calculate_total(dealer_hand)

st.write("Dealer's Hand:")
display_hand(dealer_hand, hide_first_card=True)
st.write(f"Dealer's Total: {dealer_total}")

st.write("Your Hand:")
display_hand(player_hand)
st.write(f"Your Total: {player_total}")

while st.button('Hit'):
    player_hand.append(deal_card())
    player_total = calculate_total(player_hand)
    st.write("Your Hand:")
    display_hand(player_hand)
    st.write(f"Your Total: {player_total}")
    if player_total > 21:
        st.write("You bust! Dealer wins.")
        break

if player_total <= 21:
    while dealer_total < 17:
        dealer_hand.append(deal_card())
        dealer_total = calculate_total(dealer_hand)
    st.write("Dealer's Hand:")
    display_hand(dealer_hand)
    st.write(f"Dealer's Total: {dealer_total}")

    if dealer_total > 21 or player_total > dealer_total:
        st.write("You win!")
    elif player_total < dealer_total:
        st.write("Dealer wins.")
    else:
        st.write("It's a tie!")
