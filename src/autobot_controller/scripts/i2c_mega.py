#!/usr/bin/python
import smbus
import time

xavier_bus = smbus.SMBus(2)

mega_addr = 0x40

duty_cycle = 0
left_encoder = 0
right_encoder = 0

def writePWM(value):
    xavier_bus.write_byte(mega_addr, value)
    print("PWM Written")

def readEncoder_left():
    left_encoder = xavier_bus.read_byte(mega_addr)
    return left_encoder

def readEncoder_right():
    right_encoder = xavier_bus.read_byte(mega_addr)
    return right_encoder

def main():
    value = input("Enter Value: ")
    if value == 1:
        print("Enter PWM")
        duty_cycle = input("")
        writePWM(duty_cycle)
    if value == 2:
        temp = readEncoder_left()
        print(temp)
    if value == 3:
        temp1 = readEncoder_right()
        print(temp1)


if __name__ == "__main__":
    main()
