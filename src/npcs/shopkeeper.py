__author__ = 'Matt'
from combat.items.inventory import *
from npc import npc
class shopkeeper(npc):
    def __init__(self, level):
        self.inventory = inventory()
        #populates shop with 3 items at a time.
        for index in range(3):
            self.inventory.addHealthPotion(10*level,5*level)
            self.inventory.addManaPotion(15*level,5*level)

    def listItems(self):
        hp = "\nHealth Potions:  " + str(self.inventory.countItems("Health Potion"))
        mp = "\nMana Potions  " + str(self.inventory.countItems("Mana Potion"))

        return hp, mp

    #from player's perspective
    def buyItem(self, item):

        #remove from shopkeeper's inventnory
        return self.inventory.removeItem(item)

    def sellItem(self, item):
        ""


    def getRandomItem(self):
        print("hello")

if __name__ == '__main__':
    from shopkeeper import *
    keeper = shopkeeper(15)
    hp, np = keeper.listItems()
    print("Listed Items:  \n" + hp, np )
    print(keeper.inventory)
    print("Bought:  " + keeper.buyItem("Health Potion"))
