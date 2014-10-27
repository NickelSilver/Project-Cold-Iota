__author__ = 'Andrea'
import unittest

from mapLogic import *

class tests(unittest.TestCase):


    def test_doMapLogic(self):
        self.assertTrue(doMapLogic("town1", 20, 30, "down"))



if __name__ == '__main__':
    unittest.main()