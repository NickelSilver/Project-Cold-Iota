__author__ = 'Andrea'

from menu import Menu

class Option:
    #each option in a menu should only be linked to one other menu, however options in that menu may each be linked to one more
    #and so on, this can be changed.  We can almost think of options as tabs in some cases

    def __init__(self):
        self.name = ''
        self.linked = False
        self.link = None

    def getLink(self):
        if self.linked:
            return self.link
        else:
            return None

    def setLink(self, menu):
        self.linked = True
        self.link.append(menu)

    def getName(self):
        return self.name



    def __str__(self):
        return ''+self.name