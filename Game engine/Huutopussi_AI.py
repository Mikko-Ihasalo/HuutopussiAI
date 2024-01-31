#Huutopussi AI
#Ideana tehda koneoppimalli joka pelaa korttipelia huutopussi. 
# %%

import random
import pandas as pd 
import sys


class Card:
    suits = ["♣", "♠", "♦", "♥"] # suits of cards
    ranks = [ "6", "7", "8", "9", "10", "J", "Q", "K", "A"] # ranks

    def __init__(self, suit=0, rank=0): 
        self.suit = suit # card suit 
        self.rank = rank # card rank
        self.name = f"{Card.suits[suit]}{Card.ranks[rank]}" # card name

    def __str__(self):
        return f"{Card.suits[self.suit]} {Card.ranks[self.rank]}" # card suit and rank printed as it's name

    def __lt__(self, other):
        return (self.rank, self.suit) < (other.rank, other.suit) # comparison of 2 cards
    def __repr__(self):
        return f"{self.name}"


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in range(4) for rank in range(9)]
        self.shuffle() # Add cards to deck with suit and rank

    def __str__(self):
        return ', '.join(str(card) for card in self.cards) # print deck

    def __len__(self):
        return len(self.cards) # length of deck

    def add_card(self, card):
        self.cards.append(card) # add  a card

    def pop_card(self, i:int):
        return [self.cards.pop() for _ in range(i)] # delete i card's from deck

    def shuffle(self):
        random.shuffle(self.cards) # shuffle deck

    def sort(self):
        self.cards.sort()  # sort deck according to suit and rank



class Hand:
    """Represents a hand of playing cards."""

    def __init__(self):
        self.cards = [] # empty hand

    def draw(self, deck, n:int):
        added_card = deck.pop_card(n)
        self.cards.extend(added_card) # draw a card from a specific deck
    
    def remove_card(self):
        single_card = input("Choose a card to remove: ") # which card to remove
        for card in self.cards:
            if card.name == single_card: # if card is in hand
                self.cards.remove(card) # remove card
                print(f"Removed card {single_card}")
                return card
        print("You don't have that card") # card not in hand
        return None  # return None if the card is not found

        

    def __str__(self):
        return ', '.join(str(card) for card in self.cards) # print hand

class Player:
    def __init__(self, name): # player with name and empty hand 
        self.name = name
        self.hand = Hand()
        self.won_cards = Hand()
        self.points = 0

    def round_winner(self, huuto: int):
        """Increase the points for a player"""
        self.points += huuto # increase points

    def get_points(self):
        """Get the points of a player"""
        return self.points # get points

    def print_hand(self):
        return f"Player's current hand: {self.hand}" # print hand
    
    def print_won_cards(self):
        return f"Player's current hand: {self.hand}" # print won cards

    def __str__(self):
        return f"{self.name} has {self.points} points and their current hand is {self.hand}"

class BiddingSystem:
    def __init__(self, bidders):
        self.bidders = bidders
        self.current_bidder_index = 0
        self.current_bid = 0
        self.active_bidders = set(bidders)

    def place_bid(self, bidder, amount):
        if bidder == self.bidders[self.current_bidder_index] and amount > self.current_bid:
            self.current_bid = amount
            self.current_bidder_index = (self.current_bidder_index + 1) % len(self.bidders)

    def pass_bid(self, bidder):
        if bidder == self.bidders[self.current_bidder_index]:
            self.active_bidders.remove(bidder)
            self.current_bidder_index = (self.current_bidder_index + 1) % len(self.bidders)

    def run_bidding(self):
        while len(self.active_bidders) > 1:
            current_bidder = self.bidders[self.current_bidder_index]
            print(f"{current_bidder}, the current bid is {self.current_bid}. Your move.")
            action = input("Enter 'bid' to raise the bid or 'pass' to pass: ")
            if action == "bid":
                amount = int(input("Enter your bid amount: "))
                self.place_bid(current_bidder, amount)
            elif action == "pass":
                self.pass_bid(current_bidder)
            else:
                print("Invalid action. Please enter 'bid' or 'pass'.")

            print("")

        print(f"The winner is {list(self.active_bidders)[0]} with a bid of {self.current_bid}.")


class Game:
    def __init__(self):
        self.deck = Deck()  # Get a deck for the game 
        self.players = [Player(input("p1 name ")), Player(input("p2 name ")), Player(input("p3 name "))] # add players
        self.huudot = [0, 0, 0]
        self.dealer = 0

    def restart_game(self):  # Resets all variables important to the game
        for player in self.players:
            player.hand = Hand()
            player.points = 0
        self.deck = Deck()
        self.huudot = [0, 0, 0]
        self.dealer = 0

    def play_tick(self, winner_n):  # Single tick to play
        played_cards = []
        for i in range(3):
            played_cards.extend(self.players[(winner_n + i) % 3].hand.remove_card()) # make a list of played cards
            print(f"played {played_cards}") # print played cards
        highest_card_index = max(range(3), key=lambda i: played_cards[i].rank) # find index of highest card
        print(f"highest card was {played_cards[highest_card_index]}. Winner is {self.players[highest_card_index]}") # print who won
        winner_n = (winner_n + highest_card_index) % 3 # get the index of winner
        self.players[winner_n].won_cards.add_card(played_cards,3)
        self.players[winner_n].round_winner(1)
    
    def count_points(self):
            for player in self.players:
                points = 0
                for card in player.won_cards.cards:
                    if card.rank == 10 or card.rank == 13:
                        points += 10
                    elif card.rank >= 11:
                        points += 5
                player.points += points

    def start_round(self):
        for player in self.players: 
            player.hand.draw(self.deck,10) # deal cards
            print(player) # print players hands
        devils_deck = self.deck # devils deck of the cards not in any players hand
        bidding_system = BiddingSystem(self.players) # bidding phase
        bidding_system.run_bidding()
        winner_n = bidding_system.current_bidder_index # Winner of the bid
        winner = self.players[winner_n]


        winner.hand.draw(devils_deck,6)
        print(winner.hand) # winner gets devils deck

        while len(winner.hand.cards) > 10:
            winner.hand.remove_card() # remove cards from winner's hand until at 10 cards

        while len(self.players[0].hand.cards) > 0:
            self.play_tick(winner_n) # play rounds until no cards left
        self.count_points()
        print(self.players[0].points,self.players[1].points,self.players[2].points)