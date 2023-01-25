#!/usr/bin/python3

import rospy
from move_base_sequence.srv import *

switch_state = 0

status_service = rospy.ServiceProxy('/move_base_sequence/get_state', get_state)
start_service = rospy.ServiceProxy('/move_base_sequence/set_state', set_state)
reset_service = rospy.ServiceProxy('/move_base_sequence/reset', reset)

if __name__ == "__main__":

    rospy.init_node('Mode_selection_node')


    while not rospy.is_shutdown():

            while(1): #Check switch state

                # switch_state = int(input("Enter Value: "))

                rospy.set_param('/move_base_sequence/is_repeating', False)

                #Manual Mode
                if switch_state == 1:

                    status = status_service()
                    if(str(status) != 'state: "Paused"'):
                        print("Teleop Mode")
                        start_service(False)


                #Automatic Mode
                if switch_state == 0:
                    reset_service()
                    status = status_service()
                    if(str(status) != 'state: "operating"'):
                        print("Automatic Mode")
                        start_service(True)

                rospy.set_param('/move_base_sequence/is_repeating', True)

            rospy.spin()