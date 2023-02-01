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
        self.memory = session.service("ALMemory")
        self.ALDialog = session.service("ALDialog")
        self.ALDialog.setLanguage("English")

        #memory = session.service("ALMemory")

        #if topic is not put into home/nao folder, change path here...
        try:
            self.startGameTopic = self.ALDialog.loadTopic("/home/nao/topics/start_memoryGame_topic.top")
        except:
            self.startGameTopic = "start_game_topic"

        # Activating the loaded topic
        self.ALDialog.activateTopic(self.startGameTopic)

        self.ALDialog.subscribe("PlayingMemory")


        # Connect the event callback.
        # subscriber = memory.subscriber("PlayingMemory")
        # subscriber.signal.connect(self.startGame)
        
        # Get the services ALTextToSpeech and ALFaceDetection.
        
        #self.tts = session.service("ALTextToSpeech")
        #self.face_detection = session.service("ALFaceDetection")
        #self.face_detection.subscribe("HumanGreeter")
        #self.got_MemoryBoard = False

    def startGame(self):
        print "start game"

    def run(self):
        print "Starting MemoryGame"

        try:
            self.ALDialog.setFocus(self.startGameTopic)
            self.ALDialog.forceOutput()
            raw_input("\nSpeak to the robot using rules from the just loaded .top file. Press Enter when finished:")

        finally:
            self.ALDialog.unsubscribe("PlayingMemory")
            self.ALDialog.deactivateTopic(self.startGameTopic)
            self.ALDialog.unloadTopic(self.startGameTopic)


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
    memoryGame.run()
