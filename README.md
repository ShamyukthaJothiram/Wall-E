# **Project Wall-E - An Autonomous Load Carrier Robot**

## **Architecture**

### **1. Sensor Layer**

The vehicle is equipped with three primary sensors:

- **Camera (Lane+Object Detection)**  : Detects lanes, road edges, obstacles and visual cues using computer vision.

- **LiDAR (Point Cloud Data)**        : Provides three-dimensional spatial perception of the surroundings, enabling accurate detection of obstacles and free space.

- **GPS**                           : Supplies global positioning and heading information for localization in outdoor environments.

<br>

### **2. Sensor Fusion**
   
The raw data streams from the camera, LiDAR, and GPS are combined through a sensor fusion framework. This step mitigates the limitations of individual sensors and produces a consistent, reliable representation of the vehicle’s environment and current state.

<br>

### **3. SLAM (Simultaneous Localization and Mapping)**
   
The fused data is used to perform SLAM, which enables the vehicle to:

- Construct a dynamic map of the environment.

- Continuously estimate its own position within that map.

SLAM ensures reliable operation near buildings and supports real-time updates as the vehicle encounters new obstacles or changes in the environment.

<br>

### **4. Path Planning**
   
Based on the SLAM output, the path planning module generates an optimal trajectory for reaching the target destination while ensuring collision avoidance and efficient navigation.

The planner continuously evaluates updated environmental information and adapts the path in real time to account for dynamic changes such as moving obstacles or altered routes.

SLAM updates are continuously shared with the path planner to enable re-planning when necessary.

<br>

### **5. Motor Control**
   
The path planner’s commands are translated into actionable control signals by the motor control system. 

This subsystem handles:

1. Speed regulation.

2. Steering adjustments.

3. Execution of motion commands with precise timing.








