import random
from web3 import Web3
import streamlit
import json
from PIL import Image
# self.image_location = 'Resources/{}{}.png'.format(self.short_rank, self.short_suit)


### Card Class ###

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        if self.rank == 1:
            self.card_scores = [1, 11]
        elif self.rank >= 11 and self.rank <= 13:
            self.card_scores = [10, 10]
        else:
            self.card_scores = [self.rank, self.rank]

        if self.rank == 1:
            self.short_rank = 'A'
        elif self.rank == 11:
            self.short_rank = 'J'
        elif self.rank == 12:
            self.short_rank = 'Q'
        elif self.rank == 13:
            self.short_rank = 'K'
        else:
            self.short_rank = str(self.rank)

        if self.suit == 'Spades':
            self.short_suit = 'S'
        elif self.suit == 'Hearts':
            self.short_suit = 'H'
        elif self.suit == 'Clubs':
            self.short_suit = 'C'
        else:
            self.short_suit = 'D'

        self.image_location = 'Project3CryptoGames/Resources/{}{}.png'.format(self.short_rank, self.short_suit)

    def __repr__(self):
        true_rank = ''
        if self.rank == 1:
            true_rank = 'Ace'
        elif self.rank == 11:
            true_rank = 'Jack'
        elif self.rank == 12:
            true_rank = 'Queen'
        elif self.rank == 13:
            true_rank = 'King'
        else:
            true_rank = str(self.rank)
        return '{} of {}'.format(true_rank, self.suit)

### Deck Class
### Variables
suits = ('Spades', 'Hearts', 'Clubs', 'Diamonds')

class Deck:
    def __init__(self, number_of_decks):
        self.number_of_decks = number_of_decks
        self.cards = []
        self.create(self.number_of_decks)

    def __repr__(self):
        return 'Game deck has {} cards remaining'.format(len(self.cards))

    def create(self, number_of_decks):
        decks = [Card(rank, suit) for suit in suits for rank in range(1, 14)
                 for deck in range(number_of_decks)]
        decks = random.sample(decks, len(decks))
        self.cards.extend(decks)

    def draw(self):
        drawn_card = self.cards[0]
        self.cards.remove(self.cards[0])
        return drawn_card

    def reset(self):
        self.cards = []
        self.create(self.number_of_decks)

class Dealer:
    def __init__(self):
        self.cards = []
        self.hand_scores = [0, 0]
        self.best_outcome = 'Awaiting deal'

    def __repr__(self):
        return 'Dealer Hand: {}, Scores: {}, Best Outcome: {}'.format(self.cards, list(set(self.hand_scores)), self.best_outcome)

    def hit(self, game_deck):
        draw_card = game_deck.draw()
        self.cards.append(draw_card)
        card_scores = draw_card.card_scores
        self.hand_scores = [a + b for a,
                            b in zip(self.hand_scores, card_scores)]
        if len(self.cards) <= 1:
            self.best_outcome = 'Awaiting Deal'
        elif 21 in self.hand_scores and len(self.cards) == 2:
            self.best_outcome = 'Blackjack'
        elif self.hand_scores[0] > 21 and self.hand_scores[1] > 21:
            self.best_outcome = 'Bust'
        else:
            self.best_outcome = max([i for i in self.hand_scores if i <= 21])

    def reset(self):
        self.cards.clear()
        self.hand_scores = [0, 0]
        self.best_outcome = 'Awaiting deal'

