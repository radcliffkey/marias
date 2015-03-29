'''
Created on Mar 29, 2015

@author: Radoslav Klic
'''

class StdGameType:
    def __init__(self, trumpCard, is100, is7):
        self.trump = trumpCard.suit
        self.revealedTrumpCard = trumpCard
        self.is100 = is100
        self.is7 = is7

class BetlGameType:
    pass

class DurchGameType:
    pass
