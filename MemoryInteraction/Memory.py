#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
# Example: A Simple class to get & read FaceDetected Events
## Usage: python human-gretter.py --ip nao.local
"""

import qi
import time
import sys
import argparse
from random import *

from pointToCards import main as pointToCard

class Card():
    picture = None
    xcoord = None
    ycoord = None
    __isActive = True
    
    def __init__(self, picture, xcoord, ycoord):
        self.picture = picture
        self.xcoord = xcoord
        self.ycoord = ycoord
        
    def getIsActive(self):
        return self.__isActive
        
    def setIsActive(self, isActive):
        self.__isActive = isActive

class GameState(object):
    def __init__(self):
        self.pictures = ["bus", "broccoli", "coffee", "teddy", "bottle", "car", "dog", "orange", "apple", "hydrant"]
        self.board = [ [ None for i in range(4) ] for j in range(4) ]
        self.history = []

        self.naoPoints = 0
        self.humanPoints = 0

    def updateScore(self, oldCount):
        currentCount = 0
        for row in self.board:
            for card in row:
                if card != None:
                    currentCount += 1

        self.humanPoints += (oldCount - currentCount) %2


class NaoRobot(object): 
    def __init__(self):
        self.knownCards = []
        self.knownPairs = []
        self.unknownCards = []

        for i in range(4):
            for j in range(4):
                self.unknownCards.append(Card("unknown", i, j))

    def deleteCardFromList(self, card, li):
        if(li == "unknownCards"):
            for i in self.unknownCards:
                if(i.xcoord == card.xcoord and i.ycoord == card.ycoord):
                    self.unknownCards.remove(i)
        elif(li == "knownCards"):
            for i in self.knownCards:
                if(i.xcoord == card.xcoord and i.ycoord == card.ycoord):
                    self.knownCards.remove(i)
        elif(li == "knownPairs"):
            for i in self.knownPairs:
                if(i.picture == card.picture):
                    self.knownPairs.remove(i)

    def getStateOfBoard(self):
        # currentBoard = [
        #     ["dog", None, "hidden", "hidden", "hidden"],
        #     ["hidden", "hidden", "hidden", "hidden", "hidden"],
        #     ["hidden", None, "hidden", "hidden", None],
        #     [None, "hidden", "bus", "hidden", "hidden"]
        # ]

        currentBoard = []

        # TODO: fetch two dimensional array from image recognition interface

        return currentBoard

    def checkForKnownPairs(self):
        knownPair = None

        if len(self.knownPairs) > 0:
            knownPair = [self.knownPairs[0]]
            knownPair.append(self.knownPairs[1])

            self.deleteCardFromList(self.knownPairs[0], "knownPairs")
            self.deleteCardFromList(self.knownPairs[1], "knownPairs")

        return knownPair

    def checkForKnownCard(self, newCard):
        knownCard = None

        for card in self.knownCards:
            if card.picture == newCard.picture:
                knownCard = card

        return knownCard

    def pickRandomCard(self):
        return self.unknownCards[randint(0, len(self.unknownCards) - 1)]

    def countCards(self):
        return len(self.unknownCards) + len(self.knownCards) + len(self.knownPairs)

    def updateState(self, board):
        # TODO: check which cards currently on the lists are now missing from the board
        print("Update the state.")

class MemoryGame(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, session):
        """
        Initialisation of qi framework and event detection.
        """
        super(MemoryGame, self).__init__()

        # Get the service ALMemory.
        self.session = session
        self.memory = session.service("ALMemory")
        self.tts = session.service("ALTextToSpeech")

        # Get the service ALDialog
        self.ALDialog = session.service("ALDialog")
        self.ALDialog.setLanguage("German")

        # self.topics = {
        #     "startGame": "startGame_topic",
        #     "humansTurn": "humansTurn_topic",
        #     "naosTurn": "naosTurn_topic"
        # }

        # for topicName in self.topics:
        #     self.loadTopic(self.topics[topicName])

        # print("All loaded topics: " + str(self.ALDialog.getAllLoadedTopics()))

        # Connect the event callback.
        subscriberHumansTurn = self.memory.subscriber("HumansTurn")
        subscriberNaosTurn = self.memory.subscriber("NaosTurn")

        subscriberHumansTurn.signal.connect(self.humansTurn)
        subscriberNaosTurn.signal.connect(self.naosTurn)

        self.gameState = GameState()
        self.naoRobot = NaoRobot()

        self.run()

    def loadTopic(self, topicName):
        try:
            self.ALDialog.loadTopic("/home/nao/topics/" + topicName + ".top")
        except Exception as e:
            print(str(e))

    def naosTurn(self, value):
        print("NAOs turn starts.")
        isPair = False

        self.gameState.board = self.naoRobot.getStateOfBoard()
        self.gameState.updateScore(self.naoRobot.countCards())
        self.naoRobot.updateState(self.gameState.board)

        knownPair = self.naoRobot.checkForKnownPairs()
        if knownPair:
            pointToCard(self.session, [knownPair[0].xcoord, knownPair[0].ycoord])
        else:
            firstUnknownCard = self.naoRobot.pickRandomCard()
            pointToCard(self.session, [firstUnknownCard.xcoord, firstUnknownCard.ycoord])
            intermediateBoard = self.naoRobot.getStateOfBoard()
            firstUnknownCard.picture = intermediateBoard[firstUnknownCard.xcoord][firstUnknownCard.ycoord]

        if knownPair: 
            pointToCard(self.session, [knownPair[1].xcoord, knownPair[1].ycoord])
            self.gameState.naoPoints += 1
            isPair = True
        else:
            knownCard = self.naoRobot.checkForKnownCard(firstUnknownCard)

            if knownCard:
                pointToCard(self.session, [knownCard.xcoord, knownCard.ycoord])
                self.naoRobot.deleteCardFromList(firstUnknownCard, "unknownCards")
                self.naoRobot.deleteCardFromList(knownCard, "knownCards")
                self.gameState.naoPoints += 1
                isPair = True
            else:
                self.naoRobot.deleteCardFromList(firstUnknownCard, "unknownCards")
                self.naoRobot.knownCards.append(firstUnknownCard)

                secondUnknownCard = self.naoRobot.pickRandomCard()
                pointToCard(self.session, [secondUnknownCard.xcoord, secondUnknownCard.ycoord])
                intermediateBoard = self.naoRobot.getStateOfBoard()
                secondUnknownCard.picture = intermediateBoard[firstUnknownCard.xcoord][firstUnknownCard.ycoord]

                self.naoRobot.deleteCardFromList(secondUnknownCard, "unknownCards")

                if firstUnknownCard.picture == secondUnknownCard.picture:
                    self.gameState.naoPoints += 1
                    isPair = True
                    self.naoRobot.deleteCardFromList(firstUnknownCard, "knownCards")
                else:
                    knownCard = self.naoRobot.checkForKnownCard(secondUnknownCard)
                    if knownCard:
                        self.naoRobot.deleteCardFromList(knownCard, "knownCards")
                        self.naoRobot.knownPairs.append(knownCard)
                        self.naoRobot.knownPairs.append(secondUnknownCard)
                    else:
                        self.naoRobot.knownCards.append(secondUnknownCard)

        if isPair:
            self.tts.say("Bitte nimm das Paar vom Spielbrett. Dann starte ich meinen nächsten Zug!")
            self.tts.say("Ich habe gerade " + str(self.gameState.naoPoints) + " und du hast gerade " + str(self.gameState.humanPoints) + " Punkte.")
            self.memory.raiseEvent("NaosTurn", 1)
        else: 
            self.tts.say("Bitte dreh die Karten wieder um und beginne mit deinem Zug.")
            self.tts.say("Ich habe gerade " + str(self.gameState.naoPoints) + " und du hast gerade " + str(self.gameState.humanPoints) + " Punkte.")
            self.memory.raiseEvent("HumansTurn", 1)

        print("Nao's turn ends.")

    def humansTurn(self, value):
        print("Human's turn starts.")

        try:
            raw_input("\nDrücke Enter, wenn du deinen Zug abgeschlossen hast!")
        finally: 
            self.memory.raiseEvent("NaosTurn", 1)
            print("Human's turn ends.")
        
    def destroyGame(self):
        activeTopics = self.ALDialog.getActivatedTopics()
        print("ActiveTopics at exit:" + str(activeTopics))

        self.ALDialog.unsubscribe("PlayingMemory")

        for topicName in self.topics:
            try: 
                self.ALDialog.deactivateTopic(self.topics[topicName])
                self.ALDialog.unloadTopic(self.topics[topicName])
            except Exception as e:
                print(str(e))

    def run(self):
        print("Starting MemoryGame")

        self.memory.raiseEvent("NaosTurn", 1)

        while True:
            time.sleep(20)
            print("Is it Naos turn? " + str(self.memory.getData("NaosTurn")))
            print("Is it Humans turn? " + str(self.memory.getData("HumansTurn")))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="nao.local",
                        help="Robot's IP address. If on a robot or a local Naoqi - use '127.0.0.1' (this is the default value).")
    parser.add_argument("--port", type=int, default=9559,
                        help="port number, the default value is OK in most cases")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://{}:{}".format(args.ip, args.port))
    except RuntimeError:
        print ("\nCan't connect to Naoqi at IP {} (port {}).\nPlease check your script's arguments."
               " Run with -h option for help.\n".format(args.ip, args.port))
        sys.exit(1)
    memoryGame = MemoryGame(session)
