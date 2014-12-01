__author__ = 'Matt'

#a specific item of the inventory
class item():
    def __init__(self):
        self.name = ""
        self.description = ""
        self.price = 0
        self.value = 0
        self.sprite = ""

        #identifies how the item will interact

    def use(self):
        #uses item action based on i
        return self.value

    def sell(self):
        return self.price


    





