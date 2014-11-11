'''
Created on 21 Oct 2014

@author: Nickel
'''

from PIL import Image


    
class npc:
    global facing, horizontalPos, verticalPos, mapID, sprite
    def __init__(self, mapish, h, v, direction, spritesheet):
        self.mapID = mapish
        self.facing = direction
        self.horizontalPos = h
        self.verticalPos = v
        self.sprite = spritesheet
        self.text = []
        self.updateFlag = True
        self.moving = 0
        self.holdingDown = False
        self.holdingUp = False
        self.holdingLeft = False
        self.holdingRight = False
        self.sway = False
        self.responses = [None] * 3
        self.initResponse() #method to store responses.
       
    def setText(self, line):
        self.text.append(line)
        
    def getText(self):
        return self.text
    
    def turnTowardPlayer(self, pfacing):
        temp = self.facing
        if pfacing == "up":
            self.facing = "down"
        elif pfacing == "down":
            self.facing = "up"
        elif pfacing == "left":
            self.facing = "right"
        elif pfacing == "right":
            self.facing = "left"
        if self.facing != temp:
            self.updateFlag = True
    
    def turnUp(self):
        self.facing = "up"
        self.updateSprite()
    
    def turnDown(self):
        self.facing = "down"
        self.updateSprite()
    
    def turnLeft(self):
        self.facing = "left"
        self.updateSprite()
    
    def turnRight(self):
        self.facing = "right"
        self.updateSprite()
    
    def moveUp(self):
        self.holdingUp = True
        self.updateSprite()
    
    def moveDown(self):
        self.holdingDown = True
        self.updateSprite()
    
    def moveLeft(self):
        self.holdingLeft = True
        self.updateSprite()
    
    def moveRight(self):
        self.holdingRight = True
        self.updateSprite()
    
    def getHorizontal(self):
        return self.horizontalPos
    
    def getVertical(self):
        return self.verticalPos
    
    def getFlagForUpdate(self):
        return self.updateFlag
    
    def flagForUpdate(self, tf):
        self.updateFlag = tf
        
    def getSprite(self):
        return self.sprite
    
    def updateSprite(self):
        #If we've already got a movement animation, skip this function.
        if self.moving > 0:
            return self.box

        #Switch the walking animation frames after every step.
        if self.sway and self.moving == 0:
            self.sway = False
        elif not self.sway and self.moving == 0:
            self.sway = True

        if self.holdingUp:
            self.facing = "up"
            if self.moving == 0:
                self.moving = 500
            if self.sway and self.moving > 0:
                self.box = (0, 96, 32, 128)
                self.sway = False
            elif not self.sway and self.moving > 0:
                self.box = (64, 96, 96, 128)
                self.sway = True
            self.holdingUp = False #Reset. In other words, every time self.moveUp() is called, move up exactly one tile.
            return self.box
        elif self.holdingDown:
            self.facing = "down"
            if self.moving == 0:
                self.moving = 500
            if self.sway and self.moving > 0:
                self.box = (0, 0, 32, 32)
                self.sway = False
            elif not self.sway and self.moving > 0:
                self.box = (64, 0, 96, 32)
                self.sway = True
            self.holdingDown = False
            return self.box
        elif self.holdingLeft:
            self.facing = "left"
            if self.moving == 0:
                self.moving = 500
            if self.sway and self.moving > 0:
                self.box = (0, 32, 32, 64)
                self.sway = False
            elif not self.sway and self.moving > 0:
                self.box = (64, 32, 96, 64)
                self.sway = True
            self.holdingLeft = False
            return self.box
        elif self.holdingRight:
            self.facing = "right"
            if self.moving == 0:
                self.moving = 500
            if self.sway and self.moving > 0:
                self.box = (0, 64, 32, 96)
                self.sway = False
            elif not self.sway and self.moving > 0:
                self.box = (64, 64, 96, 96)
                self.sway = True
            self.holdingRight = False
            return self.box

        if self.moving > 0: #If the avatar is moving, we don't need to get the still image.
            return self.box;

        #If our avatar is not moving, find the right still animation, then update texture 0
        if self.facing == "up" and self.moving == 0:
            self.box = (32, 96, 64, 128)
        elif self.facing == "down" and self.moving == 0:
            self.box = (32, 0, 64, 32)
        elif self.facing == "left" and self.moving == 0:
            self.box = (32, 32, 64, 64)
        elif self.facing == "right" and self.moving == 0:
            self.box = (32, 64, 64, 96)
        
        return self.box
        
    def initResponse(self):
        if self.sprite == "sprites/goatBoySpriteSheet1.png":
            self.responses[0] = ("Here we goat again...")
            self.responses[1] = ("Hey, goat any grass?")
            self.responses[2] = ("Whatever goats your boat.")
        elif self.sprite == "sprites/emoSpriteSheet.png":
            self.responses[0] = ("meh...")
            self.responses[1] = ("I wish I was a flower.")
            self.responses[2] = ("Good day.")
        elif self.sprite == "sprites/holstaurusSpriteSheet.png":
            self.responses[0] = ("")
            self.responses[1] = ("")
            self.responses[2] = ("")
        elif self.sprite == "sprites/horsinAroundSpriteSheet1.png":
            self.responses[0] = ("I'm horsin' around.")
            self.responses[1] = ("Neigh-sayers all around.")
            self.responses[2] = ("Don't bale on me!")
        elif self.sprite == "sprites/monkeyBusinessSpriteSheet1.png":
            self.responses[0] = ("Selling bananas is harder than it looks.")
            self.responses[1] = ("It's hard to keep a good suite clean.")
            self.responses[2] = ("I used to be a banker but I lost interest.")
        elif self.sprite == "sprites/mrPiddlesSpriteSheet1.png":
            self.responses[0] = ("Mr piddles requests your assistance.")
            self.responses[1] = ("You've got to be kitten me.")
            self.responses[2] = ("Looking forward to Caturday.")
        elif self.sprite == "sprites/profChowdaSpriteSheet1.png":
            self.responses[0] = ("")
            self.responses[1] = ("")
            self.responses[2] = ("")
        elif self.sprite == "sprites/npc1SpriteSheet1.png":
            ""
    
    def getResponse(self):
        from random import randrange
        response = randrange(3)
        return self.responses[response]
    
    
        
        
        
        
        