## Project Workflow

This project implements a complete **autonomous mobile robot navigation pipeline** using the ROS 2 Navigation (Nav2) framework. The robot first constructs a 2D occupancy grid map of the environment, localizes itself within the generated map, computes a collision-free global path, and continuously generates safe local trajectories while navigating around static obstacles and moving pedestrians.

The complete workflow consists of the following stages.

---

## 1. Simulation Environment Setup

A dynamic indoor cafe environment was created in Gazebo using **ROS 2 Jazzy**. The simulation replicates a realistic indoor public space where the robot must safely navigate while interacting with static furniture and moving pedestrians.

The environment includes:

* TurtleBot3 Burger mobile robot
* Gazebo simulation environment
* Tables, chairs, walls, and furniture
* Moving pedestrian actors
* 2D LiDAR sensor
* RViz2 visualization
* ROS 2 Nav2 navigation stack

The environment provides a realistic benchmark for evaluating human-aware navigation algorithms.

### Cafe Environment

![Cafe Environment](Cafe%20Environment.png)

---

## 2. Occupancy Grid Map Generation

Before autonomous navigation can begin, the robot must first build a representation of its surroundings.

The TurtleBot3 Burger was manually driven throughout the cafe using keyboard teleoperation while continuously collecting LiDAR laser scan data.

Using these scans, the GMapping-based mapping pipeline generated a **2D occupancy grid map**, which classifies the environment into:

* Occupied regions
* Free space
* Unknown space

The generated occupancy grid map serves as the reference map for localization and autonomous navigation.

### Generated Occupancy Grid Map

![Generated Map](Generated%20Map.png)

---

## 3. Robot Localization

Once the occupancy grid map was created, the robot estimated its pose using **Adaptive Monte Carlo Localization (AMCL)**.

AMCL continuously compares incoming LiDAR scans with the stored occupancy grid map and estimates the robot pose by maintaining a particle filter.

The localization process estimates:

* Robot X position
* Robot Y position
* Robot orientation (Yaw)

Accurate localization is essential because all subsequent planning and navigation decisions depend on the robot's estimated pose within the map.

---

## 4. Static Navigation Verification

Before introducing moving pedestrians, the complete Nav2 navigation pipeline was validated in a static environment.

The following navigation components were verified:

* Map Server
* AMCL Localization
* NavFn Global Planner
* Controller Server
* Behavior Tree Navigator
* Goal execution through RViz

Multiple navigation goals were assigned to confirm that the robot could successfully follow planned paths and accurately reach target locations.

### Static Navigation

![Static Navigation](Static%20Navigation.png)

---

## 5. Dynamic Human-Aware Navigation

After successful validation, moving pedestrians were enabled within the cafe environment.

During navigation, the robot continuously executes the following perception and planning cycle:

1. Acquire LiDAR measurements
2. Update the local costmap
3. Detect nearby dynamic and static obstacles
4. Recompute local trajectories
5. Generate safe velocity commands
6. Continue progressing toward the navigation goal

Unlike static navigation, dynamic navigation requires continuous trajectory replanning because pedestrian motion constantly changes the environment around the robot.

### Dynamic Navigation

![Dynamic Navigation](Dynamic%20Navigation.png)

---

## 6. Local Planner Comparison

The primary objective of this project was to evaluate the performance of two Nav2 local planners while keeping every other navigation component unchanged.

The same robot, map, localization system, global planner, and environment were used for both experiments.

---

### Configuration 1 — NavFn + MPPI Controller

The **Model Predictive Path Integral (MPPI)** controller generates hundreds of candidate trajectories at every control cycle and evaluates each trajectory using a cost function.

The cost function considers:

* Distance from obstacles
* Goal tracking
* Path following accuracy
* Motion smoothness
* Control effort

The trajectory with the minimum overall cost is selected to generate robot velocity commands.

#### Observed Characteristics

* Smooth robot motion
* Stable trajectory generation
* Effective pedestrian avoidance
* Conservative behavior in crowded environments
* Increased navigation time in highly cluttered areas

---

### Configuration 2 — NavFn + DWB Controller

The **Dynamic Window Approach (DWB)** evaluates multiple feasible velocity commands based on the robot's dynamic constraints.

Each candidate trajectory is scored using several navigation critics, including:

* Goal distance
* Obstacle distance
* Path alignment
* Heading alignment
* Rotation behavior

The highest-scoring trajectory is selected for execution.

#### Observed Characteristics

* Faster trajectory computation
* Efficient path following
* More direct navigation
* Greater dependence on critic parameter tuning

### DWB Navigation

![DWB Result](DWB%20Result.png)

---

## 7. Navigation in Cluttered Environments

To further evaluate controller robustness, additional cylindrical and cuboid obstacles were manually inserted into the cafe environment.

These obstacles reduced the available free space and forced both controllers to generate more complex avoidance trajectories while maintaining safe navigation.

This experiment provided additional insight into controller behavior under increasingly constrained environments.

### Additional Obstacles

![Additional Obstacles](Additional%20Obstacles.png)

---

## 8. Performance Evaluation

A custom Python-based metrics logger was developed to quantitatively evaluate navigation performance.

The following metrics were recorded for each navigation experiment:

* Total navigation time
* Total path length
* Minimum obstacle distance
* Number of close encounters

These metrics were combined with RViz and Gazebo observations to compare navigation efficiency, obstacle avoidance capability, and overall controller behavior.

### Performance Metrics

![Performance Metrics](Performance%20Metrics.png)

---

## Results Summary

Both controller configurations successfully completed all navigation experiments.

### MPPI Controller

The MPPI controller generated smoother trajectories and demonstrated better adaptation to moving pedestrians. It maintained larger safety margins around obstacles but generally required longer navigation times due to more conservative local planning.

### DWB Controller

The DWB controller produced more direct trajectories and lower computational overhead. However, its navigation behavior was more sensitive to critic parameter tuning, particularly in crowded environments with dynamic obstacles.

### Overall Findings

The experiments demonstrate that local planner selection significantly influences:

* Navigation efficiency
* Path smoothness
* Human-aware obstacle avoidance
* Safety margins around pedestrians
* Robot behavior in cluttered indoor environments

The comparison highlights the trade-offs between computational efficiency, trajectory smoothness, and dynamic obstacle avoidance when deploying autonomous mobile robots in human-populated environments.
