#Huutopussi AI
#Ideana tehda koneoppimalli joka pelaa korttipelia huutopussi. 
# %%

import random
import pandas as pd 
import sys


class Card:
    suits = ["\u2663", "\u2665", "\u2666", "\u2660"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self, suit=0, rank=0):
        """Default constructor """
        suit_name = ["C","H","D","S"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.suit = suit
        self.rank = rank
        self.name = suit_name[suit]+ranks[rank]

    def __str__(self):
        """Returns a human-readable string representation """
        return '%s %s' % (Card.suits[self.suit], Card.ranks[self.rank])
        
    def __lt__(self, other):
        """Overriding < operator """
        t1 = self.rank, self.suit
        t2 = other.rank, other.suit
        return t1 < t2


class Deck:
    def __init__(self):
        """Initializes the Deck with 36 cards."""
        self.cards = []
        for suit in range(4):
            for rank in range(4,13):
                card = Card(suit, rank)
                self.cards.append(card)
        self.shuffle()

    def __str__(self):
        """Returns a string representation of the deck."""
        res = []
        for card in self.cards:
            res.append(str(card))
        return ', '.join(res)

    def __len__(self):
        """Overriding len operator"""
        return len(self.cards)

    def add_card(self, card):
        """Adds a card to the deck."""
        self.cards.append(card)

    def pop_card(self, i=0):
        """Removes and returns a card from the deck.
        i: index of the card to pop; by default, pops the card on top of the deck
        """
        return self.cards.pop(i)

    def shuffle(self):
        """Shuffles the cards in this deck."""
        random.shuffle(self.cards)

    def sort(self):
        """Sorts the cards in ascending order."""
        self.cards.sort()



class Hand:
    """Represents a hand of playing cards."""

    def __init__(self):
        self.cards = []
        self.names = []

    
    def draw(self,Deck):
        added_card = Deck.pop_card()
        self.cards.append(added_card)
        self.names.append(added_card.name)

    def remove_card(self):
        single_card = str(input("Choose a card to remove"))
        if single_card in self.names:
            index = self.names.index(single_card)
            self.names.pop(index)

            print(f"Removed card {single_card}")
            return self.cards.pop(index)
        else:
            print("You dont have that card")

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return ', '.join(res)

class Player: ## describe a player
    def __init__(self,name):
        self.name = name
        self.hand = Hand()
        self.points = 0
    

    def roundwinner(self,huuto:int):
        """ increasing the points for a player """
        self.points += huuto
    def getpoints(self):
        """ get the points of  a player """
        return self.points

    def print_hand(self):
        return f"Players current hand {self.hand}"
    
    def __str__(self):
        return f"{self.name} has {self.points} points and his current hand is {self.hand}"





class Game: #This game always has 3 players
    def __init__(self):
        name1 = input("p1 name ") #names
        name2 = input("p2 name ")
        name3= input("p3 name")
        self.deck = Deck() #get empty deck for the game
        self.players = [Player(name1),Player(name2),Player(name3)] #save players as class player
        self.huudot = [0,0,0]
        self.dealer = 0

        

        
    
    def restart_game(self): #resets all variables important to the game. 
        for player in self.players:
            player.hand = Hand()
            player.points = 0
        self.deck = Deck()
        self.huudot = [0,0,0]
        self.dealer = 0
        

    def play_round(self,winner_n): #single tick to play. 
        played_cards= []
        for i in range(3):
            played_cards.append(self.players[(winner_n+i)%3].hand.remove_card())
            print(f"played {played_cards}")
        highest_card =pd.Series([played_cards[0].rank,played_cards[1].rank,played_cards[2].rank]).idxmax()
        print(f"highest card was {played_cards[highest_card]}. Winner is {self.players[highest_card]}")
        winner_n = (winner_n +highest_card)%3
        self.players[winner_n].roundwinner(1)
            
            

        
        
        

    def start_game(self):
        for player in self.players:
            for i in range(10):
                player.hand.draw(self.deck)
            print(player)
        devils_deck = self.deck
        bids = []
        bidders = [self.players[0].name, self.players[1].name, self.players[2].name]
        turn = 0
        passes = 0
        played_cards = []
        while passes < 2:
            new_bid = float(input(f"{bidders[turn]}, enter a new bid: "))
            if new_bid == 0:
                print(f"{bidders[turn]} has passed")
                passes +=1 
            if bids and new_bid <= bids[-1] and new_bid !=0:
                print("Bid must be higher than the previous bid.")
                continue
            bids.append(new_bid)
            if len(bids) == 1:
                turn = (turn + 1) % len(bidders)
                continue
            if bids[-1] != bids[-2]:
                print(f"{bidders[turn]} has placed a bid of {new_bid}.")
                turn = (turn + 1) % len(bidders)
            else:
                print(f"{bidders[turn]} has passed.")
                passes += 1
                turn = (turn + 1) % len(bidders)

        if len(bids) > 0:
            winner = self.players[(turn - 1) % len(bidders)]
            winner_n = (turn - 1) % len(bidders)
            print(f"The winner is {winner.name} with a bid of {bids[-1]}.")
        else:
            print("No bids were placed.")
        
        for x in range(6):
            winner.hand.draw(devils_deck)
            print(winner.hand)

        while True:
            if len(winner.hand.cards) > 10:
                winner.hand.remove_card()
            
            else: 
                while True:
                    if len(self.players[0].hand.cards) > 0:
                        self.play_round(winner_n)



        

        
            
        


        


                        
                

        
        


        


   
        

        

    





    

