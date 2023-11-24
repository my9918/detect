#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float64
import numpy as np
import time
from geometry_msgs.msg import Twist
import tf


# 閾値を設定
threshold = 10  # 仮の閾値、実際の値に合わせて調整してください

# detect_valueの前回値を保持するための変数
prev_detect_value = None

def detect_callback(data):
    global detect_value, prev_detect_value

    # detect_valueが最初に設定された場合はそのまま代入して処理を続行
    if detect_value is None:
        detect_value = data.data
        prev_detect_value = detect_value
        print("first detect_value:", detect_value)
        return

    # 前回値との差分を計算
    diff = abs(data.data - prev_detect_value)

    # 差分が閾値を超えた場合に通知し、detect_valueを更新
    if diff < threshold:#閾値を超えなかった場合


        if detect_value < yaw_value: #停止
            print("detect_value:",detect_value)
            print("detect_value - yaw_value:",detect_value - yaw_value)        
            print("first_yaw_value:",first_yaw_value)
        
            print("yaw_value + first_yaw_value:",yaw_value - first_yaw_value)
            twist.angular.x = 0.0
            twist.angular.z = 0.0
            pub.publish(twist)
            rospy.signal_shutdown("Detection value exceeded yaw value!")

        else: #目的角度まで旋回            
            print("detect_value:",detect_value)
            speed = 25 #deg/s目的の速度
            twist.angular.z = speed * 3.1415 / 180.0 #rad
            pub.publish(twist)
            print("twist pub\ndetect_value - yaw_value:",detect_value - yaw_value)
            print("#####################################################") 
                

        detect_value = data.data  # detect_valueを更新
        prev_detect_value = detect_value  # 前回値も更新

    else:
        print(f"Detect value changed significantly! Previous: {prev_detect_value}, Current: {data.data}")
        detect_value = data.data  # detect_valueを更新
        prev_detect_value = detect_value  # 前回値も更新



def yaw_callback(data):
    global yaw_value,first_yaw_value
    if yaw_value is None:
       yaw_value = data.data
       first_yaw_value = data.data
       print("first_yaw_value:",first_yaw_value)
    yaw_value = data.data
    print("yaw_value:",yaw_value)






rospy.init_node('detection_listener')
rospy.Subscriber('yaw', Float64, yaw_callback)
rospy.Subscriber('detect', Float64, detect_callback)
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
print("start!")
print("#####################################################")

twist = Twist()

twist.linear.x = 0
twist.angular.z = 0 

yaw_value = None
detect_value = None
rospy.spin()
