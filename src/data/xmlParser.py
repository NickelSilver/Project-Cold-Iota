__author__ = 'Matt'

import xml.etree.ElementTree as ET

class xmlParser():

    def readDialogue(self, dialogueNumber):

        tree = ET.parse('data\story.xml')
        root = tree.getroot()

        dialogueroot = ""
        #search for appropriate story

        for dialogue in root.findall('dialogue'):
            #gets attribute

            if int(dialogue.get('id')) == int(dialogueNumber):

                dialogueroot = dialogue
        if dialogueroot != "":
            characterList = []
            textList = []

            for eachCharacter in dialogueroot.iter('character'):
                #join game speech into two different lists, one list displays character, second list displays his/her speech.
                character = eachCharacter.get('id')
                text = eachCharacter.text
                characterList.append(character)
                textList.append(text)
            return characterList, textList
        else:
            return [],[]




