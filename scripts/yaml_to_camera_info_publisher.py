#!/usr/bin/env python
"""
pointgrey_camera_driver (at least the version installed with apt-get) doesn't
properly handle camera info in indigo.
This node is a work-around that will read in a camera calibration .yaml
file (as created by the cameracalibrator.py in the camera_calibration pkg),
convert it to a valid sensor_msgs/CameraInfo message, and publish it on a
topic.
The yaml parsing is courtesy ROS-user Stephan:
    http://answers.ros.org/question/33929/camera-calibration-parser-in-python/
This file just extends that parser into a rosnode.
"""
import rospy
import yaml
from sensor_msgs.msg import CameraInfo

def yaml_to_CameraInfo(yaml_fname):
    """
    Parse a yaml file containing camera calibration data (as produced by 
    rosrun camera_calibration cameracalibrator.py) into a 
    sensor_msgs/CameraInfo msg.
    
    Parameters
    ----------
    yaml_fname : str
        Path to yaml file containing camera calibration data
    Returns
    -------
    camera_info_msg : sensor_msgs.msg.CameraInfo
        A sensor_msgs.msg.CameraInfo message containing the camera calibration
        data
    """
    # Load data from file
    with open(yaml_fname, "r") as file_handle:
        calib_data = yaml.load(file_handle)
    # Parse
    camera_info_msg = CameraInfo()
    camera_info_msg.width = calib_data["image_width"]
    camera_info_msg.height = calib_data["image_height"]
    camera_info_msg.K = calib_data["camera_matrix"]["data"]
    camera_info_msg.D = calib_data["distortion_coefficients"]["data"]
    camera_info_msg.R = calib_data["rectification_matrix"]["data"]
    camera_info_msg.P = calib_data["projection_matrix"]["data"]
    camera_info_msg.distortion_model = calib_data["distortion_model"]
    return camera_info_msg

if __name__ == "__main__":
    # Initialize publisher node
    rospy.init_node("camera_info_publisher", anonymous=True)
    
    filename = rospy.get_param(rospy.get_name()+"/filename")
    cameraname = rospy.get_param(rospy.get_name()+"/cameraname")
    frame_id = rospy.get_param(rospy.get_name()+"/frame_id")
    # Parse yaml file
    camera_info_msg = yaml_to_CameraInfo(filename)

    publisher = rospy.Publisher(cameraname+"/camera_info", CameraInfo, queue_size=10)
    rate = rospy.Rate(15)

    # Run publisher
    while not rospy.is_shutdown():
        camera_info_msg.header.frame_id = frame_id
        camera_info_msg.header.stamp = rospy.Time.now()
        publisher.publish(camera_info_msg)
        rate.sleep()