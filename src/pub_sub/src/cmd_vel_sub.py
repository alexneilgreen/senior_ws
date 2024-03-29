#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

# Use "catkin_create_pkg <folder name> rospy" in order to store publisher/subscribers
# Make sure to catkin_make and source enviornment
# Make sure to make file executable. Command "chmod +x <filename>"
# Within <ws/src> rosrun subscriber.py. EX "~/robot_gazebo/src$ rosrun tutorial subscriber.py"

class MotorController:
    def __init__(self):
        rospy.init_node('motor_controller', anonymous=True)
        rospy.Subscriber("/cmd_vel", Twist, self.cmd_vel_callback)
        self.model_state_pub = rospy.Publisher("/gazebo/set_model_state", ModelState, queue_size=10)
        self.model_state = ModelState()

    def cmd_vel_callback(self, msg):
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        # Assuming a skid steer drive model
        # Calculate the velocities for each wheel
        wheel_separation = 0.5  # Placeholder value, adjust according to your robot
        wheel_radius = 0.1  # Placeholder value, adjust according to your robot
        left_speed = (linear_x - angular_z * wheel_separation / 2) / wheel_radius
        right_speed = (linear_x + angular_z * wheel_separation / 2) / wheel_radius

        # Publish the motor speeds
        self.publish_motor_speeds(left_speed, right_speed)

    def publish_motor_speeds(self, left_speed, right_speed):
        # Move cursor to the beginning of the line and clear the entire line
        print("\r\x1b[K", end="", flush=True)
        
        # Publish the left and right speeds to the terminal
        print(f"Left Speed: {left_speed}, Right Speed: {right_speed}", end="", flush=True)

        # Publish the model state to control the robot in Gazebo
        self.model_state.model_name = "RAPID Robot"  # Adjust your robot's name
        self.model_state.twist.linear.x = left_speed  # Adjust according to your robot's configuration
        self.model_state.twist.linear.y = right_speed  # Adjust according to your robot's configuration

        # Publish the model state
        self.model_state_pub.publish(self.model_state)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        motor_controller = MotorController()
        motor_controller.run()
    except rospy.ROSInterruptException:
        pass
