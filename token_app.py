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
    with open(Path(r'C:/Users/ryans/Next/Ryans/Project3CryptoGames/Complied/BlackJack_ABI_file.json')) as f:
        artwork_abi = json.load(f)

    contract_address = "0x5bEE276df94dC77BF665F3eFB86A0A6dFBBC41a9"

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

def get_balance(player_address):
    balance = w3.eth.get_balance(player_address)

    balance_conversion = balance / 10**18
    return balance_conversion

#Display token balances of player

player_accounts = w3.eth.accounts

def display_player_balances(selected_account):
    eth_balance = get_balance(selected_account)
    st.write(f"Player {selected_account}: {eth_balance} ETH")

selected_account = st.selectbox("Select Player Account",  options= player_accounts)
display_player_balances(selected_account)
################################################################################
# Display a Token
################################################################################
#st.markdown("## Check Balance of an Account")

#eth = contract.functions.balanceOf(selected_account).call()

#st.write(f"This address owns {eth} chips")

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