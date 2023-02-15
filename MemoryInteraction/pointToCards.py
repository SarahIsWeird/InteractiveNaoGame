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


def main(session, cardCoordinates=[0,3]):
    """
    Example of a whole body Left or Right Arm position control
    Warning: Needs a PoseInit before executing
            Whole body balancer must be inactivated at the end of the script
    This example is only compatible with NAO
    """
    # Get the service ALMotion.

    if cardCoordinates[0] < 3:
        chainName = "LArm"
        handName = "LHand"
    else: 
        chainName = "RArm"
        handName = "RHand"

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    backgroundMovement_service = session.service("ALBackgroundMovement")
    tts_service = session.service("ALTextToSpeech")

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
    motion_service.wbEnableEffectorControl(chainName, isEnabled)

    # Example showing how to set position target for LArm
    # The 3 coordinates are absolute LArm position in FRAME_ROBOT
    # Position in meter in x, y and z axis.

    # X Axis LArm Position feasible movement = [ +0.00, +0.12] meter
    # Y Axis LArm Position feasible movement = [ -0.05, +0.10] meter
    # Y Axis RArm Position feasible movement = [ -0.10, +0.05] meter
    # Z Axis LArm Position feasible movement = [ -0.10, +0.10] meter

    coef = 1.0
    if chainName == "LArm":
            coef = +1.0
    elif chainName == "RArm":
        coef = -1.0

    xAxisMapping = [+0.10, +0.025, -0.05, +0.025, +0.10]
    yAxisMapping = [+0.10, +0.03, -0.03, -0.10]
    targetCoordinate = [ +0.12, xAxisMapping[cardCoordinates[0]]*coef, yAxisMapping[cardCoordinates[1]]]

    print("Pointing Infos:")
    print("Koordinate: " + str(targetCoordinate))
    print("Chain Name: " + chainName)
    print("Hand Name: " + handName)

    # wbSetEffectorControl is a non blocking function
    # time.sleep allow head go to his target
    # The recommended minimum period between two successives set commands is
    # 0.2 s.
    # for targetCoordinate in targetCoordinateList:
    #     print("Progressive Arm Coordinates:")
    #     print(motion_service.getPosition(chainName, frame, useSensor))
    #     targetCoordinate = [targetCoordinate[i] + effectorInit[i] for i in range(3)]
    #     motion_service.wbSetEffectorControl(chainName, targetCoordinate)
    #     time.sleep(4.0)

    motion_service.openHand(handName)

    targetCoordinate = [targetCoordinate[i] + effectorInit[i] for i in range(3)]
    motion_service.wbSetEffectorControl(chainName, targetCoordinate)

    letter = ["A", "B", "C", "D", "E"][cardCoordinates[0]]
    tts_service.say("Drehe die Karte " + letter + " " + str(cardCoordinates[1] + 1)  + " um.")

    time.sleep(5.0)

    initCoordinate = [effectorInit[i] for i in range(3)]
    motion_service.wbSetEffectorControl(chainName, initCoordinate)

    motion_service.closeHand(handName)

    motion_service.setIdlePostureEnabled(chainName, True)

    # print motion state
    # print("Final state: ")
    # print(motion_service.getSummary())
    # print("Final Arm Coordinates:")
    # print(motion_service.getPosition(chainName, frame, useSensor))


    # Go to rest position
    posture_service.goToPosture("StandInit", 0.5)

    time.sleep(5)

    backgroundMovement_service.setEnabled(True)

    # time.sleep(10)

    # motion_service.rest()

    # Deactivate Head tracking
    # motion_service.wbEnableEffectorControl(chainName, False)
    # motion_service.wbEnable(False)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="nao.local",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)


