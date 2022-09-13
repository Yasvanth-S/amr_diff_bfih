#!/usr/bin/python

import rospy
import Jetson.GPIO as GPIO
from geometry_msgs.msg import Twist


# Common PWM Channel
motor_pwm = 18

# Motor Left

l_brake = 11
l_direction = 19

# Motor Right

r_brake = 21
r_direction = 23

GPIO.setmode(GPIO.BOARD)
# HIGH - CW/FORWARD , LOW - CCW/REVERSE
GPIO.setup(l_direction, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(l_brake, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(r_brake, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(r_direction, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(motor_pwm, GPIO.OUT)
speed = GPIO.PWM(motor_pwm, 100)
speed.start(0)


class velocity_pwm:
    def __init__(self):
        rospy.init_node("velocity_to_pwm")
        self.vel_sub = rospy.Subscriber("/cmd_vel", Twist, self.vel_callback)
        self.x = 0
        self.z = 0
        self.max_vel = 7.77  # 100 Duty Cycle 7.77 m/s

    def calc_dutycycle(self, velocity):
        self.duty_cycle = velocity / self.max_vel * 100
        return self.duty_cycle

    def vel_callback(self, msg):
        self.x = msg.linear.x
        self.z = msg.angular.z

        if self.x == 0 and self.z == 0:
            GPIO.output(r_brake, GPIO.HIGH)
            GPIO.output(l_brake, GPIO.HIGH)
            print("BRAKE ENABLED")

        if self.x != 0 and self.x > 0:
            GPIO.output(r_brake, GPIO.LOW)
            GPIO.output(l_brake, GPIO.LOW)
            GPIO.output(l_direction, GPIO.HIGH)
            GPIO.output(r_direction, GPIO.LOW)
            speed.ChangeDutyCycle(self.calc_dutycycle(self.x))
            print(self.calc_dutycycle(self.x))
            print("FORWARD")
        elif self.x != 0 and self.x < 0:
            GPIO.output(r_brake, GPIO.LOW)
            GPIO.output(l_brake, GPIO.LOW)
            GPIO.output(l_direction, GPIO.LOW)
            GPIO.output(r_direction, GPIO.HIGH)
            speed.ChangeDutyCycle(self.calc_dutycycle((self.x*(-1))))
            print(self.calc_dutycycle((self.x*(-1))))
            print("REVERSE")

        if self.z != 0 and self.z > 0:
            GPIO.output(r_brake, GPIO.LOW)
            GPIO.output(l_brake, GPIO.LOW)
            GPIO.output(l_direction, GPIO.HIGH)
            GPIO.output(r_direction, GPIO.HIGH)
            speed.ChangeDutyCycle(self.calc_dutycycle(self.z))
            print(self.calc_dutycycle(self.z))
            print("LEFT")
        elif self.z != 0 and self.z < 0:
            GPIO.output(r_brake, GPIO.LOW)
            GPIO.output(l_brake, GPIO.LOW)
            GPIO.output(l_direction, GPIO.LOW)
            GPIO.output(r_direction, GPIO.LOW)
            speed.ChangeDutyCycle(self.calc_dutycycle((self.z*(-1))))
            print(self.calc_dutycycle((self.z*(-1))))
            print("RIGHT")
if __name__ == '__main__':
    try:
        velocity_pwm()
        rospy.spin()
    except:
        rospy.ROSInterruptException
    pass


