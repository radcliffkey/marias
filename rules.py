'''
Created on Feb 22, 2015

@author: Radoslav Klic
'''

import deck

class StdGameRules(object):
    '''
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

    def ranking(self, card):
        return StdGameRules.RANKING[card.rank]

    def __init__(self, gameType):
        self.gameType = gameType
    
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
            higherCards = [card for card in matchingSuitCards if self.ranking(card) > rankingToBeat]
            if not higherCards:
                return matchingSuitCards
            else:
                return higherCards
        else:
            trumpCards = [card for card in hand.cards if card.suit == self.gameType.trump]
            if not trumpCards:
                return list(hand.cards)
            rankingToBeat = self.getTrumpRankingToBeat(table)
            higherCards = [card for card in trumpCards if self.ranking(card) > rankingToBeat]
            if not higherCards:
                return trumpCards
            else:
                return higherCards

    def getSameSuitRankingToBeat(self, table):
        if len(table) == 1:
            return self.ranking(table[0])
        if table[1].suit == self.gameType.trump:
            return -1
        if table[1].suit == table[0].suit:
            return self.ranking(table[1])
        return -1
    
    def getTrumpRankingToBeat(self, table):
        if len(table) == 2 and table[1].suit == self.gameType.trump:
            return self.ranking(table[1])
        return -1
        