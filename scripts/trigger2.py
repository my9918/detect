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



def image_callback(msg):
    global crosswalk_detected
    # 横断歩道が検出されていない場合、関数を実行せずに終了
    if not crosswalk_detected:
        return
    
    bridge = CvBridge()
    # ROSのイメージメッセージをOpenCVの画像に変換
    image_origin = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
    #cv2.imwrite("detection.jpg", image_origin) #yoloででてくる生の画像：線なし切り抜いていない画像

    image = image_origin

    
    image = image[bbox.ymin:bbox.ymax,bbox.xmin:bbox.xmax]
    #print("\nbbox.xmin",bbox.xmin,"\n")

    height, width = image.shape[:2]
    edited_height = height *  0.2 #上から何％カットするか1.0で100％
    edited_width = width * 1/2
    #print(height, width)


    list_deg=[]  
    lines=[]
    #エフェクト処理
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,90,450,apertureSize = 3)

    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/360, threshold=150, minLineLength=300, maxLineGap=70)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        rad = math.atan2(y1 - y2, x2 - x1)
        deg = np.rad2deg(rad)
        if (10 < deg) or (deg < -10) or y1 < edited_height or y2 < edited_height:
            # 横縞以外の邪魔な線　BGR形式
            cv2.line(image,(x1,y1),(x2,y2),(255,0,0),1,lineType=cv2.LINE_AA)
        else:
            # 横縞
            if(0 <= deg):
                cv2.line(image,(x1,y1),(x2,y2),(0,0,255),1,lineType=cv2.LINE_AA)
            else:
                cv2.line(image,(x1,y1),(x2,y2),(0,255,0),1,lineType=cv2.LINE_AA)
            list_deg.append(deg) 
            #print(deg)"""


    cv2.imwrite("result.jpg", image)
    cv2.imwrite("detection.jpg", image_origin) #線を書き込まれた切り抜いていない画像


    #print("画像を書き込みました")
    

    list_deg.sort()
    #print(list_deg)
    #del list_deg[0:40]
    detect_angle = np.mean(list_deg)   
    print("detect_angle",detect_angle)

    # 受け取った値に加える
    detect_angle_value = -90 #  detect_angle
    print("detect_angle_value",detect_angle_value)
    # 新しい値をパブリッシュする
    pub.publish(detect_angle_value)
    crosswalk_detected = False

def bounding_boxes_callback(msg):
    global bounding_boxes,bbox,crosswalk_detected
    bounding_boxes = msg
    for bbox in msg.bounding_boxes:
        if bbox.Class == 'crosswalk' and bbox.probability >= 0.3:
            #rospy.loginfo("Received BoundingBoxes")
            #rospy.loginfo("Received BoundingBoxes:\n%s", bounding_boxes)
            #print("座標",bbox.xmin,bbox.ymin,bbox.ymax,bbox.xmax)
            # 横断歩道が検出されたフラグをセット
            crosswalk_detected = True
            rospy.Subscriber("/yolov5/image_out", Image, image_callback)
        else:
            rospy.loginfo("NOOOO")


    

def main():
    global pub  # pubをグローバル変数として使用することを明示
    rospy.init_node('main', anonymous=True)
    rospy.Subscriber('/yolov5/detections', BoundingBoxes, bounding_boxes_callback)
    pub = rospy.Publisher('detect', Float64, queue_size=10)

    rospy.spin()


if __name__ == '__main__':
    print("start")
    main()
