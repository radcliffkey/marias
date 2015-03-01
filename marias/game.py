'''
Created on Feb 22, 2015

@author: Radoslav Klic
'''

from deck import GermanDeck
from rules import StdGameRules

PLAYER_CNT = 3

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

def rotateList(l, firstIdx):
    return l[firstIdx:] +l[:firstIdx]

class Game:

    def __init__(self, players):
        self.players = players

        self.leaderIdx = 0
        self.deck = GermanDeck()
        self.deck.shuffle()
    
    def orderedPlayers(self):
        #starting from the leader
        return rotateList(self.players, self.leaderIdx)
            
    def deal(self):
        ordPlayers = self.orderedPlayers()
        ordPlayers[0].hand = self.deck[:7]
        ordPlayers[1].hand = self.deck[12:22]
        ordPlayers[2].hand = self.deck[22:32]
        
    def playOneGame(self):
        self.deal()
        
        ordPlayers = self.orderedPlayers()
        leader = ordPlayers[0]
        
        gameType = leader.selectGameType()
        print(gameType)
        
        leader.hand.addCards(self.deck[7:12])
        
        if isinstance(gameType, StdGameType):
            gameType = leader.specifyStdGame()
            print(gameType)
            print("Trump:", gameType.trump)
            print("Trump card:", gameType.revealedTrumpCard)
            self.rules = StdGameRules(gameType)
        else:
            raise Exception("Game type not supported")
        
        self.talon = leader.selectTalon(self.rules)
        print("Talon:", self.talon)
        
        leader.hand.removeCards(self.talon)
        
        scores = [0] * PLAYER_CNT
        
        table = []
        startingPlayerIdx = self.leaderIdx
        for i in range(10):
            absIndices = rotateList(list(range(PLAYER_CNT)), startingPlayerIdx)
            ordPlayers = rotateList(self.players, startingPlayerIdx)
            for player in ordPlayers:                    
                table.append(player.play(table, self.rules))
                print("Played:", table[-1])
            
            print("Table:", table)
            
            turnScores, takingPlayerIdx = self.rules.scoreTurn(table, ordPlayers)
            takingPlayerIdx = absIndices[takingPlayerIdx]
            print("Taking player: ", takingPlayerIdx + 1)
            for idx, score in zip(absIndices, turnScores):
                scores[idx] += score
            
            print("Scores:", scores)
            startingPlayerIdx = takingPlayerIdx
            
            table = []
        scores[startingPlayerIdx] += 10
        
        print("Scores:", scores)
        
        