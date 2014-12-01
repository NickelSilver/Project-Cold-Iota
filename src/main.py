from OpenGL.GL import *
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import time
import random
import math
from PIL import Image #@UnresolvedImport
from menus.menuManager import *
from combat.monsterManager import *
from combat.hero import *


from mapLogic import *
from npcs.npcManager import *
from menus.pauseMenu import *

# NOTE: Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use ESCAPE = b"\033" where the b before the string converts it to bytes.

# Number of the glut window.
window = 0
holdingUp = False
holdingDown = False
holdingLeft = False
holdingRight = False
sway = False
moving = 0
movedVertical = vertOffset = -0.6 #aligns our avatar to the proper grid. Adjust as necessary.
movedHorizontal = 0
mapMovedVertical = 0.0
mapMovedHorizontal = 0.0
verticalPos = 0
horizontalPos = 0
facing = "down"
updateTime = 0
texture = ""
sceneMap = "map1"
npcList = ""
npcs = []
firstRun = True #For the first cycle, make sure everything updates properly.
npcCollider = False
showText = False
paused = False
hasNext = 0
currentLine = 0
selection = 0
maxSelection = 0
npcTimer = 0
npcSteps = 0
tutorial = True
combat = False
town = False
hasMonster = False
monster = None
combatAction = 0
protagonist = hero('Somnolous', 1)
battleTurn = 0 #0 for character turn, 1 for enemy turn
protagDefend = False
monDefend = False
npcFight =False


