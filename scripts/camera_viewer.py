#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def image_callback(msg):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    cv2.imshow("Camera", cv_image)
    cv2.waitKey(1)

def camera_viewer():
    rospy.init_node("camera_viewer")
    rospy.Subscriber("usb_cam/image_raw", Image, image_callback)
    rospy.spin()

#このスクリプトが直接実行された場合にのみcamera_viewer関数を呼び出すための条件文
if __name__ == "__main__":
    camera_viewer()
