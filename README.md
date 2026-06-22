# Project Workflow

The project implements a complete autonomous mobile robot navigation pipeline in ROS 2. The robot first constructs an occupancy grid map of the environment, localizes itself within the map, plans a collision-free global path, and continuously computes safe local trajectories while navigating around moving pedestrians and static obstacles.

The complete workflow consists of the following stages.

---

## 1. Simulation Environment Setup

A dynamic indoor cafe environment was launched in Gazebo using ROS 2 Jazzy.

The simulation includes:

- TurtleBot3 Burger mobile robot
- Static obstacles such as tables, walls, and furniture
- Dynamic pedestrians acting as moving obstacles
- LiDAR sensor for environment perception
- RViz for visualization

The environment provides a realistic indoor navigation scenario where the robot must safely interact with both static and dynamic objects.

![Cafe Environment](cafe_environment.png)

---

## 2. Occupancy Grid Map Generation

Before autonomous navigation can begin, the robot must first understand its environment.

The TurtleBot3 was manually teleoperated through the cafe while continuously collecting LiDAR laser scan data.

Using the collected scan data, ROS generated a 2D occupancy grid map representing:

- Free space
- Occupied space
- Unknown regions

This map serves as the global representation of the environment and is later reused for localization and path planning.

### Generated Occupancy Grid Map

![Generated Map](generated_map.png)

---

## 3. Robot Localization

Once the occupancy grid map was generated, the robot used Adaptive Monte Carlo Localization (AMCL) to estimate its position inside the map.

AMCL continuously compares incoming LiDAR measurements with the previously generated occupancy grid map to estimate the robot's pose.

The localization process estimates:

- Robot x-position
- Robot y-position
- Robot heading (yaw)

Accurate localization is essential because both global planning and local navigation depend on knowing the robot's current pose.

---

## 4. Static Navigation Verification

Before introducing moving pedestrians, the navigation system was validated in a static environment.

The following Nav2 components were verified:

- Map Server
- AMCL Localization
- NavFn Global Planner
- Local Planner
- Behavior Tree Navigator
- Controller Server

Navigation goals were sent from RViz to confirm that the robot could successfully reach the desired location without dynamic obstacles.

### Static Navigation

![Static Navigation](static_navigation.png)

---

## 5. Dynamic Human-Aware Navigation

After successful validation, moving pedestrians were enabled inside the cafe environment.

During navigation the robot continuously performs the following operations:

1. Receive LiDAR measurements
2. Update the local costmap
3. Detect nearby obstacles
4. Replan local trajectories
5. Generate safe velocity commands
6. Continue toward the navigation goal

Unlike static navigation, the robot must continuously adapt its motion because pedestrians move unpredictably throughout the environment.

### Dynamic Navigation

![Dynamic Navigation](dynamic_navigation.png)

---

## 6. Local Planner Comparison

The main objective of this project was to compare two different Nav2 local planners while keeping all other navigation components unchanged.

### Configuration 1 — NavFn + MPPI

The MPPI (Model Predictive Path Integral) controller samples hundreds of possible future trajectories and evaluates each trajectory using multiple cost functions such as obstacle avoidance, path following, and goal tracking.

The trajectory with the minimum overall cost is selected to generate velocity commands.

Advantages observed during testing:

- Smooth robot motion
- Better obstacle avoidance
- More stable behavior around pedestrians
- Conservative navigation in crowded environments

---

### Configuration 2 — NavFn + DWB

The Dynamic Window Approach (DWB) controller evaluates multiple candidate velocity commands and scores each trajectory using several navigation critics.

These critics evaluate:

- Distance to goal
- Distance from obstacles
- Path alignment
- Rotation behavior

The highest scoring trajectory is selected for execution.

Advantages observed:

- Faster computation
- Efficient path following
- More direct trajectories

### DWB Navigation

![DWB Result](dwb_result.png)

---

## 7. Navigation in Cluttered Environments

To further evaluate controller robustness, additional cylindrical and cuboid obstacles were manually inserted into the environment.

These obstacles reduced the available free space and forced the local planners to generate more complex avoidance trajectories.

This experiment demonstrates controller performance under increasingly difficult navigation scenarios.

![Additional Obstacles](additional_obstacles.png)

---

## 8. Performance Evaluation

A custom Python-based metrics logger was developed to quantitatively compare both controllers.

The following performance metrics were recorded for every navigation experiment:

- Total navigation time
- Total path length
- Minimum obstacle distance
- Number of close encounters

These metrics were used to evaluate navigation efficiency, safety, and controller behavior.

### Performance Metrics

![Performance Metrics](performance_metrics.png)

---

## Results Summary

Both MPPI and DWB successfully completed all navigation tasks.

### MPPI

- Produced smoother trajectories
- Better handled moving pedestrians
- Generated safer obstacle avoidance behavior
- Required longer navigation time in highly cluttered environments due to conservative planning

### DWB

- Generated shorter paths in several scenarios
- Required careful critic parameter tuning
- Produced faster responses but exhibited less smooth motion in crowded environments

Overall, the project demonstrates how local planner selection significantly influences navigation performance in human-populated indoor environments. The comparison highlights the trade-offs between smoothness, computational efficiency, obstacle avoidance, and overall navigation safety.
