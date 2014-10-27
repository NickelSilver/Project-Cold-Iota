'''
Created on Oct 25, 2014

@author: Matt
'''
import unittest
from npc import npc

class Test(unittest.TestCase):
    

    def testName(self):
        pass
    
    def speak(self, text):
        print(text)
        
    def speakTo(self, text, destination):
        print(text)
    
    def move(self):
        ""
        
    
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()