# Initial State:
# ---------------------- Model ---------------------------
#         BodyName   Stiffness     Command      Sensor
#          HeadYaw    1.000000    0.000000   -0.016916
#        HeadPitch    1.000000    0.000000   -0.015382
#   LShoulderPitch    1.000000    1.401270    1.451122
#    LShoulderRoll    1.000000    0.298589    0.273010
#        LElbowYaw    1.000000   -1.387686   -1.357632
#       LElbowRoll    1.000000   -1.004115   -0.974048
#        LWristYaw    1.000000    0.001146    0.024502
#     LHipYawPitch    1.000000    0.000000   -0.007628
#         LHipRoll    1.000000    0.000000    0.004644
#        LHipPitch    1.000000   -0.450000   -0.454022
#       LKneePitch    1.000000    0.700000    0.704064
#      LAnklePitch    1.000000   -0.350000   -0.360532
#       LAnkleRoll    1.000000    0.000000   -0.001492
#     RHipYawPitch    1.000000    0.000000   -0.007628
#         RHipRoll    1.000000    0.000000   -0.010696
#        RHipPitch    1.000000   -0.450000   -0.454106
#       RKneePitch    1.000000    0.700000    0.702614
#      RAnklePitch    1.000000   -0.350000   -0.358914
#       RAnkleRoll    1.000000    0.000000    0.000042
#   RShoulderPitch    1.000000    1.401148    1.446604
#    RShoulderRoll    1.000000   -0.298443   -0.271560
#        RElbowYaw    1.000000    1.388265    1.365218
#       RElbowRoll    1.000000    1.003817    0.972598
#        RWristYaw    1.000000    0.001399    0.035240
#            LHand    1.000000    0.250000    0.258800
#            RHand    1.000000    0.250000    0.258400
# ---------------------- Tasks  --------------------------
#             Name         ID
#    IdleAnimation           6
# ----------------- Motion Cycle Time --------------------
#               24 ms
# Initial Arm Coordinates:
# [0.11987698823213577, 0.1335529088973999, 0.2744051516056061, -1.2157829999923706, 0.48279911279678345, 0.015403485856950283]
# Progressive Arm Coordinates:
# [0.22570770978927612, 0.13133499026298523, 0.27807313203811646, -1.482122540473938, 0.6948450207710266, 0.09956952929496765]
# Progressive Arm Coordinates:
# [0.2035769671201706, 0.13631191849708557, 0.21660387516021729, -1.1806901693344116, 0.9689118266105652, -0.16998720169067383]
# Progressive Arm Coordinates:
# [0.21043676137924194, 0.17680594325065613, 0.21758432686328888, -0.9920628666877747, 0.9923311471939087, 0.16810989379882812]
# Progressive Arm Coordinates:
# [0.2386760413646698, 0.1820129156112671, 0.3655085265636444, -1.5407930612564087, 0.2853245139122009, 0.3454590141773224]
# Progressive Arm Coordinates:
# [0.23883701860904694, 0.04081866145133972, 0.3655291795730591, -1.7411075830459595, 0.2888936698436737, -0.31031906604766846]
# Progressive Arm Coordinates:
# [0.21288186311721802, 0.05323245748877525, 0.2134728878736496, -2.7432353496551514, 0.9872819781303406, -0.5297163128852844]
# Progressive Arm Coordinates:
# [0.20991423726081848, 0.13283973932266235, 0.2152082622051239, -1.907836675643921, 1.03239107131958, -0.020415790379047394]
# Progressive Arm Coordinates:
# [0.22526486217975616, 0.13107475638389587, 0.27826544642448425, -2.245330810546875, 0.76698237657547, 0.10250744223594666]
# Final Arm Coordinates:
# [0.12041959911584854, 0.13286729156970978, 0.2654464840888977, -2.1833672523498535, 0.8938819766044617, 0.23948067426681519]
# Final state: 
# ---------------------- Model ---------------------------
#         BodyName   Stiffness     Command      Sensor
#          HeadYaw    1.000000   -0.001573    0.013764
#        HeadPitch    1.000000    0.114672    0.104270
#   LShoulderPitch    1.000000    1.027455    1.049214
#    LShoulderRoll    1.000000    0.141954    0.127280
#        LElbowYaw    1.000000   -1.794388   -1.782550
#       LElbowRoll    1.000000   -0.036749   -0.019900
#        LWristYaw    1.000000   -0.582255   -0.569156
#     LHipYawPitch    1.000000    0.000073    0.004644
#         LHipRoll    1.000000    0.015861    0.016916
#        LHipPitch    1.000000    0.125273    0.130432
#       LKneePitch    1.000000   -0.092328   -0.089014
#      LAnklePitch    1.000000    0.050174    0.052114
#       LAnkleRoll    1.000000   -0.015817   -0.016832
#     RHipYawPitch    1.000000    0.000073    0.004644
#         RHipRoll    1.000000    0.015862    0.018450
#        RHipPitch    1.000000    0.124617    0.124212
#       RKneePitch    1.000000   -0.092328   -0.088930
#      RAnklePitch    1.000000    0.050830    0.050664
#       RAnkleRoll    1.000000   -0.015809   -0.016832
#   RShoulderPitch    1.000000    1.193589    1.233378
#    RShoulderRoll    1.000000   -0.129108   -0.116626
#        RElbowYaw    1.000000    0.907507    0.891212
#       RElbowRoll    1.000000    0.102330    0.089014
#        RWristYaw    1.000000    0.099954    0.079726
#            LHand    0.000000    0.019453    0.018000
#            RHand    1.000000    0.718451    0.715200
# ---------------------- Tasks  --------------------------
#             Name         ID
# angleInterpolationBezier         273
# ----------------- Motion Cycle Time --------------------
#               24 ms
