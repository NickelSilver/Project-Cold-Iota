__author__ = 'Matt'

import xml.etree.ElementTree as ET


def readStory(storyNumber):

    tree = ET.parse('story.xml')
    root = tree.getroot()

    storyroot = root
    #search for appropriate story
    for story in root:
        #gets attribute
        if story.get('id') == storyNumber:
            storyroot = story

    characterList = []
    textList = []

    for eachCharacter in storyroot.iter('character'):
        #join game speech into two different lists, one list displays character, second list displays his/her speech.
        character = eachCharacter.get('id')
        text = eachCharacter.text
        characterList.append(character)
        textList.append(text)
    return characterList, textList

    #test

CharacterList, TextList = readStory('tutorial')


for index in range(len(CharacterList)):
    print(CharacterList[index])
    print(TextList[index])

