#!/usr/bin/python

#REFERENCE CODE FROM ENCODER PRODUCT PAGE ROBU.IN ORANGE ROTORY ENCODER

import rospy
import Jetson.GPIO as GPIO
from std_msgs.msg import Int32

#Encoder Left - Use only PULL-UP GPIO PINS!!!

l_encoder_a = 31
l_encoder_b = 29

#Encoder Right - Use only PULL-UP GPIO PINS!!!! 31,12,29
r_encoder_a = 7
r_encoder_b = 11


GPIO.setmode(GPIO.BOARD)


GPIO.setup(l_encoder_a, GPIO.IN)
GPIO.setup(l_encoder_b, GPIO.IN)
GPIO.setup(r_encoder_a, GPIO.IN)
GPIO.setup(r_encoder_b, GPIO.IN)

class encoder_value:
    def __init__(self):
        rospy.init_node("encoder_value")
        self.l_enc_pub = rospy.Publisher("left_encoder", Int32, queue_size=10)
	self.r_enc_pub = rospy.Publisher("right_encoder", Int32, queue_size=10)
	self.lastEncoded_l = 0
        self.encoderValue_l = 0 
        self.MSB_l = 0
        self.LSB_l = 0
	self.sum_l = 0
	self.encoded_l = 0
	#Right encoder
	self.lastEncoded_r = 0
        self.encoderValue_r = 0 
        self.MSB_r = 0
        self.LSB_r = 0
	self.sum_r = 0
	self.encoded_r = 0

	print("NODE STARTED")
        #Setting interrupts
        GPIO.add_event_detect(l_encoder_a, GPIO.BOTH, callback=self.updateEncoder_l, bouncetime = 0)
        GPIO.add_event_detect(l_encoder_b, GPIO.BOTH, callback=self.updateEncoder_l, bouncetime = 0)
        GPIO.add_event_detect(r_encoder_a, GPIO.BOTH, callback=self.updateEncoder_r, bouncetime = 0)
        GPIO.add_event_detect(r_encoder_b, GPIO.BOTH, callback=self.updateEncoder_r, bouncetime = 0)
   	
	#GPIO.add_event_detect(r_encoder_a, GPIO.BOTH)
	#if GPIO.event_detected(r_encoder_a):
	#	print("Hello")
    def updateEncoder_l(self, channel):
        self.MSB_l = GPIO.input(l_encoder_a)
        self.LSB_l = GPIO.input(l_encoder_b)
        print("Left MSB = {}".format(self.MSB_l))
        print("Left LSB = {}".format(self.LSB_l))
	self.encoded_l = (self.MSB_l << 1) | self.LSB_l
	self.sum_l  = (self.lastEncoded_l << 2) | self.encoded_l
	#print("SUM= {}".format(self.sum_l))
	#print("Before IF")
  	if (self.sum_l == 13) or (self.sum_l == 4) or (self.sum_l == 2) or (self.sum_l == 11):
		self.encoderValue_l+=1
		print("+")
  	if (self.sum_l == 14) or (self.sum_l == 7) or (self.sum_l == 1) or (self.sum_l == 8):
		self.encoderValue_l-=1
		print("-")
  	self.lastEncoded_l = self.encoded_l
	self.l_enc_pub.publish(self.encoderValue_l)

    def updateEncoder_r(self, channel):
	print("Inside function")
        self.MSB_r = GPIO.input(r_encoder_a)
        self.LSB_r = GPIO.input(r_encoder_b)
        print("Right MSB = {}".format(self.MSB_r))
        print("Right LSB = {}".format(self.LSB_r))
	self.encoded_r = (self.MSB_r << 1) | self.LSB_r
	self.sum_r  = (self.lastEncoded_r << 2) | self.encoded_r
	print("SUM= {}".format(self.sum_r))
	print("Before IF")
  	if (self.sum_r == 13) or (self.sum_r == 4) or (self.sum_r == 2) or (self.sum_r == 11):
		self.encoderValue_r+=1
		print("+")
  	if (self.sum_r == 14) or (self.sum_r == 7) or (self.sum_r == 1) or (self.sum_r == 8):
		self.encoderValue_r-=1
		print("-")
  	self.lastEncoded_r = self.encoded_r
	self.r_enc_pub.publish(self.encoderValue_r)


if __name__ == "__main__":
    try:
	encoder_value()
	rospy.spin()
    except:
        rospy.ROSInterruptException
	print("Exception")
	pass
