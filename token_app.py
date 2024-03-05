import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(("http://127.0.0.1:7545")))

################################################################################
# The Load_Contract Function
################################################################################


@st.cache_resource()
def load_contract():

    # Load the contract ABI
    with open(Path(r'C:/Users/ryans/Ryans/Project3CryptoGames/Complied/BlackJack_ABI_file.json')) as f:
        artwork_abi = json.load(f)

    contract_address = ("0xC7362734c0F93549de6A773e07D969833F523594")

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

contract = load_contract()
################################################################################
# Token Balance Function
################################################################################

def get_token_balance(player_address):

    return contract.functions.balanceOf(player_address).call()

#Display token balances of player

def display_player_balances():

    st.write("Token Balances:")
    for player_address in player_address:
        balance = get_token_balance(player_address)
        st.write(f"Player {player_address}: {balance} tokens")

player_accounts = w3.eth.accounts

selected_account = st.selectbox("Select Player Account",  options= player_accounts)


################################################################################
# Display a Token
################################################################################
#st.markdown("## Check Balance of an Account")

tokens = contract.functions.balanceOf(selected_account).call()

st.write(f"This address owns {tokens} tokens")

#st.markdown("## Check  Ownership and Display Token")

#total_token_supply = contract.functions.totalSupply().call()

#token_id = st.selectbox("Artwork Tokens", list(range(total_token_supply)))

#if st.button("Display"):

    # Get the art token owner
    #owner = contract.functions.ownerOf(token_id).call()
    
    #st.write(f"The token is registered to {owner}")

    # Get the art token's URI
    #token_uri = contract.functions.tokenURI(token_id).call()

    #st.write(f"The tokenURI is {token_uri}")
    #st.image(token_uri)

