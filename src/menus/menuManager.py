__author__ = 'Andrea'
from menus.battleMenu import BattleMenu
from menus.pauseMenu import PauseMenu
from menus.startMenu import StartMenu
from menus.menu import Menu
from menus.option import Option

menuList = []

def createMenus():
    global menuList

    confirmationMenu = Menu(['yes','no'],name='Are you sure?', width=320, height= 240)

    #---------------------pause menu--------------------
    save = Option('save')
    save.setLink(confirmationMenu)
    load = Option('load')
    load.setLink(confirmationMenu)
    inventory = Option('inventory')
    #link to inventory menu
    equipment = Option('equipment')
    #link to equipment menu
    map = Option('map')
    #link to the map
    settings = Option('settings')
    #link to setting menu
    exitOut = Option('exit')
    exitOut.setLink(confirmationMenu)
    pauseOptions = [save,load,inventory,equipment,map,settings,exitOut]

    pauseM = PauseMenu(pauseOptions,'Paused')

    #-----------------------start screen menu--------------------------------
    newGame = Option('new game')
    startOptions = [newGame, load, settings]

    startM = StartMenu(startOptions,'Main menu')


    #-----------------------------battle menu---------------------------------
    battleM = BattleMenu()




    #build menu list
    menuList.append(startM)
    menuList.append(pauseM)
    menuList.append(battleM)

def getMenuList():
    global menuList
    return menuList