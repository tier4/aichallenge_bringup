#!/usr/bin/env python
from geometry_msgs.msg import PoseWithCovarianceStamped
import rospy
import time

if __name__ == "__main__":
    # Initialize publisher node
    rospy.init_node("initial_pose_pub", anonymous=True)
    publisher = rospy.Publisher("initialpose", PoseWithCovarianceStamped, queue_size=1, latch=True)
    # Run publisher
    msg = PoseWithCovarianceStamped()
    msg.header.frame_id = "map"
    msg.pose.pose.position.x = 15.7058410645
    msg.pose.pose.position.y = 108.812957764
    msg.pose.pose.position.z = 0.0
    msg.pose.pose.orientation.x = 0.00282391965222
    msg.pose.pose.orientation.y = -0.0111912951505
    msg.pose.pose.orientation.z = -0.704921607798
    msg.pose.pose.orientation.w = 0.709191305114
    msg.pose.covariance[0] = 0.25
    msg.pose.covariance[7] = 0.25
    msg.pose.covariance[35] = 0.06853892326654787
    time.sleep(1)
    publisher.publish(msg)
    rospy.spin()