# Autonomous Mobile Robot (Diff-Drive)
 - [BharatFIH](https://www.bharatfih.com/) (a Foxconn Technology Group Company) Collaborated Autonomous Mobile Robot for Material Handling during electrical assembly
 - Differential Drive Robot driven by BLDC Motors and Additional External Incremental Encoders for Odometry Feedback.
 - Additional IMU MPU-9250 for better yaw feedback filtered using ekf.
 - Within the core of the Robot is a NVIDIA Jetson Xavier AGX computing the whole process.
 - Completed Full Autonomous navigation using DWA Planner during an Internship Period of 1 month (HW and Simulation).

## 1. Designing the URDF for our mobile robot:
<p align="center">
<img src="https://github.com/yasvanth-s/amr_diff_bfih/assets/URDF.gif"
</p>
 
 - Simple description of our robot's dimensional Properties using default box and cirlces.
 - Added Required plugins in .gazebo for simulation requirements.
 
 ## 2. Creating a experimental gazebo environment and mapping(with ref. to Physical environment):
 
 - Using Gmapping to map the simulation environment.
<p align="center">
<img src="https://github.com/yasvanth-s/amr_diff_bfih/assets/mapping.gif"
</p> 
