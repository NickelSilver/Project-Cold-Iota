from OpenGL.GL import *
OpenGL.ERROR_CHECKING = False
OpenGL.ERROR_LOGGING = False
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from PIL import Image #@UnresolvedImport


from mapLogic import *
from npcManager import *

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
sceneMap = "town1"
npcList = ""
npcs = []
firstRun = True #For the first cycle, make sure everything updates properly. 

class Main():

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
        global moving, sway, facing

        #If we've already got a movement animation, skip this function.
        if moving > 0:
            return 0

        #Switch the walking animation frames after every step.
        if sway and moving == 0:
            sway = False
        elif not sway and moving == 0:
            sway = True

        #Get our spritesheet and determine if our character is moving. If so, crop out the right image in the spritesheet and update texture 0
        image = Image.open("sprites/protagSpriteSheet1.png")
        if holdingUp:
            facing = "up"
            if moving == 0:
                moving = 500
            if sway and moving > 0:
                box = (0, 96, 32, 128)
                image = image.crop(box)
            elif not sway and moving > 0:
                box = (64, 96, 96, 128)
                image = image.crop(box)
        elif holdingDown:
            facing = "down"
            if moving == 0:
                moving = 500
            if sway and moving > 0:
                box = (0, 0, 32, 32)
                image = image.crop(box)
            elif not sway and moving > 0:
                box = (64, 0, 96, 32)
                image = image.crop(box)
        elif holdingLeft:
            facing = "left"
            if moving == 0:
                moving = 500
            if sway and moving > 0:
                box = (0, 32, 32, 64)
                image = image.crop(box)
            elif not sway and moving > 0:
                box = (64, 32, 96, 64)
                image = image.crop(box)
        elif holdingRight:
            facing = "right"
            if moving == 0:
                moving = 500
            if sway and moving > 0:
                box = (0, 64, 32, 96)
                image = image.crop(box)
            elif not sway and moving > 0:
                box = (64, 64, 96, 96)
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
        
    def updateNPCs(self):
        global npcList, sceneMap, npcs
        if npcList == sceneMap: #If our NPC's are already populating our map, we don't need to update them. 
            return 0
        
        npcList = sceneMap
        createNPCList(sceneMap) #from npcManager class
        npcs = getNPCList()
        

    def update(self):
        global updateTime, firstRun

        elapsedTime = glutGet(GLUT_ELAPSED_TIME)
        if (elapsedTime - updateTime > 1000//30) or firstRun: #effectively the framerate. Adjust the denominator to adjust the FPS and the speeds of animation.
            updateTime = elapsedTime
        else:
            return 0
        
        firstRun = False

        self.updateAvatar()
        self.updateMap()


    # The main drawing function.
    def DrawGLScene(self):
        global moving, movedVertical, movedHorizontal, mapMovedVertical, mapMovedHorizontal, sceneMap, parallaxMap, verticalPos, horizontalPos, npcs
        self.update()
        # Clear The Screen And The Depth Buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()                    # Reset The View

        glBindTexture(GL_TEXTURE_2D, 1)
        
        colliderUp = parallaxMap[((1568*32*(verticalPos-2)*4 + 1568*16*4)+(32*(horizontalPos-1) + 16)*4+1)] #each tile is 32x32 pixels. This returns the value of "green" colour in each pixel. 
        try: #This can throw an index out of bounds exception. Catch it and set the collider appropriately. 
            colliderDown = parallaxMap[((1568*32*(verticalPos)*4 + 1568*16*4)+(32*(horizontalPos-1) + 16)*4+1)] #When the background is white, it is 255. When it is magenta, it is 0.
        except:
            colliderDown = 0
        colliderLeft = parallaxMap[((1568*32*(verticalPos-1)*4 + 1568*16*4)+(32*(horizontalPos-2) + 16)*4+1)]
        colliderRight = parallaxMap[((1568*32*(verticalPos-1)*4 + 1568*16*4)+(32*(horizontalPos) + 16)*4+1)]
        
        npcColliders = False
        for x in range(len(npcs)):
            if facing == "up":
                if npcs[x].getVertical() == verticalPos - 1 and npcs[x].getHorizontal() == horizontalPos:
                    npcColliders = True
            elif facing == "down":
                if npcs[x].getVertical() == verticalPos + 1 and npcs[x].getHorizontal() == horizontalPos:
                    npcColliders = True
            elif facing == "left":
                if npcs[x].getVertical() == verticalPos and npcs[x].getHorizontal() == horizontalPos - 1:
                    npcColliders = True
            elif facing == "right":
                if npcs[x].getVertical() == verticalPos and npcs[x].getHorizontal() == horizontalPos + 1:
                    npcColliders = True

        if moving > 0:
            if facing == "up":
                if colliderUp != 0 and verticalPos > 2 and not npcColliders:
                    mapMovedVertical -= 0.004
                    movedVertical -= 0.004
            elif facing == "down":
                if colliderDown != 0 and verticalPos < 29 and not npcColliders:
                    movedVertical += 0.004
                    mapMovedVertical += 0.004
            elif facing == "left":
                if colliderLeft != 0 and horizontalPos > 1 and not npcColliders:
                    movedHorizontal += 0.004
                    mapMovedHorizontal += 0.004
            elif facing == "right":
                if colliderRight != 0 and horizontalPos < 49 and not npcColliders:
                    movedHorizontal -= 0.004
                    mapMovedHorizontal -= 0.004
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
        glBegin(GL_QUADS)                   # Start drawing a 4 sided polygon
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
            #for ease of use, NPC coords are given using practical coords. Convert them to the OpenGL coords of our scene. 
            transmatrixX.append((npcs[x].getHorizontal()-25)*2 + mapMovedHorizontal)
            transmatrixY.append((-npcs[x].getVertical()+15)*2 - vertOffset + mapMovedVertical)
            
            if npcs[x].getFlagForUpdate():
                print(x)
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
                
        vertex = []
        vertices = []
        vertex.append(1.0)
        vertex.append(1.0)
        vertex.append(0.0)
        vertices.append(vertex)
        vertex = []      
        vertex.append(-1.0)
        vertex.append(1.0)
        vertex.append(0.0)
        vertices.append(vertex)
        vertex = []   
        vertex.append(-1.0)
        vertex.append(-1.0)
        vertex.append(0.0)
        vertices.append(vertex)
        vertex = []   
        vertex.append(1.0)
        vertex.append(-1.0)
        vertex.append(0.0)
        vertices.append(vertex)
        
        for x in range(len(transmatrixX)):
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

        #  since this is double buffered, swap the buffers to display what just got drawn.
        glutSwapBuffers()

    # The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
    def keyPressed(self, *args):
        global holdingLeft, holdingRight, holdingUp, holdingDown
        if args[0] == b"\033": # If escape is pressed, kill everything.
            sys.exit()
        elif args[0] == b'w' or args[0] == b'W':
            holdingUp = True
        elif args[0] == b'a' or args[0] == b'A':
            holdingLeft = True
        elif args[0] == b's' or args[0] == b'S':
            holdingDown = True
        elif args[0] == b'd' or args[0] == b'D':
            holdingRight = True

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
        glutIdleFunc(self.DrawGLScene)

        # Register the function called when our window is resized.
        glutReshapeFunc(self.ReSizeGLScene)

        # Register the function called when the keyboard is pressed.
        glutKeyboardFunc(self.keyPressed)
        glutKeyboardUpFunc(self.keyReleased)

        # Initialize our window.
        self.InitGL(640, 480)

        # Start Event Processing Engine
        glutMainLoop()

#And here we go...fingers crossed.
Main().main()