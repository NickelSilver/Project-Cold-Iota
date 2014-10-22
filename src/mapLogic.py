'''
Created on 20 Oct 2014

@author: Nickel
'''

def doMapLogic(map, x, y, facing): 
    if map == "town1" and x >= 19 and x <= 21 and y >= 29 and facing == "down":
        print("Teleport")
        