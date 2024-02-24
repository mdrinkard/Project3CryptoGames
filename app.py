import random
import streamlit as st
from web3 import Web3
import streamlit
import json
from PIL import Image
import BlackjackFunctions as bf

### Streamlit App Title ### 
st.title('The Greatest Blackjack app ever developed')

### Game loop ###
if st.button('New Hand'):
    bf.deal_initial_cards()
    bf.player_turn()
