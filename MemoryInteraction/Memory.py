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

        # Get the service ALDialog
        self.ALDialog = session.service("ALDialog")
        self.ALDialog.setLanguage("German")

        try:
            # If topic is not put into home/nao folder, change path here...
            self.startGameTopic = self.ALDialog.loadTopic("/home/nao/topics/start_memoryGame_topic.top")
        except:
            self.startGameTopic = "start_game_topic"

        try:
            # If topic is not put into home/nao folder, change path here...
            self.humansTurnTopic = self.ALDialog.loadTopic("/home/nao/topics/memoryGame_HumansTurn.top")
        except:
            self.humansTurnTopic = "humansTurn_topic"

        try:
            # If topic is not put into home/nao folder, change path here...
            self.humansTurnTopic = self.ALDialog.loadTopic("/home/nao/topics/memoryGame_NaosTurn.top")
        except:
            self.humansTurnTopic = "naosTurn_topic"

        self.ALDialog.activateTopic(self.startGameTopic)
        self.ALDialog.activateTopic(self.humansTurnTopic)
        self.ALDialog.activateTopic(self.naosTurnTopic)

        self.ALDialog.subscribe("PlayingMemory")

        # Connect the event callback.
        subscriberHumansTurn = self.memory.subscriber("HumansTurn")
        subscriberNaosTurn = self.memory.subscriber("NaosTurn")

        subscriberHumansTurn.signal.connect(self.humansTurn)
        subscriberNaosTurn.signal.connect(self.naosTurn)

        self.ALDialog.setFocus(self.startGameTopic)
        self.run()
        
        self.state = GameState()

    def naosTurn(self):
        print("It's NAOs turn.")

        # TODO: update the state, 
        #       i.e. recognize the cards on the board, 
        #       remove missing cards from game state, 
        #       update game score

        # TODO: check if matching pair is known
        # TODO: determine first card to flip and point
        pointToCard(self.session, [0,0])
        # TODO: check if flipped card matches a known card
        # TODO: determine second card to flip and point
        pointToCard(self.session, [2,2])

        # TODO: recognize second flipped card, 
        #       save unknown ones to state, 
        #       check if it's a pair

        # TODO: tell human to flip cards or 
        #       take them off the board, if it was a pair

        # TODO: announce current score

        self.ALDialog.say("/home/nao/topics/memoryGame_NaosTurn.top", "doneWithTurn")

    def humansTurn(self):
        self.activateOnlyTopic(self.humansTurnTopic)
        print("It's human's turn.")

    def activateOnlyTopic(topicName):
        # TODO: write function
        print("Active Topic: " + topicName)
        
    def destroyGame(self):
        self.ALDialog.unsubscribe("PlayingMemory")
        self.ALDialog.deactivateTopic(self.startGameTopic)
        self.ALDialog.deactivateTopic(self.humansTurnTopic)
        self.ALDialog.unloadTopic(self.startGameTopic)
        self.ALDialog.unloadTopic(self.humansTurnTopic)

    def run(self):
        print("Starting MemoryGame")

        try:
            raw_input("\nSpeak to the robot using rules from the just loaded .top file. Press Enter when finished:")
        
        finally:
            self.destroyGame()



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
