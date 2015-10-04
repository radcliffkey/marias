'''
Created on Feb 22, 2015

@author: Radoslav Klic
'''

from game import Game
from player import Player


def main():
    p1 = Player("1")
    p2 = Player("2")
    p3 = Player("3")
    game = Game([p1, p2, p3])
    
    game.playOneGame()
    
    print(p1)
    print(p2)
    print(p3)

if __name__ == '__main__':
    main()
