__author__ = 'Andrea'

class Cursor:
    def __init__(self, xpos=0, ypos=0, width = 5,height  = 10, jump=5, image = None):
        self.x = xpos
        self.y = ypos
        self.width = width
        self.height = height
        self.jump = jump
        self.count = 0
        self.image = image

    def moveUp(self):
        self.count-=1
        if self.count>0:
            self.y +=self.jump

    def moveDown(self):
        self.y-=self.jump
        self.count+=1

    def setPos(self, xpos, ypos):
        self.x = xpos
        self.y = ypos

    def getPos(self):
        return (self.x,self.y)

    def setJump(self, jump):
        self.jump = jump

    def getJump(self):
        return self.jump

    def setImage(self, image):
        self.image = image

    def getImgae(self):
        return self.image

    def getCount(self):
        return self.count

    def setCount(self, num):
        self.count = num