'''
Created on 20 Oct 2014

@author: Nickel
'''

def doMapLogic(map, x, y):
    if map == "swamp1" and x >= 48:
        print("Teleport1")
    elif map == "swamp1" and y >= 27:
        print("Teleport2")
    elif map == "swamp1" and x <= -48:
        print("Teleport3")
    elif map == "swamp1" and y <= -26:
        print("Teleport4")
        