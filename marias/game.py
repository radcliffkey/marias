'''
Created on Feb 22, 2015

@author: Radoslav Klic
'''

from util import rotateList
from deck import GermanDeck
from gameType import StdGameType
from rules import StdGameRules
from player import ROLE_LEADER, ROLE_COOP1, ROLE_COOP2

PLAYER_CNT = 3

class Game:

    def __init__(self, players):
        self.players = players

        self.leaderIdx = 0
        self.deck = GermanDeck()
        self.deck.shuffle()
    
    def orderedPlayers(self):
        # starting from the leader
        return rotateList(self.players, self.leaderIdx)
            
    def deal(self):
        ordPlayers = self.orderedPlayers()
        ordPlayers[0].hand = self.deck[:7]
        ordPlayers[1].hand = self.deck[12:22]
        ordPlayers[2].hand = self.deck[22:32]
        
    def playOneGame(self):
        self.deal()
        
        ordPlayers = self.orderedPlayers()
        ordPlayers[0].role = ROLE_LEADER
        ordPlayers[1].role = ROLE_COOP1
        ordPlayers[2].role = ROLE_COOP2
        
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
        
        talon = leader.selectTalon(self.rules)
        print("Talon:", talon)
        
        leader.hand.removeCards(talon)
        
        scores = [0] * PLAYER_CNT
        
        turnHistory = []

        # Cards played, ordered from the turn starting player's one
        table = []
        startingPlayerIdx = self.leaderIdx
        for i in range(10):
            table = []

            # Map relative index (to the turn starting player) -> absolute index
            absIndices = rotateList(list(range(PLAYER_CNT)), startingPlayerIdx)
            # ordered players from the turn starting player
            ordPlayers = rotateList(self.players, startingPlayerIdx)
            for player in ordPlayers:
                table.append(player.play(table, self.rules))
                print("Played:", table[-1])
            
            print("Table:", table)
                      
            turnScores, takingPlayerRelIdx = self.rules.scoreTurn(table, ordPlayers)
            takingPlayerIdx = absIndices[takingPlayerRelIdx]
            
            turnHistory.append((rotateList(table, startingPlayerIdx), startingPlayerIdx, takingPlayerIdx))
            print("Taking player: ", takingPlayerIdx + 1)
            for idx, score in zip(absIndices, turnScores):
                scores[idx] += score
            
            print("Scores:", scores)
            startingPlayerIdx = takingPlayerIdx
            
        scores[startingPlayerIdx] += 10
        
        print("Scores:", scores)
        
        moneyGains = self.rules.moneyGains(self.players, scores, turnHistory)

        print("Money gains:", moneyGains)
