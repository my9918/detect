#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float64
import numpy as np
import time
from geometry_msgs.msg import Twist
import tf
import math

def detect_callback(data):
    global detect_value,first_detect_value,first_yaw_value
    if detect_value is None:
       first_detect_value = data.data
    detect_value = data.data

    target_value = first_detect_value + first_yaw_value

    # target_valueが180度を超える場合の調整
    if target_value > 180:
        target_value -= 360

    # target_valueが-180度を超える場合の調整
    if target_value < -180:
        target_value += 360

    #print("目標の姿勢,現在の値:",target_value,yaw_value)
    #print("最初の姿勢:",first_yaw_value,"動いた角度",yaw_value - first_yaw_value)



    if detect_value > 0:
        print("左旋回")


        if first_yaw_value > 0 and target_value < 0:
            print("境界")#まず180まで旋回して残りの角度を計算
            
            speed = 25 #deg/s目的の速度
            twist.angular.z = speed * 3.1415 / 180.0 #rad
            pub.publish(twist)
            print("#####################################################")
            if yaw_value < 0:

                #print("\n-180から目標まで:",detect_value - (180 - first_yaw_value))#-180から目標まで
                #print("開始角度から180まで:",180 - first_yaw_value)#開始角度から180まで
                if target_value > yaw_value:
                    print("\n境界を超えました")
                else:
                    twist.angular.x = 0.0
                    twist.angular.z = 0.0
                    pub.publish(twist)
                    print("停止します")
                    #print("\n180 -first_yaw_value:",180 -first_yaw_value)#+側残りの角度
                    #print("yaw_value,180 -yaw_value:",yaw_value,180 + yaw_value)#ー側残りの角度
                    print("\n動いた角度:",(180 -first_yaw_value) + (180 + yaw_value))#動いた角度
                    move_value = (180 -first_yaw_value) + (180 + yaw_value)
                    if move_value > detect_value:
                        print("\n境界　目標値",detect_value,"度を超えました")
                    rospy.signal_shutdown("停止")


        else:
            print("通常")
            if target_value > yaw_value:
   

                speed = 25 #deg/s目的の速度
                twist.angular.z = speed * 3.1415 / 180.0 #rad
                pub.publish(twist)                
                print("#####################################################")
                
            else:#停止
                twist.angular.x = 0.0
                twist.angular.z = 0.0
                pub.publish(twist)
                print("停止します")
                move_value = yaw_value - first_yaw_value

                if move_value > detect_value:
                    print("\n通常 目標値",detect_value,"度を超えました")
                rospy.signal_shutdown("停止")            


    else:
        print("右旋回")

        if first_yaw_value < 0 and target_value > 0:
            print("境界")#まず180まで旋回して残りの角度を計算
            
            speed = -25 #deg/s目的の速度
            twist.angular.z = speed * 3.1415 / 180.0 #rad
            pub.publish(twist)
            print("#####################################################")
            if yaw_value > 0:

                #print("\n-180から目標まで:",detect_value - (180 - first_yaw_value))#-180から目標まで
                #print("開始角度から180まで:",180 - first_yaw_value)#開始角度から180まで
                if target_value < yaw_value:
                    print("\n境界を超えました")
                else:
                    twist.angular.x = 0.0
                    twist.angular.z = 0.0
                    pub.publish(twist)
                    print("停止します")
                    #print("\n180 + first_yaw_value:",(180 +first_yaw_value))#-側残りの角度
                    #print("yaw_value,180 -yaw_value:",yaw_value,180 - yaw_value)#+側残りの角度
                    print("\n動いた角度:",(180 +first_yaw_value) + (180 - yaw_value))#動いた角度
                    move_value = (180 + first_yaw_value) + (180 - yaw_value)
                    if move_value > detect_value:
                        print("\n境界　目標値",detect_value,"度を超えました")
                    rospy.signal_shutdown("停止")


        else:
            print("通常")
            if target_value < yaw_value:
   

                speed = -25 #deg/s目的の速度
                twist.angular.z = speed * 3.1415 / 180.0 #rad
                pub.publish(twist)                
                print("#####################################################")
                
            else:#停止
                twist.angular.x = 0.0
                twist.angular.z = 0.0
                pub.publish(twist)
                print("停止します")
                move_value = first_yaw_value - yaw_value
                print("\n動いた角度:",move_value)#動いた角度

                if move_value > detect_value:
                    print("\n通常 目標値",detect_value,"度を超えました")
                rospy.signal_shutdown("停止")            

      



def yaw_callback(data):
    global yaw_value,first_yaw_value
    if yaw_value is None:
       yaw_value = data.data
       first_yaw_value = yaw_value
       print("開始時点の姿勢:",first_yaw_value)
    yaw_value = data.data
    #print("現在の値:",yaw_value)






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
