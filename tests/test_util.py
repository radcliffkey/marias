# coding=utf-8
'''
Created on Mar 1, 2015

@author: Radoslav Klic
'''
import unittest

import util

class TestUtil(unittest.TestCase):
       
    def testRotateList(self):
        self.assertListEqual([], util.rotateList([], 10))
        self.assertListEqual([1,2,3,4,5], util.rotateList([1,2,3,4,5], 0))
        self.assertListEqual([3,4,5,1,2], util.rotateList([1,2,3,4,5], 2))
        self.assertListEqual([4,5,1,2,3], util.rotateList([1,2,3,4,5], -2))
        self.assertListEqual([3,4,5,1,2], util.rotateList([1,2,3,4,5], 7))
        self.assertListEqual([4,5,1,2,3], util.rotateList([1,2,3,4,5], -7))
        self.assertListEqual([1,2,3,4,5], util.rotateList(util.rotateList([1,2,3,4,5], -8), 8))
        