import random
from web3 import Web3
import streamlit
import json
from PIL import Image

class Wallet:
    def __init__(self, initial_balance):
        self.wallet_balance = initial_balance
        self.current_bet = 0
    
    def place_bet(self, amount, player):
        if amount <= self.wallet_balance:
            self.wallet_balance -= amount
            player.current_bet = amount  # Update the current_bet attribute in the Player class
            return True  # Return True if the bet was successfully placed
        else:
            print('Insufficient balance')
            return False  # Return False if the bet couldn't be placed
        
    def adjust_balance(self, outcome):
        if outcome == 'win':
            self.wallet_balance += self.current_bet * 2
        elif outcome == 'blackjack':
            self.wallet_balance += self.current_bet * 3
        elif outcome == 'loss':
            self.wallet_balance -= self.current_bet
        else:
            self.wallet_balance += self.current_bet
        return self.wallet_balance
    
class Card:
### This is the constructor method __init__() for the Card class. It is called when a new Card object is created.
### It takes two parameters, rank and suit, which represent the rank and suit of the card, respectively.
    def __init__(self, rank, suit):
### These lines initialize the instance variables rank and suit with the values passed to the constructor.
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

        self.image_location = 'Resources/{}{}.png'.format(self.short_rank, self.short_suit)

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

#### Dealer Class

class Dealer:
    def __init__(self):
        self.cards = []
        self.hand_scores = [0,0]
        self.best_outcome = 'Awaiting Deal'

    def __repr__(self):
        return 'Dealer Hand: {}, Scores: {}, Best Outcome: {}'.format(self.cards, list(set(self.hand_scores)), self.best_outcome)
    
    def hit(self,game_deck):
        draw_card = game_deck.draw()
        self.cards.append(draw_card)
        card_scores = draw_card.card_scores
        self.hand_scores = [a+b for a, b in zip(self.hand_scores, card_scores)]
        if len(self.cards) <= 1:
            self.best_outcome = 'Awaiting Deal'
        elif 21 in self.hand_scores and len(self.cards) == 21:
            self.best_outcome = 'Blackjack'
        elif self.hand_scores[0] > 21 and self.hand_scores[1] > 21:
            self.best_outcome = 'Bust'
        else:
            self.best_outcome = max([i for i in self.hand_scores if i <= 21])

    def reset(self):
        self.cards.clear()
        self.hand_scores = [0,0]
        self.best_outcome = 'Awaiting Deal'

class Player(Dealer):
    def __init__(self, wallet):
        super().__init__()
        self.wallet = wallet
        self.current_bet = 0
        self.cards = []  # Player's hand
        self.hand_scores = [0, 0]  # Possible scores for the hand, considering Ace as 1 or 11
        self.best_outcome = 'Awaiting deal'  # Best possible outcome based on the hand
        self.possible_actions = ['No deal yet']  # Available actions for the player

    def __repr__(self):
        return 'Player Hand: {}, Scores: {}, Best Outcome: {}'.format(self.cards, list(set(self.hand_scores)), self.best_outcome)

    def stand(self, game_play):
        self.possible_actions = []
        game_play.commentary.append('Player is standing')

    def double_down(self, game_deck, game_play):
        self.current_bet *= 2
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
        outcome = None
        if len(self.player.possible_actions) == 0:
            if self.player.best_outcome == 'Bust':
                self.commentary.append("Player busted. No need for Dealer to go. Player loses their initial bet")
                outcome = 'loss'
            elif self.dealer.best_outcome == 'Awaiting Deal':
                self.commentary.append("Dealer has not finished dealing. Please wait.")
            else:
                # Dealer turn can proceed as normal
                while int(self.dealer.best_outcome) < 17:
                    self.dealer_turn()
                # Check outcomes
                if self.dealer.best_outcome == 'Bust' or int(self.dealer.best_outcome) < int(self.player.best_outcome):
                    outcome = 'win'
                    self.commentary.append("Dealer has {} whereas Player has {}. Player wins their initial bet".format(
                        str(self.dealer.best_outcome), str(self.player.best_outcome)))
                elif int(self.dealer.best_outcome) == int(self.player.best_outcome):
                    self.commentary.append("Dealer and Player have same score. Player retains their initial bet")
                else:
                    outcome = 'loss'
                    self.commentary.append("Dealer has {} whereas Player has {}. Player loses their initial bet".format(
                        str(self.dealer.best_outcome), str(self.player.best_outcome)))
            
            if outcome:
                new_balance = self.player.wallet.adjust_balance(outcome)
                # Reset current bet
                self.player.current_bet = 0
        else:
            # Dealer turn not initiated yet
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

    # def update(self):
    #     outcome = None
    #     if len(self.player.possible_actions) == 0:
    #         if self.player.best_outcome == 'Bust':
    #             self.commentary.append(
    #                 "Player busted. No need for Dealer to go. Player loses their initial bet")
    #             outcome = 'loss'
    #         elif self.player.best_outcome == 'Blackjack' and self.dealer.cards[0].rank not in [1, 10]:
    #             outcome = 'blackjack'
    #             self.commentary.append("Player has Blackjack. Dealer has no chance to hit Blackjack. Player wins {} times their initial bet".format(
    #                 str(self.blackjack_multiplier)))
    #         else:
    #             self.commentary.append("Dealer turn can proceed as normal")
    #             self.dealer_turn()
    #             if self.dealer.best_outcome == 'Bust':
    #                 outcome = 'win'
    #                 self.commentary.append(
    #                     "Dealer busted. Player wins their initial bet")
    #             elif self.dealer.best_outcome == 'Blackjack' and self.player.best_outcome == 'Blackjack':
    #                 self.commentary.append(
    #                     "Dealer and Player both have Blackjack. Player retains their initial bet")
    #             elif self.dealer.best_outcome == 'Blackjack' and self.player.best_outcome != 'Blackjack':
    #                 outcome = 'loss'
    #                 self.commentary.append(
    #                     "Dealer has Blackjack. Player loses their initial bet")
    #             elif self.dealer.best_outcome != 'Blackjack' and self.player.best_outcome == 'Blackjack':
    #                 outcome = 'blackjack'
    #                 self.commentary.append("Player has Blackjack. Player wins {} times their initial bet".format(
    #                     str(self.blackjack_multiplier)))
    #             elif int(self.dealer.best_outcome) == int(self.player.best_outcome):
    #                 self.commentary.append(
    #                     "Dealer and Player have same score. Player retains their initial bet")
    #             elif int(self.dealer.best_outcome) > int(self.player.best_outcome):
    #                 outcome = 'loss'
    #                 self.commentary.append("Dealer has {} whereas Player has {}. Player loses their initial bet".format(
    #                     str(self.dealer.best_outcome), str(self.player.best_outcome)))
    #             else:
    #                 outcome ='win'
    #                 self.commentary.append("Dealer has {} whereas Player has {}. Player wins their initial bet".format(
    #                     str(self.dealer.best_outcome), str(self.player.best_outcome)))
            
    #         if outcome:
    #             new_balance = self.player.wallet.adjust_balance(outcome)

    #     else:
    #         pass