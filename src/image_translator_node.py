#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class ImageTranslatorNode:
    def __init__(self):
        rospy.init_node('image_translator_node', anonymous=True)
        self.bridge = CvBridge()
        self.translation_vector = np.array([-0.035, 0.039, -0.044])  # Vector de traslacion
        self.image_sub = rospy.Subscriber('/maqui/camera/front/image_raw', Image, self.image_callback)
        self.image_pub = rospy.Publisher('/maqui/camera/front_aligned_to_depth/image_raw', Image, queue_size=10)

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        translated_image = self.translate_image(cv_image, self.translation_vector)
        translated_msg = self.bridge.cv2_to_imgmsg(translated_image,'bgr8')
        self.image_pub.publish(translated_msg)

    def translate_image(self, image, translation_vector):
        rows, cols, _ = image.shape
        translation_matrix = np.float32([[1, 0, translation_vector[0]],
                                         [0, 1, translation_vector[1]]])
        translated_image = cv2.warpAffine(image, translation_matrix, (cols, rows))
        return translated_image

if __name__ == '__main__':
    image_translator = ImageTranslatorNode()
    rospy.spin()
