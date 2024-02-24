import streamlit as st
import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def value(self):
        if self.rank.isdigit():
            return int(self.rank)
        elif self.rank in ['Jack', 'Queen', 'King']:
            return 10
        else:
            return 11  # Ace

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades'] for rank in
                      ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']]
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            self.__init__()
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = sum(card.value() for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == 'A')
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

def display_hand(hand, hide_first_card=False):
    """
    Function to display a hand.
    """
    for card in hand:
        if hide_first_card and card == hand[0]:
            st.image('Resources/back.png', width=100)
        else:
            image_path = f"Resources/{card.rank}_{card.suit}.png"
            st.image(image_path, width=100)

def play_blackjack():
    st.title("Blackjack")
    st.write("Welcome to the game of Blackjack!")

    deck = Deck()

    player_hand = Hand()
    dealer_hand = Hand()

    # Initial deal
    player_hand.add_card(deck.draw())
    player_hand.add_card(deck.draw())
    dealer_hand.add_card(deck.draw())

    st.subheader("Dealer's Hand")
    display_hand(dealer_hand.cards, hide_first_card=True)

    st.subheader("Your Hand")
    display_hand(player_hand.cards)

    # Player's turn
    while st.button("Hit"):
        player_hand.add_card(deck.draw())
        display_hand([player_hand.cards[-1]])

        if player_hand.get_value() > 21:
            st.write("You busted! Dealer wins.")
            return

    st.write("You chose to stand.")

    # Dealer's turn
    st.subheader("Dealer's Turn")
    display_hand(dealer_hand.cards)

    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.draw())
        display_hand([dealer_hand.cards[-1]])

    if dealer_hand.get_value() > 21:
        st.write("Dealer busted! You win.")
        return

    # Compare hands
    player_score = player_hand.get_value()
    dealer_score = dealer_hand.get_value()

    if player_score > dealer_score:
        st.write("You win!")
    elif player_score < dealer_score:
        st.write("Dealer wins!")
    else:
        st.write("It's a tie!")

play_blackjack()