class Player(Dealer):
    def __init__(self):
        self.cards = []
        self.hand_scores = [0, 0]
        self.best_outcome = 'Awaiting deal'
        self.possible_actions = ['No deal yet']

    def __repr__(self):
        return 'Player Hand: {}, Scores: {}, Best Outcome: {}'.format(self.cards, list(set(self.hand_scores)), self.best_outcome)

    def stand(self, game_play):
        self.possible_actions = []
        game_play.commentary.append('Player is standing')

    def double_down(self, game_deck, game_play):
        self.hit(game_deck)
        game_play.commentary.append('Player is doubling down')
        self.possible_actions = []

    def player_hit(self, game_deck, game_play):
        self.hit(game_deck)
        game_play.commentary.append('Player has hit')
        self.get_possibilities(game_play)

    def get_possibilities(self, game_play):
        if self.best_outcome in ['Blackjack', 'Bust', 21]:
            self.possible_actions = []
            game_play.commentary.append('Player has no options')
        elif len(self.cards) == 2:
            self.possible_actions = ['Hit', 'Stand', 'Double Down']
            game_play.commentary.append(
                'Player can still hit, double down or stand')
        else:
            self.possible_actions = ['Hit', 'Stand']
            game_play.commentary.append('Player can still hit or stand')

    def reset(self):
        self.cards = []
        self.hand_scores = [0, 0]
        self.best_outcome = 'Awaiting deal'
        self.possible_actions = []
        self.has_doubled_down = False

class GamePlay:
    def __init__(self, player, dealer, game_deck, blackjack_multiplier):
        self.player = player
        self.dealer = dealer
        self.game_deck = game_deck
        self.blackjack_multiplier = blackjack_multiplier
        self.commentary = []

    def __repr__(self):
        return "Commentary: {}".format(self.commentary)

    def dealer_turn(self):
        self.dealer.hit(self.game_deck)
        if self.dealer.best_outcome == 'Blackjack':
            self.commentary.append('Dealer hit Blackjack')
        elif self.dealer.best_outcome == 'Bust':
            self.commentary.append('Dealer went Bust')
        elif int(self.dealer.best_outcome) < 17:
            self.commentary.append(
                'Dealer has {}, Dealer has to hit'.format(self.dealer.best_outcome))
            self.dealer_turn()
        elif int(self.dealer.best_outcome) == 17 and 1 in [card.rank for card in self.dealer.cards]:
            self.commentary.append('Dealer has a soft 17, Dealer has to hit')
            self.dealer_turn()
        else:
            self.commentary.append(
                'Dealer is proceeding with {}'.format(self.dealer.best_outcome))

    def update(self):
        if len(self.player.possible_actions) == 0:
            if self.player.best_outcome == 'Bust':
                self.commentary.append(
                    "Player busted. No need for Dealer to go. Player loses their initial bet")
            elif self.player.best_outcome == 'Blackjack' and self.dealer.cards[0].rank not in [1, 10]:
                self.commentary.append("Player has Blackjack. Dealer has no chance to hit Blackjack. Player wins {} times their initial bet".format(
                    str(self.blackjack_multiplier)))
            else:
                self.commentary.append("Dealer turn can proceed as normal")
                self.dealer_turn()
                if self.dealer.best_outcome == 'Bust':
                    self.commentary.append(
                        "Dealer busted. Player wins their initial bet")
                elif self.dealer.best_outcome == 'Blackjack' and self.player.best_outcome == 'Blackjack':
                    self.commentary.append(
                        "Dealer and Player both have Blackjack. Player retains their initial bet")
                elif self.dealer.best_outcome == 'Blackjack' and self.player.best_outcome != 'Blackjack':
                    self.commentary.append(
                        "Dealer has Blackjack. Player loses their initial bet")
                elif self.dealer.best_outcome != 'Blackjack' and self.player.best_outcome == 'Blackjack':
                    self.commentary.append("Player has Blackjack. Player wins {} times their initial bet".format(
                        str(self.blackjack_multiplier)))
                elif int(self.dealer.best_outcome) == int(self.player.best_outcome):
                    self.commentary.append(
                        "Dealer and Player have same score. Player retains their initial bet")
                elif int(self.dealer.best_outcome) > int(self.player.best_outcome):
                    self.commentary.append("Dealer has {} whereas Player has {}. Player loses their initial bet".format(
                        str(self.dealer.best_outcome), str(self.player.best_outcome)))
                else:
                    self.commentary.append("Dealer has {} whereas Player has {}. Player wins their initial bet".format(
                        str(self.dealer.best_outcome), str(self.player.best_outcome)))
        else:
            pass

    def reset(self):
        self.commentary = []

    def deal_in(self):
        self.dealer.reset()
        self.player.reset()
        self.game_deck.reset()
        self.reset()
        self.player.hit(self.game_deck)
        self.dealer.hit(self.game_deck)
        self.player.hit(self.game_deck)
        self.player.get_possibilities(self)
