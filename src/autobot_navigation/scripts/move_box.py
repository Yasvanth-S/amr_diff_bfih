#! /usr/bin/python3

import rospy
import actionlib
from rospy.timer import sleep
from move_base_msgs.msg import MoveBaseAction
from move_base_msgs.msg import MoveBaseGoal
from move_base_msgs.msg import MoveBaseResult

pose = [[0, 0], [0, 0], [0, 0]]

from geometry_msgs.msg import PointStamped

global x,y,z

class pubPoints:
    def __init__(self):
        self.client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.point_sub = rospy.Subscriber('/clicked_point', PointStamped, self.callback)
        self.client.wait_for_server()
        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = 'map'
        self.i = 0
        self.collected_flag = 0


    def move_box(self, value):
        self.goal.target_pose.pose.position.x = pose[value][0]
        self.goal.target_pose.pose.position.y = pose[value][1]
        self.goal.target_pose.pose.position.z = 0.0
        self.goal.target_pose.pose.orientation.x = 0
        self.goal.target_pose.pose.orientation.y = 0
        self.goal.target_pose.pose.orientation.w = 0.2
        self.goal.target_pose.pose.orientation.z = 3.14
        self.client.send_goal(self.goal)
        self.client.wait_for_result()
        self.result = self.client.get_result()
        print("Goal Reached for point {}".format(value))

    def callback(self, msg): 
        rospy.loginfo("coordinates:x=%f y=%f" %(msg.point.x,msg.point.y))
        if self.i < 3:
            pose[self.i][0] = msg.point.x
            pose[self.i][1] = msg.point.y
            self.i = self.i + 1
            print("Input")
        if self.i == 3:
            print("Collected 3 points")
            print("First {}".format(pose[0]))
            print("Second {}".format(pose[1]))
            print("Third {}".format(pose[2]))
            for a in range(3):
                go = input("Move to Goal {} ?: ".format(a))
                if go == "y" or go == "Y":
                    self.move_box(a)
                else:
                    print("Goal abandoned")
            self.i = 0  #Resetting the Goal list
            print("Input Next 3 Goals - List Resetted")
        

if __name__ == "__main__":
    rospy.init_node("pub_points")
    pp = pubPoints()
    rospy.spin()


