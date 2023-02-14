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

from pointToCards import main as pointToCard

class GameState(object):
    def __init__(self):
        self.naoPoints = 0
        self.humanPoints = 0



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

        self.topics = {
            "startGame": "startGame_topic",
            "humansTurn": "humansTurn_topic",
            "naosTurn": "naosTurn_topic"
        }

        for topicName in self.topics:
            self.loadTopic(self.topics[topicName])

        print("All loaded topics: " + str(self.ALDialog.getAllLoadedTopics()))

        self.activateOnlyTopic(self.topics["startGame"])

        # Connect the event callback.
        subscriberHumansTurn = self.memory.subscriber("HumansTurn")
        subscriberNaosTurn = self.memory.subscriber("NaosTurn")

        subscriberHumansTurn.signal.connect(self.humansTurn)
        subscriberNaosTurn.signal.connect(self.naosTurn)

        self.run()
        
        self.state = GameState()

    def loadTopic(self, topicName):
        try:
            self.ALDialog.loadTopic("/home/nao/topics/" + topicName + ".top")
        except Exception as e:
            print(str(e))

    def activateOnlyTopic(self, topicName):
        try:
            self.ALDialog.unsubscribe("PlayingMemory")
        except Exception as e:
            print(str(e))

        activeTopics = self.ALDialog.getActivatedTopics()
        print("Previous ActiveTopics:" + str(activeTopics))

        for topic in activeTopics: 
            self.ALDialog.deactivateTopic(topic)


        print("Topic to be activated: " + topicName)
        # self.ALDialog.activateTopic(topicName)

        # Check if activation was done correctly
        activeTopics = self.ALDialog.getActivatedTopics()
        print("After ActiveTopics:" + str(activeTopics))

        self.ALDialog.subscribe("PlayingMemory")

    def naosTurn(self, value):
        print("NAOs turn starts.")

        # self.activateOnlyTopic(self.topics["naosTurn"])

        # TODO: update the state, 
        #       i.e. recognize the cards on the board, 
        #       remove missing cards from game state, 
        #       update game score

        # TODO: check if matching pair is known
        # TODO: determine first card to flip and point
        pointToCard(self.session, [0,0])

        # TODO: check if flipped card matches a known card
        # TODO: determine second card to flip and point
        # pointToCard(self.session, [2,2])

        # TODO: recognize second flipped card, 
        #       save unknown ones to state, 
        #       check if it's a pair

        # TODO: tell human to flip cards or 
        #       take them off the board, if it was a pair

        # TODO: announce current score

        self.tts.say("Drehe die Karte A 1 um.")
        self.memory.raiseEvent("HumansTurn", 1)
        print("Nao's turn ends.")

    def humansTurn(self, value):
        print("Human's turn starts.")
        # self.activateOnlyTopic(self.topics["humansTurn"])

        # input("Drücke Enter, wenn du deinen Zug abgeschlossen hast!")
        try:
            raw_input("\nSpeak to the robot using rules from the just loaded .top file. Press Enter when finished:")
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
