# coding=utf-8
'''
Created on Feb 22, 2015

@author: Radoslav Klic
'''

import random

class Suit:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
    
    def __repr__(self):
        return "{s} ({n})".format(s=self.symbol,n=self.name)

class Rank:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        
    def __repr__(self):
        return "{s} ({n})".format(s=self.symbol,n=self.name)

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __repr__(self):
        return self.suit.symbol + self.rank.symbol

class Deck:
    def __init__(self, cards):
        self.cards = cards
    
    def shuffle(self):
        random.seed()
        random.shuffle(self.cards)
    
    def addCards(self, cards):
        self.cards.extend(cards)
        
    def removeCards(self, cards):
        for card in cards:
            self.cards.remove(card)
    
    def __getitem__(self, idx):
        selCards = self.cards[idx]
        return Deck(selCards) if isinstance(idx, slice) else selCards 
    
    def __str__(self):
        return ', '.join(map(str, self.cards))

class GermanDeck(Deck):
    def __init__(self):
        cards = [Card(suit, rank) for suit in GERMAN_SUITS for rank in GERMAN_RANKS]
        Deck.__init__(self, cards)


RANK_7 = Rank("7", "7")
RANK_8 = Rank("8", "8")
RANK_9 = Rank("9", "9")
RANK_10 = Rank("10", "10")
RANK_UNTER = Rank("Unter", "U")
RANK_OBER = Rank("Ober", "O")
RANK_KING = Rank("King", "K")
RANK_ACE = Rank("Ace", "A")

GERMAN_RANKS = [
    RANK_7,
    RANK_8,
    RANK_9,
    RANK_10,
    RANK_UNTER,
    RANK_OBER,
    RANK_KING,
    RANK_ACE
]

SUIT_HEARTS = Suit("Hearts", "\u2665")
SUIT_BELLS = Suit("Bells", "\u2666")
SUIT_ACORNS = Suit("Acorns", "\u2663")
SUIT_LEAVES = Suit("Leaves", "\u2660")

GERMAN_SUITS = [
    SUIT_HEARTS,
    SUIT_BELLS,
    SUIT_ACORNS,
    SUIT_LEAVES,
]

def germanDefaultSortingKey(card):
    return GERMAN_SUITS.index(card.suit) * len(GERMAN_RANKS) + GERMAN_RANKS.index(card.rank)
