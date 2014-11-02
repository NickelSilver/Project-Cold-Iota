__author__ = 'Andrea'

from menus.option import *
from menus.cursor import *
class Menu:

    #menus should have a list of options (tabs) for the user to select from
    #also make menu manager class
    def __init__(self, optionList = [], name = '', xpos = 0, ypos = 0, width = 640, height = 480):
        self.options = optionList
        self.name = name
        self.cursor = Cursor()
        self. x = xpos
        self.y = ypos
        self.width = width
        self.height = height

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def moveCursorUp(self):
        self.cursor.moveUp()
        return self.cursor.getPos()

    def moveCursorDown(self):
        count =self.cursor.getCount() +1
        if not count>=len(self.options):
            self.cursor.moveDown()
        return self.cursor.getPos()


    def getAllOptions(self):
        optionList = ''
        if len(self.options)!=0:
            for option in self.options:
                optionList+=option.getName()+'\n'

        return optionList

    def getSelectedOption(self, count):
        if not count>=len(self.options):
            option = self.options[count]
        return option



    def addOption(self, option):
        self.options.append(option)


    def getLinkedMenu(self, option):
        return option.getLink()

    def setImage(self, image):
        self.image = image

    def getImgae(self):
        return self.image