__author__ = 'Andrea'
import unittest
from npcs.npc import *
from mapLogic import *


class tests(unittest.TestCase):

    #-----------------maplogictests-------------------------
    def test_doMapLogic(self):
        self.assertTrue(doMapLogic("town1", 20, 30, "down"))



    #-------------NPC tests-------------------------

    def testResponse(self):

        npc1 = npc("town1", 7, 7, "down", "sprites/npc1SpriteSheet1.png")
        npc2 = npc("town1", 7, 7, "down", "sprites/emoSpriteSheet.png")
        npc3 = npc("town1", 7, 7, "down", "sprites/goatBoySpriteSheet1.png")
        npc4 = npc("town1", 7, 7, "down", "sprites/holstaurusSpriteSheet.png")
        npc5 = npc("town1", 7, 7, "down", "sprites/horsinAroundSpriteSheet1.png")
        npc6 = npc("town1", 7, 7, "down", "sprites/monkeyBusinessSpriteSheet1.png")
        npc7 = npc("town1", 7, 7, "down", "sprites/mrPiddlesSpriteSheet1.png")

        print(npc3.getResponse())
        print(npc3.getResponse())
        print(npc3.getResponse())

        pass



if __name__ == '__main__':
    unittest.main()