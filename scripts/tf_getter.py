#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import tf
from std_msgs.msg import Float64
import numpy as np
rospy.init_node('angle_listener')

listener = tf.TransformListener()
# 機体の座標系と親座標系を指定
child_frame_id = 'base_link'
parent_frame_id = 'odom'

pub = rospy.Publisher('yaw', Float64 , queue_size=1)

rate = rospy.Rate(10)
while not rospy.is_shutdown():
    try:
        # 機体の姿勢を取得
        (trans, rot) = listener.lookupTransform(parent_frame_id, child_frame_id, rospy.Time(0))
        # クオータニオンをオイラー角に変換
        roll, pitch, yaw = tf.transformations.euler_from_quaternion(rot)
        deg = np.rad2deg(yaw)
        a = deg
        pub.publish(a)
        rate.sleep()
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        continue