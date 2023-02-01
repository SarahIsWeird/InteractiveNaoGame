#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Getting a video stream with CV"""

import qi
import argparse
import sys, select, os

import numpy as np
import cv2 as cv
import time
import vision_definitions

from naoqi import ALProxy

width = 320
height = 240

def main(app):
    app.start()
    # session = app.session

    # Get settings for the camera stream
    resolution = vision_definitions.kQVGA
    colorSpace = vision_definitions.kBGRColorSpace
    fps = 20

    # Getting the VideoDeviceProxy service
    videoDeviceProxy = ALProxy("ALVideoDevice", "nao.local", 9559)
    clientName = videoDeviceProxy.subscribeCamera("test", 1, resolution, colorSpace, fps)

    # yuvImage = np.zeros((height + height / 2, width), dtype = np.uint8)
    # imageHeader = np.zeros((height, width), dtype = np.uint8)

    # Create image heade for CV
    # imageHeader = cv.CreateMat(320, 240, cv.CV_8UC3)
    imageHeader = np.zeros((height, width, 3), dtype = "uint8")
    # cv.namedWindow("images")

    # img = videoDeviceProxy.getImageRemote(clientName)
    # imageHeader.data = bytearray(img[6])
    # cv.imwrite("images/image-one-mismatched-pair" + "1" + ".jpg", imageHeader)

    for i in range(0, 5): 
        img = videoDeviceProxy.getImageRemote(clientName)
        imageHeader.data = bytearray(img[6])
        cv.imwrite("./images/image-bottom-" + str(i) + ".jpg", imageHeader)
        time.sleep(1)
        

    while cv.waitKey(30) != 27:
        img = videoDeviceProxy.getImageRemote(clientName)
        imageHeader.data = bytearray(img[6])
        # yuvImage.data = bytearray(img[6])
        # imageHeader = cv.cvtColor(yuvImage, cv.COLOR_YUV2RGB_YV12, 3)
        
        cv.imshow("images", imageHeader)

        videoDeviceProxy.releaseImage(clientName)

    videoDeviceProxy.unsubscribe(clientName)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="nao.local",
                        help="Robot's IP address. If on a robot or a local Naoqi - use '127.0.0.1' (this is the default value).")
    parser.add_argument("--port", type=int, default=9559,
                        help="port number, the default value is OK in most cases")

    args = parser.parse_args()
    try:
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["GetImage", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("\nCan't connect to Naoqi at IP {} (port {}).\nPlease check your script's arguments."
               " Run with -h option for help.\n".format(args.ip, args.port))
        sys.exit(1)
    main(app)