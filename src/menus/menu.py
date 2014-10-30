__author__ = 'Andrea'

from option import Option
class Menu:

    #menus should have a list of options (tabs) for the user to select from
    def __init__(self, optionList = [], name = ''):
        self.options = optionList
        self.name = name


    def getAllOptions(self):
        optionList = ''
        if len(self.options)!=0:
            for option in self.options:
                optionList+=option+'\n'
        return optionList

    def getSelectedOption(self, optionName):
        x = 0
        found = False
        while not found and x<len(self.options):
            possible = self.options[x]
            if optionName!=possible.getName:
                x+=1
            else:
                found = True
        if found:
            return possible


    def addOption(self, option):
        self.options.append(option)


    def getLinkedMenu(self, option):
        return option.getLink()