#include <ArduinoHardware.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int32.h>
#include <std_msgs/UInt32.h>

//right motor
int BRK_right = 30; 
int ZF_right = 31; //Direction CW=High, CCW=Low
int encoder_r_a = 2;
int encoder_r_b = 3;
int VR_Speed_right = 8;

//left motor
int BRK_left = 32; 
int ZF_left = 33; //Direction CW=High, CCW=Low
int encoder_l_a = 18;
int encoder_l_b = 19;
int VR_Speed_left = 9;

//encoder left
volatile int lastEncoded_l = 0;
volatile long encoderValue_l = 0;
long lastencoderValue_l = 0;
int lastMSB_l = 0;
int lastLSB_l = 0;

//encoder right
volatile int lastEncoded_r = 0;
volatile long encoderValue_r = 0;
long lastencoderValue_r = 0;
int lastMSB_r = 0;
int lastLSB_r = 0;


//int sp;

double w_r=0, w_l=0;
//wheel_rad is the wheel radius ,wheel_sep is
double wheel_rad = 7.7, wheel_sep = 0.47;
ros::NodeHandle nh;
int lowSpeed = 200;
int highSpeed = 50;
double speed_ang=0, speed_lin=0;



void updateEncoder_l(){
  int MSB_l = digitalRead(encoder_l_a); 
  int LSB_l = digitalRead(encoder_l_b); 
  int encoded_l = (MSB_l << 1) |LSB_l;
  int sum_l  = (lastEncoded_l << 2) | encoded_l; 

  if(sum_l == 0b1101 || sum_l == 0b0100 || sum_l == 0b0010 || sum_l == 0b1011) encoderValue_l --;
  if(sum_l == 0b1110 || sum_l == 0b0111 || sum_l == 0b0001 || sum_l == 0b1000) encoderValue_l ++;
  lastEncoded_l = encoded_l; 
}

void updateEncoder_r(){
  int MSB = digitalRead(encoder_r_a); 
  int LSB = digitalRead(encoder_r_b); 
  
  int encoded = (MSB << 1) |LSB;
  int sum  = (lastEncoded_r << 2) | encoded; 

  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderValue_r --;
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderValue_r ++;
  lastEncoded_r = encoded; 
}



void messageCb( const geometry_msgs::Twist& msg){
  speed_ang = msg.angular.z;
  speed_lin = msg.linear.x;
  w_r = (speed_lin/wheel_rad) + ((speed_ang*wheel_sep)/wheel_rad);
  w_l = (speed_lin/wheel_rad) - ((wheel_sep*speed_ang)/wheel_rad);
}


std_msgs::Int32 left_msg;
ros::Publisher leftpub("left_encoder", &left_msg);

std_msgs::Int32 right_msg;
ros::Publisher rightpub("right_encoder", &right_msg);

ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", &messageCb );
void Motors_init();
void MotorL(int Pulse_Width1);
void MotorR(int Pulse_Width2);
void setup(){
 Serial.begin(57600);
 Motors_init();
 nh.initNode();
 nh.subscribe(sub);
  nh.advertise(leftpub);
  nh.advertise(rightpub);
}
void loop(){
 MotorL(w_l*255);
 MotorR(w_r*255);

 right_msg.data = encoderValue_r;
 left_msg.data = encoderValue_l;
 leftpub.publish( &left_msg );
 rightpub.publish( &right_msg );
   Serial.println("w_r=");
  Serial.println(w_r);

 Serial.print("Left:");
 Serial.println(encoderValue_l);
 Serial.print("Right:");
 Serial.println(encoderValue_r);
 nh.spinOnce();
 
 delay(10);

}
void Motors_init(){

  pinMode(BRK_right, OUTPUT);
  pinMode(ZF_right, OUTPUT);
  pinMode(VR_Speed_right, OUTPUT);

  
  pinMode(BRK_left, OUTPUT);
  pinMode(ZF_left, OUTPUT);
  pinMode(VR_Speed_left, OUTPUT);
  

  pinMode(BRK_right,HIGH);

  pinMode(VR_Speed_right, LOW);

  
  pinMode(BRK_left, HIGH);

  pinMode(VR_Speed_left, LOW);

  //left
  pinMode(encoder_l_a, INPUT); 
  pinMode(encoder_l_b, INPUT);
  digitalWrite(encoder_l_a, HIGH);
  digitalWrite(encoder_l_b, HIGH);
  attachInterrupt(4, updateEncoder_l, CHANGE); 
  attachInterrupt(5, updateEncoder_l, CHANGE);

  //right
  pinMode(encoder_r_a, INPUT); 
  pinMode(encoder_r_b, INPUT);
  digitalWrite(encoder_r_a, HIGH);
  digitalWrite(encoder_r_b, HIGH);
  attachInterrupt(0, updateEncoder_r, CHANGE); 
  attachInterrupt(1, updateEncoder_r, CHANGE);
}

void MotorR(int Pulse_Width1){

   nh.spinOnce();
   Serial.println(Pulse_Width1);

 if (Pulse_Width1 > 0){
  
   digitalWrite(BRK_right, LOW); 
     digitalWrite(ZF_right, LOW);
     analogWrite(VR_Speed_right, Pulse_Width1);

   nh.spinOnce();

 }
 if (Pulse_Width1 < 0){
     Pulse_Width1=abs(Pulse_Width1);

   digitalWrite(BRK_right, LOW); 
     digitalWrite(ZF_right, HIGH);
     analogWrite(VR_Speed_right, Pulse_Width1);

   nh.spinOnce();


 }
 else if (Pulse_Width1 == 0){

   digitalWrite(BRK_right, HIGH); 
     digitalWrite(ZF_right, LOW);
     analogWrite(VR_Speed_right, Pulse_Width1);

   nh.spinOnce();


 }
}


void MotorL(int Pulse_Width2){
 nh.spinOnce();

 if (Pulse_Width2 > 0){
  
     digitalWrite(BRK_left, LOW);
     digitalWrite(ZF_left, HIGH);
     analogWrite(VR_Speed_left, Pulse_Width2);

   nh.spinOnce();



 }
 if (Pulse_Width2 < 0){
     Pulse_Width2=abs(Pulse_Width2);
     digitalWrite(BRK_left, LOW);
     digitalWrite(ZF_left, LOW);
     analogWrite(VR_Speed_left, Pulse_Width2);

   nh.spinOnce();

   


 }
 else if (Pulse_Width2 == 0){
     analogWrite(VR_Speed_left, Pulse_Width2);
    digitalWrite(BRK_left, HIGH);
     digitalWrite(ZF_left, LOW);

        nh.spinOnce();

 }
}
