#!/usr/bin/python

#REFERENCE CODE FROM ENCODER PRODUCT PAGE ROBU.IN ORANGE ROTORY ENCODER

import rospy
import Jetson.GPIO as GPIO

#Encoder Left

l_encoder_a = 31
l_encoder_b = 29

#Encoder Right

r_encoder_a = 36
r_encoder_b = 38


GPIO.setmode(GPIO.BOARD)


GPIO.setup(l_encoder_a, GPIO.IN)
GPIO.setup(l_encoder_b, GPIO.IN)
#GPIO.setup(l_encoder_b, GPIO.IN)
#GPIO.setup(r_encoder_b, GPIO.IN)

class encoder_value:
    def __init__(self):
        rospy.init_node("encoder_value")
        self.lastEncoded_l = 0
        self.encoderValue_l = 0
        self.lastEncoderValue = 0
        self.lastMSB = 0
        self.lastLSB = 0
        self.MSB_l = 0
        self.LSB_l = 0
	self.sum_l = 0
	self.encoded_l = 0
	print("NODE STARTED")
        #Setting interrupts
        GPIO.add_event_detect(l_encoder_a, GPIO.BOTH, callback=self.updateEncoder_l, bouncetime = 0)
        GPIO.add_event_detect(l_encoder_b, GPIO.BOTH, callback=self.updateEncoder_l, bouncetime = 0)
        #GPIO.add_event_detect(r_encoder_a, GPIO.BOTH, callback=self.updateEncoder_r, bouncetime=200)
        #GPIO.add_event_detect(r_encoder_b, GPIO.BOTH, callback=self.updateEncoder_r, bouncetime=200)
   
    def updateEncoder_l(self, channel):
        self.MSB_l = GPIO.input(l_encoder_a)
        self.LSB_l = GPIO.input(l_encoder_b)
        print("MSB = {}".format(self.MSB_l))
        print("LSB = {}".format(self.LSB_l))
	self.encoded_l = (self.MSB_l << 1) | self.LSB_l
	self.sum_l  = (self.lastEncoded_l << 2) | self.encoded_l
	print("SUM= {}".format(self.sum_l))
	#print("Before IF")
  	if (self.sum_l == 13) or (self.sum_l == 4) or (self.sum_l == 2) or (self.sum_l == 11):
		self.encoderValue_l+=1
		print("+")
  	if (self.sum_l == 14) or (self.sum_l == 7) or (self.sum_l == 1) or (self.sum_l == 8):
		self.encoderValue_l-=1
		print("-")
  	self.lastEncoded_l = self.encoded_l
	print(self.encoderValue_l)

    def updateEncoder_r(self, channel):
        print("Encoder R")


if __name__ == "__main__":
    try:
	encoder_value()
	rospy.spin()
    except:
        rospy.ROSInterruptException
	print("Exception")
	pass
