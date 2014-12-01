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
    def sellPlayerItem(self, item):
        #remove from shopkeeper's inventnory
        return self.inventory.removeItem(item)

    #shopkeeper will buy the item, player perspective
    def buyPlayerItem(self, item):
        return self.inventory.addItem()

    def itemExists(self, item):
        if self.inventory.countItems(item) > 0:
            return True

    def getRandomItem(self):
        print("hello")

if __name__ == '__main__':
    from shopkeeper import *
    from combat.hero import *
    keeper = shopkeeper(15)
    player = hero("Matt", 15)

    quit = False
    while not quit:
        hp, np = keeper.listItems()
        print("\nShop Items:  " + hp, np )

        item = input("\nPlease enter which item you'd like to buy.")
        if keeper.itemExists(item):
            soldItem = keeper.sellPlayerItem(item)
            player.buyItem(soldItem)
            print("Bought:  " + soldItem)
        else:
            print("Item does not exist.  Please enter exact name.")

        answer = input("\nEnter 1 to quit, 2 to buy an item. 3 to sell an item")
        if input == 1:
            quit = True
        elif input == 3:
            ""
            #list player items

