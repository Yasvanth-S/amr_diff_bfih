#!/usr/bin/env python  
import rospy
import tf_conversions
import tf2_ros
import geometry_msgs.msg
from sensor_msgs.msg import Temperature, Imu

class tf_imu:
	def __init__(self):
		rospy.init_node('tf_broadcaster_imu')
    		rospy.Subscriber('/imu/data', Imu, self.handle_imu_pose)
    		self.t_next = rospy.Time.now()
    		self.then = rospy.Time.now()
		self.x = 0
		self.y = 0
		self.z = 0

	def handle_imu_pose(self,msg):
    		now = rospy.Time.now()
    		if now > self.t_next:
			elapsed = now - self.then
			then = now
			elapsed = elapsed.to_sec()
		br = tf2_ros.TransformBroadcaster()
		t = geometry_msgs.msg.TransformStamped()
		    
	    	t.header.stamp = rospy.Time.now()
		t.header.frame_id = "base_link"
		t.child_frame_id = "imu_link"
		self.x += msg.linear_acceleration.x
		self.y += msg.linear_acceleration.y
		self.z += msg.linear_acceleration.z
		t.transform.translation.x = 0
		t.transform.translation.y = 0
		t.transform.translation.z = 0
		t.transform.rotation.x = msg.orientation.x
		t.transform.rotation.y = msg.orientation.y
		t.transform.rotation.z = msg.orientation.z
		t.transform.rotation.w = msg.orientation.w

		br.sendTransform(t)

if __name__ == '__main__':
    tf_imu()
    rospy.spin()
