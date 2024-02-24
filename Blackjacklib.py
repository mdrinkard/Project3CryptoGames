import random
import streamlit as st
from web3 import Web3
import streamlit
import json
from PIL import Image

# # Connect to Ganache
# ganache_url = "HTTP://127.0.0.1:7545"  # Replace with your Ganache instance URL
# web3 = Web3(Web3.HTTPProvider(ganache_url))

# # Verify connection
# print(web3.is_connected())

# contract_address = web3.to_checksum_address('0xd9145CCE52D386f254917e481eB44e9943F39138')
# contract_abi = json.loads('')

# # Load the contract ABI
# with open(contract_abi, 'r') as file:
#     contract_abi = json.load(file)

# contract = web3.eth.contract(address=contract_address, abi=contract_abi)

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

# Initial dealing
for _ in range(2):
    dealCard(dealerHand)
    for hand in playerHands:
        dealCard(hand)

### Streamlit App Title ### Commenting out inputs that are replaced by streamlit functions
st.title('The Greatest Blackjack app ever developed')

# While loop chosen to constantly check participants hands for changes, selection of options, or bust scenario
while playerIn or dealerIn:
    # Player loop
    for index, playerHand in enumerate(playerHands):
        # Player while loop
        while playerIn:
            st.write(f'\nDealer has {revealDealerHand()}')
            st.write(f'Your hand {index+1}: {playerHand} for a total of {total(playerHand)}')
            display_hand(playerHand)
            # print(f'\nDealer has {revealDealerHand()}')
            # print(f'Your hand {index+1}: {playerHand} for a total of {total(playerHand)}')

            # Bust logic
            if total(playerHand) > 21:
                st.write('You bust!')
                # print("You bust!")
                playerIn = False  # Player out of game
                break  # Breaking loop for hand that busted
            
            # Split logic
            if check_for_split(playerHand) and not playerSplit:
                response = st.radio("Do you want to split your hand? (yes/no): ")
                # response = input("Do you want to split your hand? (yes/no): ")
                if response.lower() == 'yes':
                    playerHands = split_hand(playerHand)
                    playerSplit = True
                    break  # Exit the current loop to handle split hands

            # Options Logic
            options = st.radio("Select your move", ('Stay', 'Hit', 'Double Down'))
            # response = input('1: Stay\n2: Hit\n3: Double Down\n')
            if options == 'Stay':
                playerIn = False  # Instance where player decides to stay - not out of game
            elif options == 'Hit':
                dealCard(playerHand)
                # Because responses operate in a while loop, no need to check for total
                break
            elif options == 'Double Down':
                playerDoublesDown = double_down(playerHand)
                playerIn = False  # End turn after doubling down
            # if options == '1':
            #     playerIn = False #Instance where player decides to stay - not out of game
            # elif options == '2':
            #     dealCard(playerHand)
            #     # Because responces operate in a while loop, no need to check for total
            # elif options == '3' and len(playerHand) == 2:  # Checking if hand contains 2 cards
            #     playerDoublesDown = double_down(playerHand, player_money=100)  # Adjust for actual player money variable
            #     playerIn = False  # End turn after doubling down

        # Reset player hand for next hand or next round
        playerIn = True if playerHands and index + 1 < len(playerHands) else False

    # Dealer loop
    if dealerIn and any(total(hand) <= 21 for hand in playerHands):
        while total(dealerHand) < 17:  # Dealer must hit if total is less than 17
            dealCard(dealerHand)
        dealerIn = False  # Dealer's turn ends when they stand or bust
    
    # Exit the main loop if all player hands are done
    if not any(playerIn for playerHand in playerHands):  
        break

    # Dealer's turn
    if dealerIn:
        if total(dealerHand) > 16:
            dealerIn = False
        else:
            dealCard(dealerHand)
    
    # Exit the loop if both player and dealer are done
    if not playerIn and not dealerIn:
        break  

# Results
for index, playerHand in enumerate(playerHands):
    player_total = total(playerHand)
    dealer_total = total(dealerHand)
    st.write(f'\nYour hand {index+1}: {playerHand} for a total of {player_total}')
    display_hand(playerHand)
    st.write(f'Dealer\'s hand: {dealerHand} for a total of {dealer_total}')
    display_hand(dealerHand)
    # print(f'\nYour hand {index+1}: {playerHand} for a total of {player_total}')
    # print(f'Dealer\'s hand: {dealerHand} for a total of {dealer_total}')
    if player_total > 21:
        st.write('You bust! Dealer Wins.')
        # print('You bust! Dealer Wins.')
    elif dealer_total > 21 or player_total > dealer_total:
        st.write('You win!')
        # print('You win!')
    elif player_total < dealer_total:
        st.write('Dealer wins.')
        # print('Dealer wins.')
    else:  # player_total == dealer_total
        st.write("Push. It's a tie!")
        # print('Push. It\'s a tie!')

    if playerDoublesDown:
        st.write("Note: You doubled down this round.")
        # print("Note: You doubled down this round.")
