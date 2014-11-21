__author__ = 'Andrea'

class hero:
    
    def __init__(self):
        self.health = 100
        self.speed = 10
        self.mana = 100
        self.attack = 5
        self.defense = 3
        self.level = 1
        self.experience = 0
        self.XPneeded = 100

    def fight(self):
        pass

    def defend(self):
        pass

    def useMagic(self):
        pass

    def levelUp(self):
        pass
    
    def isDead(self):
        if self.health == 0:
            return True
        else:
            return False
