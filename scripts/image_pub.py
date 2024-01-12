#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

def publish_image():
    rospy.init_node('image_publisher', anonymous=True)
    image_pub = rospy.Publisher('image_topic', Image, queue_size=10)
    bridge = CvBridge()
    rate = rospy.Rate(10)  # パブリッシュの周波数を設定（10Hz）

    while not rospy.is_shutdown():
        try:
            # 画像を読み込む
            image = cv2.imread('/home/galleria/raspicat_ws/src/detect/scripts/data/IMG_5794.JPG')
            image = cv2.resize(image, dsize=(1008,756)) 
            #image = cv2.resize(image, dsize=(1024,1024))
            # OpenCVの画像形式をROSのイメージメッセージに変換
            ros_image = bridge.cv2_to_imgmsg(image, encoding='bgr8')
            
            # 画像をパブリッシュ
            image_pub.publish(ros_image)
        except Exception as e:
            rospy.logerr('Error publishing image: {}'.format(str(e)))

        rate.sleep()

if __name__ == '__main__':
    try:
        publish_image()
    except rospy.ROSInterruptException:
        pass
