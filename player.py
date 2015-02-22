'''
Created on Feb 22, 2015

@author: Radoslav Klic
'''
import random
import deck
from deck import Deck
from game import StdGameType

class Player:

    def __init__(self, name):
        self.name = name
        self.hand = Deck([])

    def __str__(self, rules = None):
        if not rules:
            sortKey = deck.germanDefaultSortingKey
        return "name: {name}, hand: {hand}".format(name=self.name, hand=sorted(self.hand, key=sortKey))
    
    def pickTrumpCard(self):
        return self.hand[0]
    
    def selectGameType(self):
        trumpCard = self.pickTrumpCard()
        self.selectedGameType = StdGameType(trumpCard, False, False)
        return self.selectedGameType

    def specifyStdGame(self):
        return self.selectedGameType
    
    def selectTalon(self, rules):
        print("I have: " + str(self.hand))
        allowedCards = rules.allowedTalonCards(self.hand)
        if isinstance(rules.gameType, StdGameType):
            allowedCards = list(filter(lambda c: c.suit != rules.gameType.trump, allowedCards))
        
        print("Talon candidates: ", allowedCards)
        talon = allowedCards[:2]

        return talon
    
    def play(self, table, rules):
        allowedTurns = rules.allowedTurns(self.hand, table)
        print(self)
        print("Allowed turns", allowedTurns)
        selCardList = random.sample(allowedTurns, 1)
        self.hand.removeCards(selCardList)
        
        return selCardList[0]
    