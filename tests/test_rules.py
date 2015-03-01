# coding=utf-8
'''
Created on Mar 1, 2015

@author: Radoslav Klic
'''
import unittest

import rules
from game import StdGameType
from deck import Card
import deck
from player import Player

TRUMP_SUIT = deck.SUIT_LEAVES

class TestRules(unittest.TestCase):
 
    def setUp(self):
        self.stdRules = rules.StdGameRules(StdGameType(Card(TRUMP_SUIT, deck.RANK_9), False, False))
 
    def testRankValue(self):
        self.assertTrue(self.stdRules.rankValue(Card(deck.SUIT_LEAVES, deck.RANK_10))
                 > self.stdRules.rankValue(Card(deck.SUIT_LEAVES, deck.RANK_KING)))

    def testScoreTurn(self):
        p1 = Player("p1")
        p2 = Player("p2")
        p3 = Player("p3")
        
        p1.hand = deck.Deck([Card(TRUMP_SUIT, deck.RANK_OBER)])
        p2.hand = deck.Deck([Card(deck.SUIT_HEARTS, deck.RANK_KING)])
        p3.hand = deck.Deck([])
        
        players = (p1, p2, p3)
        
        tablesAndResults = (
            ((
               Card(deck.SUIT_HEARTS, deck.RANK_9),
               Card(deck.SUIT_HEARTS, deck.RANK_10),
               Card(deck.SUIT_HEARTS, deck.RANK_8)
            ), ([0, 10, 0], 1)), ((
               Card(deck.SUIT_HEARTS, deck.RANK_9),
               Card(deck.SUIT_HEARTS, deck.RANK_10),
               Card(deck.SUIT_HEARTS, deck.RANK_ACE)
            ), ([0, 0, 20], 2)), ((
               Card(deck.SUIT_HEARTS, deck.RANK_9),
               Card(deck.SUIT_HEARTS, deck.RANK_10),
               Card(deck.SUIT_BELLS, deck.RANK_ACE)
            ), ([0, 20, 0], 1)), ((
               Card(deck.SUIT_HEARTS, deck.RANK_9),
               Card(TRUMP_SUIT, deck.RANK_KING),
               Card(deck.SUIT_HEARTS, deck.RANK_8)
            ), ([0, 0, 0], 1)), ((
               Card(deck.SUIT_HEARTS, deck.RANK_9),
               Card(TRUMP_SUIT, deck.RANK_OBER),
               Card(TRUMP_SUIT, deck.RANK_KING)
            ), ([0, 0, 0], 2)), ((
               Card(deck.SUIT_HEARTS, deck.RANK_9),
               Card(deck.SUIT_HEARTS, deck.RANK_10),
               Card(TRUMP_SUIT, deck.RANK_8)
            ), ([0, 0, 10], 2)), ((
               Card(deck.SUIT_HEARTS, deck.RANK_9),
               Card(deck.SUIT_HEARTS, deck.RANK_10),
               Card(TRUMP_SUIT, deck.RANK_ACE)
            ), ([0, 0, 20], 2)), ((
               Card(deck.SUIT_HEARTS, deck.RANK_9),
               Card(TRUMP_SUIT, deck.RANK_10),
               Card(TRUMP_SUIT, deck.RANK_ACE)
            ), ([0, 0, 20], 2)), ((
               Card(deck.SUIT_HEARTS, deck.RANK_9),
               Card(deck.SUIT_HEARTS, deck.RANK_OBER),
               Card(deck.SUIT_HEARTS, deck.RANK_ACE)
            ), ([0, 20, 10], 2)), ((
               Card(TRUMP_SUIT, deck.RANK_KING),
               Card(deck.SUIT_HEARTS, deck.RANK_KING),
               Card(deck.SUIT_HEARTS, deck.RANK_ACE)
            ), ([50, 0, 0], 0))
                  
        )
        
        for cardsPlayed, scores in tablesAndResults:
            with self.subTest(cardsPlayed=cardsPlayed):       
                self.assertEqual(scores, self.stdRules.scoreTurn(cardsPlayed, players))
        