# # player_money = crypto implementation

# playerIn = True #In the game
# dealerIn = True  #In the game
# playerDoublesDown = False  # Track if player has chosen to double down
# playerSplit = False  # Track if player has chosen to split

# # Deck of Cards
# suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
# ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
# deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]


# # List of Player & Dealer hands
# playerHands = [[]]  
# dealerHand = []


# # Deals card in the beginning
# def dealCard(turn):
#     card = random.choice(deck)
#     turn.append(card)
#     deck.remove(card)

# # Function defining card total & face card values
# def total(hand):
#     """
#     Function to calculate the total value of a hand.
#     """
#     total = 0
#     num_aces = 0
#     for card in hand:
#         if card['rank'] in ['Jack', 'Queen', 'King']: # Converting String Values in dictionary into an int
#             total += 10
#         elif card['rank'] == 'Ace':
#             num_aces += 1
#             total += 11 # Ace = 11 first
#         else:
#             total += int(card['rank']) ### Is Calculating the total based on the value part in the dictionary
#     while total > 21 and num_aces:
#         total -= 10
#         num_aces -= 1 # Converting Ace to 1 if card total > 21 (if bust occurs with Ace in hand)
#     return total

# # streamlit function to show cards in app

# def display_hand(hand, hide_first_card=False):
#     """
#     Function to display a hand.
#     """
#     for card in hand:
#         if hide_first_card and card == hand[0]:
#             st.image('Resources/back.png', width=100)
#         else:
#             image_path = f"Resources/{card['rank']}_{card['suit']}.png"
#             st.image(image_path, width=100)

# # Function checking whether split is available
# def check_for_split(player_hand):
#     return len(player_hand) == 2 and player_hand[0] == player_hand[1]

# # Function defining 2 hands for players when chosen to split
# def split_hand(player_hand):
#     return [[player_hand[0]], [player_hand[1]]]

# # Function for checking/ adjusting total wallet for player based on hand (double_down)
# def double_down(player_hand, player_money):
#     if player_money >= 2:  # Assuming 1 is current bet, check if player has enough to double
#         dealCard(player_hand)
#         return True  # Player chose to double down
#     return False

# # Defining the reveal of the dealers hand at end of game
# def revealDealerHand():
#     if len(dealerHand) >= 2:
#         return dealerHand[0], 'X' # 'X' to hide dealer's second card
#     elif len(dealerHand) > 2:
#         return dealerHand[0], dealerHand[1:]
    
# def blackjack():
#     global playerHands, dealerHand
    
#     # Clear hands from previous rounds
#     playerHands = [[]]
#     dealerHand.clear()
    
#     # Deal 2 cards to dealer and player
#     for _ in range(2):
#         dealCard(dealerHand)
#         for hand in playerHands:
#             dealCard(hand)
    
#     # Displaying cards on Streamlit
#     st.subheader("Dealer's Hand:")
#     st.write(f'{dealerHand[1]}')
#     display_hand(dealerHand,hide_first_card=True)
#     st.subheader("Player's Hand(s):")
#     for hand in playerHands:
#         st.write(f"{hand}")
#         display_hand(hand,hide_first_card=False)

# # def hit_or_stay():
# #     hit_button = st.button("Hit")
# #     stay_button = st.button("Stay")

# #     if hit_button:
# #         return 'Hit'
# #     elif stay_button:
# #         return 'Stay'
# #     else:
# #         return None

# # def player_turn():
# #     global playerHands
    
# #     # Continue player's turn until they choose to stay or bust
# #     while True:
# #         decision = hit_or_stay()
# #         if decision == 'Hit':
# #             for hand in playerHands:
# #                 dealCard(hand)
# #             st.subheader("Player's Hand(s):")
# #             for hand in playerHands:
# #                 st.write(f"{hand}")
# #                 display_hand(hand, hide_first_card=False)
# #             total_value = total(playerHands[0])  # Assuming only one player for simplicity
# #             if total_value > 21:
# #                 st.write("Bust! Player's hand total exceeds 21.")
# #                 break
# #         else:
#             break