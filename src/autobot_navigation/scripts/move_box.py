#! /usr/bin/python3

import rospy
import actionlib
from rospy.timer import sleep
from move_base_msgs.msg import MoveBaseAction
from move_base_msgs.msg import MoveBaseGoal
from move_base_msgs.msg import MoveBaseResult

pose = [[0, 0, 0, 0], [0.3, -2.0, 1.54, 0.8], [0.1, 1.1, 3.14], [6.7, 1.4, 0]]


class pubPoints:
    def __init__(self):
        self.client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.client.wait_for_server()
        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = 'map'


    def move_box(self, value):
        self.goal.target_pose.pose.position.x = pose[value][0]
        self.goal.target_pose.pose.position.y = pose[value][1]
        self.goal.target_pose.pose.position.z = 0.0
        self.goal.target_pose.pose.orientation.x = 0
        self.goal.target_pose.pose.orientation.y = 0
        self.goal.target_pose.pose.orientation.z = pose[value][2]
        self.goal.target_pose.pose.orientation.w = pose[0][3]
        self.client.send_goal(self.goal)
        self.client.wait_for_result()
        self.result = self.client.get_result()
        print("Goal Reached for point {}".format(value))


if __name__ == "__main__":
    rospy.init_node("pub_points")
    pp = pubPoints()
    pp.move_box(1)
    pp.move_box(2)
    pp.move_box(3)
    rospy.spin()
