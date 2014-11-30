__author__ = 'Matt'

from item import *

class inventory():
    def __init__(self):
        #gather inventory from a saved file.
        self.inventory = []
        self.itemCount = 0

    def loadInventory(self, items):
        for item in range(items.count):
            self.inventory.addItem(item)

    def addItem(self, item):
        self.inventory.append(item)
        return "You picked up ",item,"! You can find it in your inventory."
        #remove item by index

    def addHealthPotion(self, price, value):
        hp = item()
        hp.name = "Health Potion"
        hp.description = "Increase hp by" + str(value) + "\n" + "Sell Value:  " + str(price)
        hp.price = price
        hp.value = value
        self.addItem(hp)

    def addManaPotion(self, price, value):
        mp = item()
        mp.name = "Mana Potion"
        mp.description = "Increases mana by" + str(value) + "\n" + "Sell Value:  " + str(price)
        mp.price = price
        mp.value = value
        self.addItem(mp)

    def removeItem(self, index):
        tempItem = self.inventory[index]

        self.inventory.remove(tempItem)
        return "Removed ",tempItem.name,"from inventory."

    #counts the number of items in an inventory e.g. 3 health potions.
    def countItems(self, item):
        return self.inventory.count(item)




if __name__ == '__main__':

    from inventory import inventory
    testInv = inventory()
    testInv.addItem("Health Potion")
    testInv.addItem("Mana Potion")
    testInv.addItem("Health Potion")
    testInv.addHealthPotion(50,5)

    print(testInv.countItems("Health Potion"))
    #print(testInv.removeItem(0))
    print(testInv.removeItem(3))
