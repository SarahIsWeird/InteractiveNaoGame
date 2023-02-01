#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

# Maybe look into this repo: 
# https://github.com/thomasweng15/nao-looking-and-pointing/blob/8cbfb4b272deecf6758ea23259ce5d4a28602994/naoGestures.py#L51

"""Example: Whole Body Motion - Left or Right Arm position control"""

import qi
import argparse
import sys
import motion
import time
import math

from getImages import main as getImageMain

def main(session, chainName, app):
    """
    Example of a whole body Left or Right Arm position control
    Warning: Needs a PoseInit before executing
            Whole body balancer must be inactivated at the end of the script
    This example is only compatible with NAO
    """
    # Get the service ALMotion.


    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    frame     = motion.FRAME_ROBOT
    useSensor = False

    effectorInit = motion_service.getPosition(chainName, frame, useSensor)

    # print motion state
    # print("Initial State:")
    # print(motion_service.getSummary())
    # print("Initial Arm Coordinates:")
    # print(effectorInit)

    # Active LArm tracking
    isEnabled = True
    # motion_service.wbEnableEffectorControl(chainName, isEnabled)
    motion_service.wbEnableEffectorControl('Head', isEnabled)

    targetCoordinate = [ 00.0,  +10.0,  +0.0]
    targetCoordinate = [target*math.pi/180.0 for target in targetCoordinate]
    motion_service.wbSetEffectorControl('Head', targetCoordinate)

    # Example showing how to set position target for LArm
    # The 3 coordinates are absolute LArm position in FRAME_ROBOT
    # Position in meter in x, y and z axis.

    # X Axis LArm Position feasible movement = [ +0.00, +0.12] meter
    # Y Axis LArm Position feasible movement = [ -0.05, +0.10] meter
    # Y Axis RArm Position feasible movement = [ -0.10, +0.05] meter
    # Z Axis LArm Position feasible movement = [ -0.10, +0.10] meter

    # wbSetEffectorControl is a non blocking function
    # time.sleep allow head go to his target
    # The recommended minimum period between two successives set commands is
    # 0.2 s.

    getImageMain(app)

    time.sleep(5.0)

    # print motion state
    # print("Final state: ")
    # print(motion_service.getSummary())
    # print("Final Arm Coordinates:")
    # print(motion_service.getPosition(chainName, frame, useSensor))


    

    # Go to rest position
    motion_service.rest()

    # Deactivate Head tracking
    isEnabled    = False
    motion_service.wbEnableEffectorControl(chainName, isEnabled)
    motion_service.wbEnable(False)

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="nao.local",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--chain", type=str, default="LArm",
                        choices=["LArm", "RArm"], help="Chain name")

    args = parser.parse_args()
    session = qi.Session()
    try:
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        session.connect(connection_url)
        app = qi.Application(["GetImage", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session, args.chain, app)
