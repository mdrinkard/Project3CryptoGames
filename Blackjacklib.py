import random

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
            total += 11  # initially treat ace as 11
        else:
            total += card
    while total > 21 and ace_count:
        total -= 10  # convert an ace from 11 to 1
        ace_count -= 1
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
                # Because responces operate in a while loop, no need to check for total
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
        print('You bust! Dealer Wins.')
    elif dealer_total > 21 or player_total > dealer_total:
        print('You win!')
    elif player_total < dealer_total:
        print('Dealer wins.')
    else:  # player_total == dealer_total
        print('Push. It\'s a tie!')

    if playerDoublesDown:
        print("Note: You doubled down this round.")
