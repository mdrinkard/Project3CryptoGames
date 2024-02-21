import random
from web3 import Web3
import streamlit
import json

# Connect to Ganache
ganache_url = "HTTP://127.0.0.1:7545"  # Replace with your Ganache instance URL
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Verify Ganache connection
print(web3.is_connected())

# Setting contract address to the smart contracts and ABI to define the smart contract interaction
contract_address = web3.to_checksum_address('0xd9145CCE52D386f254917e481eB44e9943F39138')
contract_abi = 'abi.json'

# Load the contract ABI
with open(contract_abi, 'r') as file:
    contract_abi = json.load(file)

# The contract object. This allows us to begin automating the transactions based on the Blackjack events
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def place_bet(player_address, bet_amount_ether):
    # Convert bet amount from Ether to Wei
    bet_amount_wei = web3.toWei(bet_amount_ether, 'ether')

    # Build the transaction
    transaction = contract.functions.placeBet().buildTransaction({
        'from': player_address,
        'value': bet_amount_wei,
        'gas': 2000000,
        'nonce': web3.eth.getTransactionCount(player_address)
    })

    # Signing transaction
    signed_txn = web3.eth.account.signTransaction(transaction, private_key='')

    # Sending transaction
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    # Mining takes place here
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return receipt

# def payout_winnings(player_address, ether_bet):
#     # Convert amount from Ether to Wei
#     amount_wei = web3.toWei(ether_bet, 'ether')
#     player_address = input('Enter address: ',)

# def dealer_winings(dealer_address, ether_bet):
#     amount_wei = web3.toWei(ether_bet, 'ether')
#     dealer_address = '0xbd9fC2a58462A9303305E7E50ff72e44A815F8E8'

# player_money = crypto implementation

playerIn = True #In the game
dealerIn = True  #In the game
playerDoublesDown = False  # Track if player has chosen to double down
playerSplit = False  # Track if player has chosen to split

# Deck of Cards
deck = [2,3,4,5,6,7,8,9,10,'J','Q','K','A'] * 4 

# List of Player & Dealer hands
playerHands = [[]]  
dealerHand = []

# Deals card in the beginning
def dealCard(turn):
    card = random.choice(deck)
    turn.append(card)
    deck.remove(card)

# Function defining card total & face card values
def total(turn):
    total = 0
    ace_count = turn.count('A')
    for card in turn:
        if card in ['J', 'K', 'Q']:
            total += 10
        elif card == 'A':
            total += 11  # Ace = 11 first
        else:
            total += card
    while total > 21 and ace_count:
        total -= 10  
        ace_count -= 1 # Converting Ace to 1 if card total > 21 (if bust occurs with Ace in hand)
    return total

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

# While loop chosen to constantly check participants hands for changes, selection of options, or bust scenario
while playerIn or dealerIn:
    # Player loop
    for index, playerHand in enumerate(playerHands):
        # Player while loop
        while playerIn:  
            print(f'\nDealer has {revealDealerHand()}')
            print(f'Your hand {index+1}: {playerHand} for a total of {total(playerHand)}')

            # Bust logic
            if total(playerHand) > 21:
                print("You bust!")
                playerIn = False  # Player out of game
                break  # Breaking loop for hand that busted
            
            # Split logic
            if check_for_split(playerHand) and not playerSplit:
                response = input("Do you want to split your hand? (yes/no): ")
                if response.lower() == 'yes':
                    playerHands = split_hand(playerHand)
                    playerSplit = True
                    break  # Exit the current loop to handle split hands

            # Options Logic
            response = input('1: Stay\n2: Hit\n3: Double Down\n')
            if response == '1':
                playerIn = False #Instance where player decides to stay - not out of game
            elif response == '2':
                dealCard(playerHand)
                # Because responces operate in a while loop, no need to check for total card value
            elif response == '3' and len(playerHand) == 2:  # Checking if hand contains 2 cards
                playerDoublesDown = double_down(playerHand, player_money=100)  # Adjust for actual player money variable
                playerIn = False  # End turn after doubling down

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
    print(f'\nYour hand {index+1}: {playerHand} for a total of {player_total}')
    print(f'Dealer\'s hand: {dealerHand} for a total of {dealer_total}')
    if player_total > 21:
        #payout_winnings(player_address= '0xbd9fC2a58462A9303305E7E50ff72e44A815F8E8', ether_bet = bet_amount)
        print('You bust! Dealer Wins.')
    elif dealer_total > 21 or player_total > dealer_total:
        #payout_winnings(player_address= '0xD89307fd27d041632e864fd416d6d1FbcF3dCB80', ether_bet = bet_amount)
        print('You win!')
    elif player_total < dealer_total:
        #payout_winnings(player_address= '0xbd9fC2a58462A9303305E7E50ff72e44A815F8E8', ether_bet = bet_amount)
        print('Dealer wins.')
    else:  # layer_total == dealer_total
        #payout_winnings(player_address= '0xD89307fd27d041632e864fd416d6d1FbcF3dCB80', dealer_address, ether_bet = bet_amount/ 2)
        print('Push. It\'s a tie!')

    if playerDoublesDown:
        print("Note: You doubled down this round.")
