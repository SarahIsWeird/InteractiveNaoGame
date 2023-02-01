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
        ALDialog.setLanguage("German")
        memory = session.service("ALMemory")

        #if topic is not put into home/nao folder, change path here...
        startGame = ALDialog.loadTopic("/home/nao/start_memoryGame_topic.top")

        # Activating the loaded topic
        ALDialog.activateTopic(startGame)
        # Connect the event callback.
        subscriber = memory.subscriber("PlayingMemory")
        subscriber.signal.connect(startGame)
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = session.service("ALTextToSpeech")
        #self.face_detection = session.service("ALFaceDetection")
        #self.face_detection.subscribe("HumanGreeter")
        self.got_MemoryBoard = False

    def startGame(self):


    def run(self):
        print "Starting MemoryGame"
        try:
            ALDialog.setFocus(startGame)
            ALDialog.forceOutput()
        finally:
            ALDialog.unsubscribe("PlayingMemory")
            ALDialog.deactivateTopic(startGame)
            ALDialog.unloadTopic(startGame)'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
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
