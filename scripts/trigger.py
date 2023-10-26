#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float64
import numpy as np
import rospy
import time
from geometry_msgs.msg import Twist
import cv2
import math
from detection_msgs.msg import BoundingBoxes
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


def callback(data):
    
    rospy.Subscriber("/yolov5/image_out", Image, image_callback)
    #img_origin = image


    img_origin = cv2.imread("/home/galleria/raspicat_ws/src/detect/scripts/IMG_4122.JPG")
    #xyxy to yyxx   bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax    xmin: 319    ymin: 161    xmax: 1008    ymax: 432
    img = img_origin[649:1725,1281:4032]

    height, width = img.shape[:2]
    edited_height = height *  0.4
    edited_width = width * 1/2

    
    #img = img_origin[161:432,319:1008]
    #img = img_origin[bbox.ymin:bbox.ymax,bbox.xmin:bbox.xmax]

    #cv2.imshow("img", img)
    #cv2.waitKey(1)

    list_deg=[]  

    #エフェクト処理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,90,450,apertureSize = 3)

    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/360, threshold=150, minLineLength=300, maxLineGap=70)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        rad = math.atan2(y1 - y2, x2 - x1)
        deg = np.rad2deg(rad)
        if (10 < deg) or (deg < -10) or y1 < edited_height or y2 < edited_height:
            # 横縞以外の邪魔な線
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2,lineType=cv2.LINE_AA)
        else:
            # 横縞
            if(0 <= deg):
                cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2,lineType=cv2.LINE_AA)
            else:
                cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2,lineType=cv2.LINE_AA)
            list_deg.append(deg) 
            print(deg)


    cv2.imwrite("result.jpg", img)

    list_deg.sort()
    #print(list_deg)
    #del list_deg[0:40]
    detect_angle = np.mean(list_deg)   
    #print(detect_angle)

    # 受け取った値に10を加える
    new_value =data.data + 90 #  detect_angle
    print(new_value)
    # 新しい値をパブリッシュする
    pub.publish(new_value)

def image_callback(msg):
    global image
    bridge = CvBridge()
    # ROSのイメージメッセージをOpenCVの画像に変換
    image = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")


def bounding_boxes_callback(msg):
    global bounding_boxes
    bounding_boxes = msg
    for bbox in msg.bounding_boxes:
        if bbox.Class == 'crosswalk' and bbox.probability >= 0.6:
            #rospy.loginfo("Received BoundingBoxes")
            #rospy.loginfo("Received BoundingBoxes:\n%s", bounding_boxes)

            rospy.Subscriber('yaw', Float64, callback)
    

def main():
    global pub  # pubをグローバル変数として使用することを明示
    rospy.init_node('main', anonymous=True)
    #rospy.Subscriber('yaw', Float64, callback)
    rospy.Subscriber('/yolov5/detections', BoundingBoxes, bounding_boxes_callback)
    
    #detect = detect angle
    pub = rospy.Publisher('detect', Float64, queue_size=10)

    rospy.spin()

if __name__ == '__main__':
    print("start")
    main()
