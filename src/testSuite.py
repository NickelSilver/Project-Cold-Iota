__author__ = 'Andrea'
import unittest
from npcs.npc import *
from mapLogic import *
from menus.menu import *
from menus.cursor import *
from menus.option import *
from data.Game import *
from data.xmlParser import *
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

    #----------------------Menu tests----------------------------
    def testGetAllOptions(self):
        options = []
        option1 = Option('option1')
        option2 = Option('option2')
        option3 = Option('option3')
        options.append(option1)
        options.append(option2)
        options.append(option3)
        optionString = option1.getName()+'\n'+option2.getName()+'\n'+option3.getName()+'\n'
        menu1 = Menu(options,'menu 1')
        self.assertEqual(optionString, menu1.getAllOptions())

    def testGetSelectedOption(self):
        options = []
        option1 = Option('option1')
        option2 = Option('option2')
        option3 = Option('option3')
        options.append(option1)
        options.append(option2)
        options.append(option3)
        menu1 = Menu(options,'menu 1')
        self.assertEqual(option1.getName(),menu1.getSelectedOption().getName())

    #-------------------option/menu tests---------------------------------
    def testGetLink(self):
        options = []
        option1 = Option('option1')
        option2 = Option('option2')
        option3 = Option('option3')
        options.append(option1)
        options.append(option2)
        options.append(option3)
        menu1 = Menu(options,'menu 1')
        menu2 = Menu(['yes','no'],'menu2')
        option1.setLink(menu2)
        selected = menu1.getSelectedOption()
        self.assertEqual(menu2.getName(),menu1.getLinkedMenu(selected).getName())

    #------------------cursor/menu tests-------------------------------
    def testMoveCursor(self):
        options = []
        option1 = Option('option1')
        option2 = Option('option2')
        option3 = Option('option3')
        options.append(option1)
        options.append(option2)
        options.append(option3)
        menu1 = Menu(options,'menu 1')
        menu1.cursor.setCount(1)
        pos = menu1.moveCursorUp()
        pos = menu1.moveCursorUp() #this line has no effect because there is handling in the cursor class
        self.assertEqual((0,5),pos)
        pos = menu1.moveCursorDown()
        pos = menu1.moveCursorDown()
        pos = menu1.moveCursorDown()#this line has no effect because there is handling in the menu class for when someone
        #tries to go beyond the bottom of the menu
        self.assertEqual((0,-5),pos)

    #------------------Game state-------------------------------
    def testGameSave(self):
        Game1 = Game()

        #write generic tests to file.
        Game1.setGameFile("Test.txt")
        Game1.setMap("map1")
        Game1.setProgress("Progress1")

        Game1.saveGame()

        #load back game
        gamedata = Game1.loadGame()

        #print(gamedata)
        pass

    def testDialogue(self):

        reader = xmlParser()
        CharacterList, TextList = reader.readDialogue(1)
        for x in range(len(TextList)):
            CharacterList[x],TextList[x]
        pass



if __name__ == '__main__':
    unittest.main()