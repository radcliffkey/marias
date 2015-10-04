'''
Created on Feb 22, 2015

@author: Radoslav Klic
'''

import deck
from deck import Card
from player import ROLE_LEADER

BASE_GAME_COST = 1
BASE_7_COST = 1
SILENT_100_COST = 2

class StdGameRules:
    '''
    Rules of standard Marias game
    '''
    RANKING = {
         deck.RANK_7: 0,
         deck.RANK_8: 1,
         deck.RANK_9: 2,
         deck.RANK_UNTER: 3,
         deck.RANK_OBER: 4,
         deck.RANK_KING: 5,
         deck.RANK_10: 6,
         deck.RANK_ACE: 7
    }

    def __init__(self, gameType):
        self.gameType = gameType

    def rankValue(self, card):
        return StdGameRules.RANKING[card.rank]
    
    def takingValue(self, card, turnSuit):
        if card.suit == turnSuit:
            return self.rankValue(card)
        if card.suit == self.gameType.trump:
            return self.rankValue(card) + 8
        return 0
    
    def pointValue(self, card, player):
        if card.rank in (deck.RANK_10, deck.RANK_ACE):
            return (10, 0)
        if self.isMarriage(card, player):
            return (0, 40) if card.suit == self.gameType.trump else (0, 20)
        return (0, 0)
    
    def isMarriage(self, card, player):
        if card.rank == deck.RANK_OBER and Card(card.suit, deck.RANK_KING) in player.hand.cards:
            return True
        if card.rank == deck.RANK_KING and Card(card.suit, deck.RANK_OBER) in player.hand.cards:
            return True
        return False

    def isAllowedInTalon(self, card):
        return card.rank not in (deck.RANK_10, deck.RANK_ACE)
    
    def allowedTalonCards(self, hand):
        return list(filter(self.isAllowedInTalon, hand.cards))

    def allowedTurns(self, hand, table):
        if len(table) == 0:
            return list(hand.cards)
        
        suit = table[0].suit
        
        matchingSuitCards = [card for card in hand.cards if card.suit == suit]

        if matchingSuitCards:
            rankingToBeat = self.getSameSuitRankingToBeat(table)
            higherCards = [card for card in matchingSuitCards if self.rankValue(card) > rankingToBeat]
            if not higherCards:
                return matchingSuitCards
            else:
                return higherCards
        else:
            trumpCards = [card for card in hand.cards if card.suit == self.gameType.trump]
            if not trumpCards:
                return list(hand.cards)
            rankingToBeat = self.getTrumpRankingToBeat(table)
            higherCards = [card for card in trumpCards if self.rankValue(card) > rankingToBeat]
            if not higherCards:
                return trumpCards
            else:
                return higherCards

    def getSameSuitRankingToBeat(self, table):
        if len(table) == 1:
            return self.rankValue(table[0])
        if table[1].suit == self.gameType.trump:
            return -1
        if table[1].suit == table[0].suit:
            return self.rankValue(table[1])
        return -1
    
    def getTrumpRankingToBeat(self, table):
        if len(table) == 2 and table[1].suit == self.gameType.trump:
            return self.rankValue(table[1])
        return -1
    
    def scoreTurn(self, cardsPlayed, players):
        turnSuit = cardsPlayed[0].suit
        maxTakeValue = -1
        takingPlayerIdx = -1
        takingPlayerScore = 0
        scores = [0] * len(players)
        for i in range(len(players)):
            takeValue = self.takingValue(cardsPlayed[i], turnSuit)
            if takeValue > maxTakeValue:
                maxTakeValue = takeValue
                takingPlayerIdx = i
            takePoints, playerPoints = self.pointValue(cardsPlayed[i], players[i])
            scores[i] += playerPoints
            takingPlayerScore += takePoints
        scores[takingPlayerIdx] += takingPlayerScore
        
        return scores, takingPlayerIdx
    
    def cardSortingKey(self, card):
        return deck.GERMAN_SUITS.index(card.suit) * len(deck.GERMAN_RANKS) + self.rankValue(card)
    
    def sortedCards(self, cards):
        return sorted(cards, key = self.cardSortingKey)   
    
    def above100Gain(self, score):
        if score >= 100:
            return SILENT_100_COST * (score - 90) / 10
        else:
            return 0
    
    def moneyGains(self, players, scores, turnHistory):
        if self.gameType.is100 or self.gameType.is7:
            raise Exception("Announced 100 or announced 7 not supported yet")
        
        leaderWonGame = False
        leaderWon7 = False
        coopWon7 = False
        leader7killed = False
        coop7killed = False
        
        leaderScore = 0
        coopScore = 0
        
        leaderGain = 0
        coopGain = 0
        
        for player, score, idx in zip(players, scores, range(len(players))):
            if player.role == ROLE_LEADER:
                leaderScore += score
                leaderIdx = idx
            else:
                coopScore += score
        
        if leaderScore == coopScore:
            raise Exception("Leader and opposition scores cannot be equal.")
        if leaderScore > coopScore:
            leaderWonGame = True

        lastTurnCards, startIdx, takingIdx =  turnHistory[-1]
        try:
            trump7Idx = lastTurnCards.index(deck.Card(self.gameType.trump, deck.RANK_7))
            if trump7Idx == takingIdx:
                if takingIdx == leaderIdx:
                    leaderWon7 = True
                else:
                    coopWon7 = True
            else:
                if trump7Idx == leaderIdx:
                    leader7killed = True
                else:
                    coop7killed = True
        except ValueError:
            pass
            
        if leaderWonGame:
            gameGain = 2 * (2 * BASE_GAME_COST + self.above100Gain(leaderScore))
            leaderGain += gameGain
            coopGain -= gameGain          
        else:
            gameGain = 2 * (2 * BASE_GAME_COST + self.above100Gain(coopScore))
            coopGain += gameGain
            leaderGain -= gameGain
        
        if leaderWon7 or coop7killed:
            silent7Gain = 2 * BASE_7_COST
            leaderGain += silent7Gain
            coopGain -= silent7Gain
        elif coopWon7 or leader7killed:
            silent7Gain = 2 * BASE_7_COST
            leaderGain -= silent7Gain
            coopGain += silent7Gain
        
        gains = [coopGain / 2] * len(players)
        gains[leaderIdx] = leaderGain
        
        if self.gameType.trump == deck.SUIT_HEARTS:
            gains = [2 * g for g in gains]
        
        return gains