class Main():

    def monsterTurn(self, enemyMon):
        global protagonist, battleTurn, monDefend, protagDefend
        option = random.randint(0,2)
        if option==0:
            monDefend = True
            print('Monster defends')
        else:
            monDefend = False
            print('monster attacks')
            if protagDefend:
                protagonist.defend(enemyMon.attackHero())
            else:
                protagonist.loseHealth(enemyMon.attackHero())
        battleTurn-=1


    # A general OpenGL initialization function.  Sets all of the initial parameters.
    def InitGL(self, Width, Height):                # We call this right after our OpenGL window is created.
        glEnable(GL_TEXTURE_2D)
        glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
        glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
        glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                    # Reset The Projection Matrix
                                            # Calculate The Aspect Ratio Of The Window
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)            # Set The Blending Function For Translucency
        glEnable(GL_BLEND)                          # Enable Blending

    # The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
    def ReSizeGLScene(self, Width, Height):
        if Height == 0:                        # Prevent A Divide By Zero If The Window Is Too Small
            Height = 1

        glViewport(0, 0, Width, Height)        # Reset The Current Viewport And Perspective Transformation
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        #prevent window resizing
        Width = 640
        Height = 480
        glutReshapeWindow(Width, Height)

    #This animates our on-screen player character, or avatar.
    def updateAvatar(self):
        global moving, sway, facing, npcList, combat, town

        #If we've already got a movement animation, skip this function.
        if moving > 0:
            return 0

        #Switch the walking animation frames after every step.
        if sway and moving == 0:
            sway = False
        elif not sway and moving == 0:
            sway = True

        #Get our spritesheet and determine if our character is moving. If so, crop out the right image in the spritesheet and update texture 0
        #duration = int(500 - 25 * len(npcs) * 0.9)
        duration = int(200)
        image = Image.open("sprites/protagSpriteSheet1.png")
        if holdingUp:
            facing = "up"
            if moving == 0:
                moving = duration
            if sway and moving > 0:
                box = (0, 96, 32, 128)
                image = image.crop(box)
            elif not sway and moving > 0:
                box = (64, 96, 96, 128)
                image = image.crop(box)
        elif holdingDown:
            facing = "down"
            if moving == 0:
                moving = duration
            if sway and moving > 0:
                box = (0, 0, 32, 32)
                image = image.crop(box)
            elif not sway and moving > 0:
                box = (64, 0, 96, 32)
                image = image.crop(box)
        elif holdingLeft:
            facing = "left"
            if moving == 0:
                moving = duration
            if sway and moving > 0:
                box = (0, 32, 32, 64)
                image = image.crop(box)
            elif not sway and moving > 0:
                box = (64, 32, 96, 64)
                image = image.crop(box)
        elif holdingRight:
            facing = "right"
            if moving == 0:
                moving = duration
            if sway and moving > 0:
                box = (0, 64, 32, 96)
                image = image.crop(box)
            elif not sway and moving > 0:
                box = (64, 64, 96, 96)
                image = image.crop(box)

        if moving>0 and not town:
            dice = random.randrange(1, 100)
            if (dice%10 == 0):
                combat = True
                paused = True

        ix = image.size[0]
        iy = image.size[1]
        image = image.tostring("raw", "RGBA", 0, -1)
        # Create Texture
        glGenTextures(1, 0)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        if moving > 0: #If the avatar is moving, we don't need to get the still image.
            return 0;

        #If our avatar is not moving, find the right still animation, then update texture 0
        image = Image.open("sprites/protagSpriteSheet1.png")
        if facing == "up" and moving == 0:
            box = (32, 96, 64, 128)
            image = image.crop(box)
        elif facing == "down" and moving == 0:
            box = (32, 0, 64, 32)
            image = image.crop(box)
        elif facing == "left" and moving == 0:
            box = (32, 32, 64, 64)
            image = image.crop(box)
        elif facing == "right" and moving == 0:
            box = (32, 64, 64, 96)
            image = image.crop(box)

        ix = image.size[0]
        iy = image.size[1]
        image = image.tostring("raw", "RGBA", 0, -1)
        # Create Texture
        glGenTextures(1, 0)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def updateMap(self):
        global texture, sceneMap, parallaxMap

        doMapLogic(sceneMap, horizontalPos, verticalPos, facing) #find out if we need to change maps.

        if texture == sceneMap: #If our current texture matches the current sceneMap, there's no need to update it.
            return 0

        if sceneMap == "town1":
            image = Image.open("maps/town1.png")
            parallaxMap = Image.open("maps/town1parallax.bmp")
            
        elif sceneMap == "map1":
            image = Image.open("maps/map1.png")
            parallaxMap = Image.open("maps/map1parallax2.bmp")
        elif sceneMap == "pseudocampusmap":
            image = Image.open("maps/pseudocampusmap.png")
            parallaxMap = Image.open("maps/pseudocampusmapparallax.bmp")
        elif sceneMap == "fortesmap":
            image = Image.open("maps/fortesmap.png")
            parallaxMap = Image.open("maps/fortesmapparallax.bmp")

        texture = sceneMap

        ix = image.size[0]
        iy = image.size[1]

        image = image.tostring("raw", "RGBA", 0, -1)
        parallaxMap = parallaxMap.tostring("raw", "RGBX", 0, 1)

        glGenTextures(1, 1)
        glBindTexture(GL_TEXTURE_2D, 1)

        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        
    def bindMenuTextures(self):
        image = Image.open("menus/MainMenu2.png")

        ix = image.size[0]
        iy = image.size[1]

        image = image.tostring("raw", "RGBA", 0, -1)

        glGenTextures(1, 20) 
        glBindTexture(GL_TEXTURE_2D, 20) #start in the 20-block of texture ID's, just to keep things simple. 
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        image = Image.open("combat/battleback.png")

        ix = image.size[0]
        iy = image.size[1]

        image = image.tostring("raw", "RGBA", 0, -1)

        glGenTextures(1, 21) 
        glBindTexture(GL_TEXTURE_2D, 21)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        image = Image.open("monsters/batmonster1.png")

        ix = image.size[0]
        iy = image.size[1]

        image = image.tostring("raw", "RGBA", 0, -1)

        glGenTextures(1, 21) 
        glBindTexture(GL_TEXTURE_2D, 40) #begin in the unused 40-block
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        image = Image.open("monsters/chickenmonster1.png")

        ix = image.size[0]
        iy = image.size[1]

        image = image.tostring("raw", "RGBA", 0, -1)

        glGenTextures(1, 21) 
        glBindTexture(GL_TEXTURE_2D, 41)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        image = Image.open("monsters/ghostmonster1.png")

        ix = image.size[0]
        iy = image.size[1]

        image = image.tostring("raw", "RGBA", 0, -1)

        glGenTextures(1, 21) 
        glBindTexture(GL_TEXTURE_2D, 42)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        image = Image.open("monsters/spidermonster1.png")

        ix = image.size[0]
        iy = image.size[1]

        image = image.tostring("raw", "RGBA", 0, -1)

        glGenTextures(1, 21) 
        glBindTexture(GL_TEXTURE_2D, 43)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def updateNPCs(self):
        global npcList, sceneMap, npcs
        if npcList == sceneMap: #If our NPC's are already populating our map, we don't need to update them.
            return 0

        npcList = sceneMap
        createNPCList(sceneMap) #from npcManager class
        npcs = getNPCList()


    def update(self):
        #global firstRun,updateTime
        """
        elapsedTime = glutGet(GLUT_ELAPSED_TIME)
        if (elapsedTime - updateTime > 1000//30) or firstRun: #effectively the framerate. Adjust the denominator to adjust the FPS and the speeds of animation.
            updateTime = elapsedTime
        else:
            return 0
        firstRun = False
        """
        self.updateAvatar()
        self.updateMap()



    # The main drawing function.
    def DrawGLScene(self):
        global moving, movedVertical, movedHorizontal, mapMovedVertical, mapMovedHorizontal, sceneMap, parallaxMap, verticalPos, \
            horizontalPos, npcs, npcList, npcCollider, showText, firstRun,texture, hasNext, currentLine, selection, maxSelection, paused, \
            npcTimer, npcSteps, tutorial, combat, hasMonster, monster, combatAction, enemyDef, protagonist, battleTurn,\
            monDefend, protagDefend, npcFight
        npcTimer+=1
        if firstRun:
            self.update()
            firstRun = False
        # Clear The Screen And The Depth Buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()                    # Reset The View

        glBindTexture(GL_TEXTURE_2D, 1) #the ID of our map texture. We won't use it for a while. 

        colliderUp = parallaxMap[((1568*32*(verticalPos-2)*4 + 1568*16*4)+(32*(horizontalPos-1) + 16)*4+1)] #each tile is 32x32 pixels. This returns the value of "green" colour in each pixel.
        try: #This can throw an index out of bounds exception. Catch it and set the collider appropriately.
            colliderDown = parallaxMap[((1568*32*(verticalPos)*4 + 1568*16*4)+(32*(horizontalPos-1) + 16)*4+1)] #When the background is white, it is 255. When it is magenta, it is 0.
        except:
            colliderDown = 0
        colliderLeft = parallaxMap[((1568*32*(verticalPos-1)*4 + 1568*16*4)+(32*(horizontalPos-2) + 16)*4+1)]
        colliderRight = parallaxMap[((1568*32*(verticalPos-1)*4 + 1568*16*4)+(32*(horizontalPos) + 16)*4+1)]

        npcCollider = False
        facingNPC = None

        if not combat:
            for x in range(len(npcs)):
                if facing == "up":
                    #if npcs[x].getVertical() == verticalPos - 1 and npcs[x].getHorizontal() == horizontalPos:
                    if abs(npcs[x].getVertical() - (verticalPos - 1)) < 0.5 and abs(npcs[x].getHorizontal() - horizontalPos) < 0.5:
                        npcCollider = True
                        facingNPC = npcs[x]
                        facingNPC.moving = 0
                elif facing == "down":
                    #if npcs[x].getVertical() == verticalPos + 1 and npcs[x].getHorizontal() == horizontalPos:
                    if abs(npcs[x].getVertical() - (verticalPos + 1)) < 0.5 and abs(npcs[x].getHorizontal() - horizontalPos) < 0.5:
                        npcCollider = True
                        facingNPC = npcs[x]
                        facingNPC.moving = 0
                elif facing == "left":
                    #if npcs[x].getVertical() == verticalPos and npcs[x].getHorizontal() == horizontalPos - 1:
                    if abs(npcs[x].getVertical() - verticalPos) < 0.5 and abs(npcs[x].getHorizontal() - (horizontalPos - 1)) < 0.5:
                        npcCollider = True
                        facingNPC = npcs[x]
                        facingNPC.moving = 0
                elif facing == "right":
                    #if npcs[x].getVertical() == verticalPos and npcs[x].getHorizontal() == horizontalPos + 1:
                    if abs(npcs[x].getVertical() - verticalPos) < 0.5 and abs(npcs[x].getHorizontal() - (horizontalPos + 1)) < 0.5:
                        npcCollider = True
                        facingNPC = npcs[x]
                        facingNPC.moving = 0

        if moving > 0:
            #offset = 2.0/(500.0 - 25.0*len(npcs)*0.9)
            offset = 2.0/200.0
            if facing == "up":
                if colliderUp != 0 and verticalPos > 2 and not npcCollider:
                    mapMovedVertical -= offset
                    movedVertical -= offset
            elif facing == "down":
                if colliderDown != 0 and verticalPos < 29 and not npcCollider:
                    movedVertical += offset
                    mapMovedVertical += offset
            elif facing == "left":
                if colliderLeft != 0 and horizontalPos > 1 and not npcCollider:
                    movedHorizontal += offset
                    mapMovedHorizontal += offset
            elif facing == "right":
                if colliderRight != 0 and horizontalPos < 49 and not npcCollider:
                    movedHorizontal -= offset
                    mapMovedHorizontal -= offset
            moving -= 1
        else:
            verticalPos = int(movedVertical/2 + 15.5) #one tile = 2 units, and we start smack-dab at 0,0, so to get the actual tile entity in a way that makes sense, compensate.
            horizontalPos = int(-movedHorizontal/2 + 25.5) #Now our map tiles begin at 1,1 and end at 50,30 for a total of 49x29, each tile representing 32 pixels of image.

        if movedVertical >= 15:
            mapMovedVertical = 15 - vertOffset
        if movedVertical <= -16:
            mapMovedVertical = -16 - vertOffset
        if movedHorizontal >= 31:
            mapMovedHorizontal = 31
        if movedHorizontal <= -31:
            mapMovedHorizontal = -31
        glTranslatef(mapMovedHorizontal, mapMovedVertical, -32.1) #We actually move the entire map.

        glBegin(GL_QUADS) #Start drawing the polygon that will represent our map. In our case, one tile = 2 units. Oops. Derp. Well, too late to change it now. Strike the Earth!
        glTexCoord2f(0.0,1.0)
        glVertex3f(-49.0, 29.0, 0.0)
        glTexCoord2f(1.0,1.0)
        glVertex3f( 49.0, 29.0, 0.0)
        glTexCoord2f(1.0,0.0)
        glVertex3f( 49.0,-29.0, 0.0)
        glTexCoord2f(0.0,0.0)
        glVertex3f(-49.0,-29.0, 0.0)
        glEnd() #Stop drawing the map

        glBindTexture(GL_TEXTURE_2D, 0)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
        glTranslatef(-movedHorizontal, -movedVertical, 0.1) #Invert our motion for the character, so if the player moves left, the map moves right and the player keeps up with the "camera"


        # Draw a square (quadrilateral)
        glBegin(GL_QUADS)                   # This represents our avatar character guy. The controllable one. 
        glTexCoord2f(0.0,1.0)
        glVertex3f(-1.0, 1.0, 0.0)          # Top Left
        glTexCoord2f(1.0,1.0)
        glVertex3f(1.0, 1.0, 0.0)           # Top Right
        glTexCoord2f(1.0,0.0)
        glVertex3f(1.0, -1.0, 0.0)          # Bottom Right
        glTexCoord2f(0.0,0.0)
        glVertex3f(-1.0, -1.0, 0.0)         # Bottom Left
        glEnd()                             # We are done with the polygon


        self.updateNPCs() #Now the real fun begins. For each and every NPC, draw a new quad and update the texture appropriately.

        transmatrixX = []
        transmatrixY=[]


        for x in range(len(npcs)):
            
            horizontal = int(npcs[x].getHorizontal())
            vertical = int(npcs[x].getVertical())
            colliderUpNPC = parallaxMap[((1568*32*(vertical-2)*4 + 1568*16*4)+(32*(horizontal-1) + 16)*4+1)] #each tile is 32x32 pixels. 
            #This returns the value of "green" colour in each pixel.
            try: #This can throw an index out of bounds exception. Catch it and set the collider appropriately.
                colliderDownNPC = parallaxMap[((1568*32*(vertical)*4 + 1568*16*4)+(32*(horizontal-1) + 16)*4+1)]
                
            #When the background is white, it is 255. When it is magenta, it is 0.
            except:
                colliderDownNPC = 0
            colliderLeftNPC = parallaxMap[((1568*32*(vertical-1)*4 + 1568*16*4)+(32*(horizontal-2) + 16)*4+1)]
           
            colliderRightNPC = parallaxMap[((1568*32*(vertical-1)*4 + 1568*16*4)+(32*(horizontal) + 16)*4+1)]
            #for ease of use, NPC coords are given using practical coords. Convert them to the OpenGL coords of our scene.
            
            transmatrixX.append((npcs[x].getHorizontal()-25)*2 + mapMovedHorizontal)
            transmatrixY.append((-npcs[x].getVertical()+15)*2 - vertOffset + mapMovedVertical)
            if npcCollider:
                facingNPC.turnTowardPlayer(facing)
                facingNPC.moving = 0


            if not paused and not combat:
                if x%6==0 and npcTimer%10==0: #adjusted the speed and number of NPCs that move. 
                    #offset = 2.0/(500.0 - 25.0*len(npcs)*0.9)
                    if npcs[x].moving > 0:
                        npcSteps+=1
                        offset = 2.0/200.0 #I CHANGE HERE JUST TO SEE THE NPC WALKING FAST SO I COULD EASILY SEE IF THEY WERE HITTING THE WALLS
                        #Changed to align them to grid
                        if npcs[x].facing == "up":
                            if colliderUpNPC != 0 and npcs[x].verticalPos > 2 :
                                npcs[x].verticalPos -= 2*offset
                                npcs[x].flagForUpdate(True)
                            elif colliderUpNPC==0:
                                npcs[x].facing = 'down'
                        elif npcs[x].facing == "down":
                            if colliderDownNPC != 0 and npcs[x].verticalPos < 29 :
                                npcs[x].verticalPos += 2*offset
                                npcs[x].flagForUpdate(True)
                            elif colliderDownNPC==0:
                                npcs[x].facing = 'up'

                        elif npcs[x].facing == "left":
                            if colliderLeftNPC != 0 and npcs[x].horizontalPos > 1 :
                                npcs[x].horizontalPos -= 2*offset
                                npcs[x].flagForUpdate(True)
                        elif npcs[x].facing == "right":
                            if colliderRightNPC != 0 and npcs[x].horizontalPos < 49 :
                                npcs[x].horizontalPos += 2*offset
                                npcs[x].flagForUpdate(True)

                        npcs[x].moving -= 10 #changed to align them to grid. 
                    elif moving==0:
                        direction = random.randrange(1, 5)
                        if direction == 1:
                            npcs[x].moveRight()
                        elif direction == 2:
                            npcs[x].moveLeft()
                        elif direction == 3:
                            npcs[x].moveDown()
                        elif direction == 4 :
                            npcs[x].moveUp()
                        

            if npcs[x].getFlagForUpdate(): #Update the textures for each NPC.
                image = Image.open(npcs[x].getSprite())
                box = npcs[x].updateSprite()
                image = image.crop(box)
                ix = image.size[0]
                iy = image.size[1]
                image = image.tostring("raw", "RGBA", 0, -1)
                glGenTextures(1, 0)
                glBindTexture(GL_TEXTURE_2D, x+2)
                glPixelStorei(GL_UNPACK_ALIGNMENT,1)
                glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                npcs[x].flagForUpdate(False)


        for x in range(len(transmatrixX)): #Draw the NPC's quad objects and apply their textures.
            glLoadIdentity()
            glTranslatef(transmatrixX[x], transmatrixY[x], -32)

            glBindTexture(GL_TEXTURE_2D, x+2)

            glBegin(GL_QUADS)
            glTexCoord2f(0.0,1.0)
            glVertex3f(-1.0, 1.0, 0.0)          # Top Left
            glTexCoord2f(1.0,1.0)
            glVertex3f(1.0, 1.0, 0.0)           # Top Right
            glTexCoord2f(1.0,0.0)
            glVertex3f(1.0, -1.0, 0.0)          # Bottom Right
            glTexCoord2f(0.0,0.0)
            glVertex3f(-1.0, -1.0, 0.0)         # Bottom Left
            glEnd()

        if paused and not combat:
            glLoadIdentity()
            glTranslatef(mapMovedHorizontal, mapMovedVertical, -32.1)
            glTranslatef(-movedHorizontal, -movedVertical, 0.1)
            glTranslatef(movedHorizontal - mapMovedHorizontal, movedVertical - mapMovedVertical, 0.1)
            
            maxSelection = 3
            x = 18
            y = 14
            glColor3f(1.0,1.0,1.0)
            glBindTexture(GL_TEXTURE_2D, 20)
            glBegin(GL_QUADS)               #draw menu box
            glTexCoord2f(0.0,1.0)
            glVertex3f(-x, y, 0.0)          # Top Left
            glTexCoord2f(1.0,1.0)
            glVertex3f(x, y, 0.0)           # Top Right
            glTexCoord2f(1.0,0.0)
            glVertex3f(x, -y, 0.0)          # Bottom Right
            glTexCoord2f(0.0,0.0)
            glVertex3f(-x, -y, 0.0)         # Bottom Left
            glEnd()
            
            glTranslatef(0, 2.5, 0.1)
            
            x = 18
            y = 1.5
            glTranslatef(0, -3.15*selection, 0.0)
            
            glColor4f(0.0,0.5,1.0,0.33)
            glBindTexture(GL_TEXTURE_2D, 100)
            glBegin(GL_QUADS)               #draw menu box
            glTexCoord2f(0.0,1.0)
            glVertex3f(-x, y, 0.0)          # Top Left
            glTexCoord2f(1.0,1.0)
            glVertex3f(x, y, 0.0)           # Top Right
            glTexCoord2f(1.0,0.0)
            glVertex3f(x, -y, 0.0)          # Bottom Right
            glTexCoord2f(0.0,0.0)
            glVertex3f(-x, -y, 0.0)         # Bottom Left
            glEnd()
            
            
            glColor4f(1.0,1.0,1.0,1.0)
            
        if combat:

            glLoadIdentity()
            glTranslatef(mapMovedHorizontal, mapMovedVertical, -32.1)
            glTranslatef(-movedHorizontal, -movedVertical, 0.1)
            glTranslatef(movedHorizontal - mapMovedHorizontal, movedVertical - mapMovedVertical, 0.1)
            
            if not hasMonster:
                createMonsterPool(sceneMap)
                if npcFight:
                    npcFight = False
                    monsters = getNpcMonsterPool()
                    monster = monsters[0]
                else:
                    monsters = getMonsterPool()
                    num = random.randint(0,len(monsters)-1)
                    monster = monsters[num]
                levelMax = getLevelCap()
                minLevel = getLevelMin()
                monster.setLevel(random.randint(minLevel, levelMax))
                selection = 0
                hasMonster = True
                paused = True
                print(str(monster.name)+' level ' +str(monster.level)+' appeared')

            #print ("The combat should be implemented here.",monster.name,monster.level)
            x = 18
            y = 14
            
            glColor3f(1.0,1.0,1.0)
            glBindTexture(GL_TEXTURE_2D, 21)
            glBegin(GL_QUADS)               #draw menu box
            glTexCoord2f(0.0,1.0)
            glVertex3f(-x, y, 0.0)          # Top Left
            glTexCoord2f(1.0,1.0)
            glVertex3f(x, y, 0.0)           # Top Right
            glTexCoord2f(1.0,0.0)
            glVertex3f(x, -y, 0.0)          # Bottom Right
            glTexCoord2f(0.0,0.0)
            glVertex3f(-x, -y, 0.0)         # Bottom Left
            glEnd()
            
            x = 9
            y = 7
            glTranslatef(0, 2.5, 0.1)
            if monster.name == "Spidronus":
                glBindTexture(GL_TEXTURE_2D, 43)
            elif monster.name == "Pickles":
                glBindTexture(GL_TEXTURE_2D, 41)
            elif monster.name == "Drule":
                glBindTexture(GL_TEXTURE_2D, 40)
            else:
                glBindTexture(GL_TEXTURE_2D, 42)
            glBegin(GL_QUADS)               #draw menu box
            glTexCoord2f(0.0,1.0)
            glVertex3f(-x, y, 0.0)          # Top Left
            glTexCoord2f(1.0,1.0)
            glVertex3f(x, y, 0.0)           # Top Right
            glTexCoord2f(1.0,0.0)
            glVertex3f(x, -y, 0.0)          # Bottom Right
            glTexCoord2f(0.0,0.0)
            glVertex3f(-x, -y, 0.0)         # Bottom Left
            glEnd()
            
            x = 4
            y = 3
            glTranslatef(-12,-11.5,0.1)
            
            glBindTexture(GL_TEXTURE_2D, 100) #bind to some arbitrarily huge texture that's not likely to be bound to anything, thus producing a white rectangle. 
            
            glColor4f(1.0,1.0,1.0,0.33)
            glBegin(GL_QUADS) #draw textbox
            glVertex3f(-x, y, 0.0)          # Top Left
            glVertex3f(x, y, 0.0)           # Top Right
            glVertex3f(x, -y, 0.0)          # Bottom Right
            glVertex3f(-x, -y, 0.0)         # Bottom Left
            glEnd()
            
            y = 4
            
            glColor3f(0.0,0.0,0.0)
            renderText = "Attack"
            renderText = bytes(renderText, "ascii")
            self.renderString(-x - 15, -y - 1, -31.8, GLUT_BITMAP_HELVETICA_18, renderText)
            
            renderText = "Defend"
            renderText = bytes(renderText, "ascii")
            self.renderString(-x - 15, -y - 4, -31.8, GLUT_BITMAP_HELVETICA_18, renderText)
            
            renderText = "Magic"
            renderText = bytes(renderText, "ascii")
            self.renderString(-x - 15, -y - 7, -31.8, GLUT_BITMAP_HELVETICA_18, renderText)
            
            renderText = "Run"
            renderText = bytes(renderText, "ascii")
            self.renderString(-x - 15, -y - 10, -31.8, GLUT_BITMAP_HELVETICA_18, renderText)
            
            maxSelection = 3
            
            glTranslatef(0, 2.25, 0.0)
            glTranslatef(0, -1.5*selection, 0.0)
            
            y = 0.75
            
            glColor4f(0.0,0.5,1.0,0.33)
            glBindTexture(GL_TEXTURE_2D, 100)
            glBegin(GL_QUADS)               #draw menu box
            glTexCoord2f(0.0,1.0)
            glVertex3f(-x, y, 0.0)          # Top Left
            glTexCoord2f(1.0,1.0)
            glVertex3f(x, y, 0.0)           # Top Right
            glTexCoord2f(1.0,0.0)
            glVertex3f(x, -y, 0.0)          # Bottom Right
            glTexCoord2f(0.0,0.0)
            glVertex3f(-x, -y, 0.0)         # Bottom Left
            glEnd()
            
            glColor3f(1.0,1.0,1.0)

            if battleTurn==0:
                if combatAction==1:
                    print('You attack')
                    combatAction = 0
                    protagDefend = False
                    if monDefend:
                        monster.defend(protagonist.attackMonster())
                    else:
                        monster.loseHealth(protagonist.attackMonster())
                        print('enemy health: '+str(monster.currentHealth)+'\nYour health: ' +str(protagonist.currentHealth))
                    battleTurn+=1
                elif combatAction==2:
                    print('You defend')
                    protagDefend = True
                    combatAction = 0
                    battleTurn+=1
                elif combatAction==3:
                    print('You healed')
                    protagonist.heal()
                    protagDefend = False
                    combatAction = 0
                    print('enemy health: '+str(monster.currentHealth)+'\nYour health: ' +str(protagonist.currentHealth))
                    battleTurn+=1

            else:
                self.monsterTurn(monster)
                print('enemy health: '+str(monster.currentHealth)+'\nYour health: ' +str(protagonist.currentHealth))

            if monster.isDead() or protagonist.isDead() or combatAction == 4:
                combat = False
                hasMonster = False
                paused = False
                combatAction = 0
                battleTurn = 0
                if protagonist.isDead():
                    print("Game over, start the game again and reload")
                    sys.exit(0)
                elif monster.isDead():
                    print('you gained '+str(monster.getExperience())+' xp')
                    protagonist.gainExperience(monster.getExperience())

        #Relocated to fix NPCs rendering on top of text boxes. 
        if showText:
            x = 18.0
            y = 2.0
            glLoadIdentity()
            glTranslatef(mapMovedHorizontal, mapMovedVertical, -32.1)
            glTranslatef(-movedHorizontal, -movedVertical, 0.1)
            glTranslatef(movedHorizontal - mapMovedHorizontal, movedVertical - mapMovedVertical - 12, 0.1)

            glBindTexture(GL_TEXTURE_2D, 100) #bind to some arbitrarily huge texture that's not likely to be bound to anything, thus producing a white rectangle. 

            glBegin(GL_QUADS) #draw textbox
            glVertex3f(-x, y, 0.0)          # Top Left
            glVertex3f(x, y, 0.0)           # Top Right
            glVertex3f(x, -y, 0.0)          # Bottom Right
            glVertex3f(-x, -y, 0.0)         # Bottom Left
            glEnd()
            
            renderText = ""
            npcText = ""

            x = 5
            glColor3f(0.0,0.0,0.0)
            if tutorial:
                npcText = ["Press WASD to move around the world.","Press Enter to interact with people and objects.","Null"]
            else:
                try:
                    if combat:
                        npcText =  ["Let's fight!", "Now!"]
                    else:
                        npcText = facingNPC.getText()
                except:
                    pass
                
            if currentLine < len(npcText) and currentLine >= 0:
                renderText = npcText[currentLine]
                currentLine += 1
            else:
                renderText = ""
            renderText = bytes(renderText, "ascii")
            self.renderString(movedHorizontal - movedHorizontal - 34, movedVertical - movedVertical - 10, -31.8, GLUT_BITMAP_HELVETICA_18, renderText)
            
            if currentLine < len(npcText) and currentLine >= 0:
                renderText = npcText[currentLine]
                currentLine += 1
            else:
                renderText = ""
            renderText = bytes(renderText, "ascii")
            self.renderString(movedHorizontal - movedHorizontal - 34, movedVertical - movedVertical - 13, -31.8, GLUT_BITMAP_HELVETICA_18, renderText)
                
            if currentLine >= len(npcText):
                hasNext = False
                if tutorial:
                    tutorial = False
                    showText = False
            else:
                hasNext = True
            if len(npcText) > 0:
                currentLine -= 2
            glColor3f(1.0,1.0,1.0)
        else:
            currentLine = 0
            hasNext = 0
            
        if tutorial:
            showText = True
            

        #  since this is double buffered, swap the buffers to display what just got drawn.
        glutSwapBuffers()

    def renderString(self, x, y, z, font, characters):
        glRasterPos3f(x, y,z)
        for c in characters:
            glutBitmapCharacter(font, c)

    # The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
    def keyPressed(self, *args):
        global holdingLeft, holdingRight, holdingUp, holdingDown, showText,paused, hasNext, currentLine, selection, maxSelection, \
        movedVertical, vertOffset, movedHorizontal, mapMovedVertical, mapMovedHorizontal, verticalPos, horizontalPos, facing, \
        sceneMap, npcList, npcs, combat, combatAction, battleTurn, protagonist, npcFight
        if args[0] == b"\033" and not showText and not combat: # If escape is pressed, bring up the pause menu.
            if not paused:
                paused = True
            else:
                paused = False

        elif (args[0] == b'w' or args[0] == b'W') and not showText and not paused:
            holdingUp = True
        elif (args[0] == b'a' or args[0] == b'A') and not showText and not paused:
            holdingLeft = True
        elif (args[0] == b's' or args[0] == b'S') and not showText and not paused:
            holdingDown = True
        elif (args[0] == b'd' or args[0] == b'D') and not showText and not paused:
            holdingRight = True
        elif (args[0] == b'w' or args[0] == b'W') and paused:
            if selection > 0:
                selection -= 1
        elif (args[0] == b's' or args[0] == b'S') and paused:
            if selection < maxSelection:
                selection += 1
        elif args[0] == b'\015' and npcCollider and not showText and not paused:
            dice = random.randrange(1, 100)
            if (dice%5 == 0):
                combat = True
                npcFight =True
                paused = True
            showText = True
        elif args[0] == b'\015' and showText and not hasNext:
            showText = False
            #combat = False
            if not combat:
                paused = False       
        elif args[0] == b'\015' and showText and hasNext:
            currentLine += 2
        elif args[0] == b'\015' and paused and not combat:
            if selection == 0: #save
                saveobject = [movedVertical,vertOffset, movedHorizontal,mapMovedVertical, mapMovedHorizontal,verticalPos,
                    horizontalPos, facing, sceneMap,npcList, npcs,protagonist]
                PauseMenu.saveGame(self,saveobject)
                paused = False
            elif selection == 1: #load
                loadList = PauseMenu.loadGame(self)
                movedVertical,vertOffset, movedHorizontal,mapMovedVertical, mapMovedHorizontal,verticalPos,\
                horizontalPos, facing, sceneMap,npcList, npcs, protagonist = loadList
                paused = False
            elif selection == 2: #settings
                pass
            elif selection == 3: #exit
                sys.exit(0)
            pass #placeholder for menu selection
        elif args[0] == b'\015' and combat:
            combatAction = selection + 1


    def keyReleased(self, *args):
        global holdingLeft, holdingRight, holdingUp, holdingDown
        if args[0] == b'w' or args[0] == b'W':
            holdingUp = False
        elif args[0] == b'a' or args[0] == b'A':
            holdingLeft = False
        elif args[0] == b's' or args[0] == b'S':
            holdingDown = False
        elif args[0] == b'd' or args[0] == b'D':
            holdingRight = False


    def main(self):
        global window
        # For now we just pass glutInit one empty argument. I wasn't sure what should or could be passed in (tuple, list, ...)
        # Once I find out the right stuff based on reading the PyOpenGL source, I'll address this.
        glutInit(sys.argv)
        glutInitContextVersion( 2, 1 )

        # Select type of Display mode:
        #  Double buffer
        #  RGBA color
        # Alpha components supported
        # Depth buffer
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

        # get a 640 x 480 window
        glutInitWindowSize(640, 480)

        # the window starts at the upper left corner of the screen
        glutInitWindowPosition(0, 0)

        # Okay, like the C version we retain the window id to use when closing, but for those of you new
        # to Python (like myself), remember this assignment would make the variable local and not global
        # if it weren't for the global declaration at the start of main.
        window = glutCreateWindow(b"Project Cold Iota")

        # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
        # set the function pointer and invoke a function to actually register the callback, otherwise it
        # would be very much like the C version of the code.
        glutDisplayFunc(self.DrawGLScene)

        # Uncomment this line to get full screen.
        #glutFullScreen()

        # When we are doing nothing, redraw the scene.

        # Register the function called when our window is resized.
        glutReshapeFunc(self.ReSizeGLScene)

        # Register the function called when the keyboard is pressed.
        glutKeyboardFunc(self.keyPressed)
        glutKeyboardUpFunc(self.keyReleased)

        # Initialize our window.
        self.InitGL(640, 480)
        self.bindMenuTextures()

        glutTimerFunc(int(1000.0 / 60.0), self.mainLoop, 0)

        #make mini Menu
        self.makeMiniMenu()
        # Start Event Processing Engine
        glutMainLoop()


    def makeMiniMenu(self):
        global movedVertical,vertOffset, movedHorizontal,mapMovedVertical, mapMovedHorizontal,verticalPos,\
            horizontalPos, facing, sceneMap,npcList, npcs, protagonist

        VOID, SAVE, LOAD, QUIT = list(range(4))
        #testing glut menu
        createMenus()
        def doquit():
            sys.exit(0)

        option1 = menuList[1].saveGame
        option2 = menuList[1].loadGame
        menudict = {SAVE: option1,
                    LOAD:option2,
                    QUIT: doquit}


        def dmenu(item):
            global movedVertical,vertOffset, movedHorizontal,mapMovedVertical, mapMovedHorizontal,verticalPos,\
            horizontalPos, facing, sceneMap,npcList, npcs,protagonist
            if item == SAVE:
                saveobject = [movedVertical,vertOffset, movedHorizontal,mapMovedVertical, mapMovedHorizontal,verticalPos,
                    horizontalPos, facing, sceneMap,npcList, npcs, protagonist]
                menudict[item](saveobject)
            elif item == LOAD:
                loadList = menuList[1].loadGame()
                movedVertical,vertOffset, movedHorizontal,mapMovedVertical, mapMovedHorizontal,verticalPos,\
            horizontalPos, facing, sceneMap,npcList, npcs, protagonist = loadList
            else:
                menudict[item]()
            return 0
        glutCreateMenu(dmenu)
        glutAddMenuEntry("save", SAVE)
        glutAddMenuEntry("load", LOAD)
        glutAddMenuEntry("Quit", QUIT)
        glutAttachMenu(GLUT_RIGHT_BUTTON)

    def mainLoop(self, val):
        self.update()
        self.DrawGLScene()
        glutTimerFunc(int(1000.0 / 60.0), self.mainLoop, val)





#And here we go...fingers crossed.
Main().main()