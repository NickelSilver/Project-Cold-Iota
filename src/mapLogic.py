'''
Created on 20 Oct 2014

@author: Nickel
'''

def doMapLogic(scenemap, x, y, facing): 
    if scenemap == "town1" and x >= 19 and x <= 21 and y >= 29 and facing == "down":
        print("Teleport")
        return True
        