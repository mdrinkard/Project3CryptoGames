import streamlit as st
from PIL import Image
from BlackjackFunctions import GamePlay, Player, Dealer, Deck
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(("http://127.0.0.1:7545")))

@st.cache_resource()
def load_contract():

    # Load the contract ABI
    with open(Path(r'C:\Users\Micha\Bootcamp\Git\Project3CryptoGames\Complied\BlackJack_ABI_file.json')) as f:
        artwork_abi = json.load(f)

    contract_address = "0x5bEE276df94dC77BF665F3eFB86A0A6dFBBC41a9"

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

contract = load_contract()

# Game settings
number_of_decks = 6
blackjack_multiplier = 1.5
def get_balance(player_address):
    balance = w3.eth.get_balance(player_address)
    balance_conversion = balance / 10**18
    return balance_conversion



def display_player_balances(selected_account):
    eth_balance = get_balance(selected_account)
    st.write(f"ETH Balance: {eth_balance} ETH")


# Initialize player, dealer, deck, and gameplay. Cache these variables
@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def start_game():
    game_deck = Deck(number_of_decks)
    dealer = Dealer()
    player_accounts = w3.eth.accounts
    player = Player()  # Ensure Player class has balance and place_bet method
    player_eth_address = w3.eth.accounts[1]
    player_eth_balance = get_balance(player_eth_address)
    game_play = GamePlay(player, dealer, game_deck, blackjack_multiplier)
    return game_deck, dealer, player, player_eth_balance, player_accounts, game_play

game_deck, dealer, player, player_eth_balance, player_accounts, game_play = start_game()

st.title('BlackJack Simulator')

# Display current balances
selected_account = st.selectbox("Select Player Account",  options= player_accounts)
display_player_balances(selected_account)
#st.write(f"Player Balance: ${player_eth_balance} ETH")
st.write(f"Dealer Balance: ${dealer.balance}")  # Display the dealer's balance

bet_amount = st.number_input('Enter your bet for the next hand:', min_value=1, value=100, step=10, max_value=player.balance)

# Place bet
if st.button('Place Bet'):
    if player.place_bet(bet_amount):
        st.success(f'Bet of ${bet_amount} ETH placed. Good luck!')
    else:
        st.error('Insufficient balance. Please enter a smaller bet.')

# Ensure a bet is placed before starting a new hand
if st.button('New hand?'):
    if player.current_bet > 0:
        game_play.deal_in()
    else:
        st.error('Please place a bet before starting a new hand.')

# Game state updates and player actions
player_stats = st.empty()
player_images = st.empty()
player_hit_option = st.empty()
player_double_down_option = st.empty()
player_stand_option = st.empty()
dealer_stats = st.empty()
dealer_images = st.empty()
result = st.empty()

# Handling player actions: Hit, Stand, Double Down
if 'Hit' in player.possible_actions:
    if player_hit_option.button('Hit'):
        player.player_hit(game_deck, game_play)
        if 'Hit' not in player.possible_actions:
            player_hit_option.empty()

if 'Double Down' in player.possible_actions:
    if player_double_down_option.button('Double Down'):
        player.double_down(game_deck, game_play)
        player_double_down_option.empty()
        player_hit_option.empty()
        player_stand_option.empty()

if 'Stand' in player.possible_actions:
    if player_stand_option.button('Stand'):
        player.stand(game_play)
        player_hit_option.empty()
        player_double_down_option.empty()
        player_stand_option.empty()

# Update game state and display results
game_play.update()
player_stats.write(player)
player_images.image([Image.open(card.image_location) for card in player.cards], width=100)
dealer_stats.write(dealer)
dealer_images.image([Image.open(card.image_location) for card in dealer.cards], width=100)
result.write(game_play)