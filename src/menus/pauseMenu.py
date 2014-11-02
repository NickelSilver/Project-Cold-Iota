__author__ = 'Andrea'

from menus.menu import Menu

class PauseMenu(Menu):

    #for those I have deemed as other menus, probably will not need their own special classes since the basic functionality should
    #work for those classes on a basic level, fleshing inventory and equipment out are optional at the moment

    def pauseGame(self):
        #stop all movement in game, stop clocks, stop everything
        pass

    def saveGame(self):
        #implement save function here, note we are only going to alllow user's one save file for the time being
        pass

    def loadGame(self):
        #implement load function here
        pass

    def inventory(self):
        #show player their inventory, it'll probably be just another menu
        pass

    def equipment(self):
        #allow player to equip and unequip, again probably another menu
        pass

    def settings(self):
        #define settings here
        pass

    def quit(self):
        #allow user to quit game
        pass

    def map(self):
        #pull up map
        pass