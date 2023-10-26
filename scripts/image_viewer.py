#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def image_callback(msg):
    bridge = CvBridge()
    # ROSのイメージメッセージをOpenCVの画像に変換
    image = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
    
    # 画像の切り取り
    image = image[161:432,319:1008]
    #img = img_origin[649:1725,1281:4032]
    # 画像の表示
    cv2.imshow("Image", image)
    cv2.waitKey(1)

def main():
    rospy.init_node("image_subscriber")

    rospy.Subscriber("image_topic", Image, image_callback)
    #rospy.Subscriber("/yolov5/image_out", Image, image_callback)

    rospy.spin()

if __name__ == "__main__":
    main()
