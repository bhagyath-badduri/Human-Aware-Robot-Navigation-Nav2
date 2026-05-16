# Human-Aware-Robot-Navigation-Nav2
ROS 2 Nav2 project comparing MPPI and DWB controllers for TurtleBot3 human-aware navigation in a dynamic cafe environment with moving pedestrians.
> **Note:** Please check the uploaded report for more details and results. Individual result screenshots are not uploaded separately in this repository. All figures, screenshots, metrics, and result analysis are included in the final report PDF.
# Performance Evaluation of Nav2 Controllers for Human-Aware Indoor Robot Navigation

This repository contains the final project work for **CPE 631-A: Cooperative Autonomous Mobile Robots** at **Stevens Institute of Technology**.

The project evaluates autonomous robot navigation in a simulated indoor cafe environment using **ROS 2 Jazzy**, **Gazebo**, **RViz**, **TurtleBot3 Burger**, and the **Nav2 navigation stack**. The main objective is to compare how two Nav2 local controller configurations perform when a robot navigates around static obstacles and moving pedestrians.

## Project Objective

Autonomous mobile robots operating in indoor human environments must reach a goal safely while avoiding walls, furniture, static obstacles, and moving people. In this project, a TurtleBot3 Burger robot was tested in a cafe simulation where pedestrians were enabled as dynamic obstacles.

The project compares two controller configurations:

1. **NavFn global planner with MPPI local controller**
2. **NavFn global planner with DWB local controller**

The NavFn global planner was kept the same for both configurations. Only the local controller was changed so that the effect of the local controller could be compared clearly.

## What Was Done

The project followed a complete ROS 2 Nav2 navigation workflow:

1. **Cafe environment setup**
   - A simulated cafe environment was launched in Gazebo.
   - TurtleBot3 Burger was used as the robot platform.
   - Pedestrians were enabled to create a dynamic human environment.

2. **Teleoperation and map construction**
   - The robot was manually driven using keyboard teleoperation.
   - Laser scan data was used to build the cafe occupancy grid map.
   - The generated map was saved and later reused for localization and navigation.

3. **Static navigation verification**
   - The saved cafe map was loaded using the Nav2 map server.
   - AMCL was used to localize the robot.
   - Pedestrians were disabled first.
   - A navigation goal was assigned in RViz to verify that the map, localization, planner, controller, and goal interface were working correctly.

4. **Dynamic navigation testing**
   - Pedestrians were enabled in the simulation.
   - The robot was tested in a dynamic cafe environment.
   - The same environment, robot model, map, and global planner were used for both controller configurations.

5. **Controller comparison**
   - NavFn with MPPI was tested first.
   - NavFn with DWB was tested next.
   - Each controller was tested in two cases:
     - Normal dynamic cafe environment
     - Dynamic cafe environment with additional manually placed obstacles

6. **Metrics collection**
   - A custom Python metrics logger was used.
   - The logger recorded navigation time, robot path distance, minimum scan distance, and close encounters below a selected threshold.

## Navigation Configurations

### NavFn with MPPI

In this configuration, NavFn generated the global path from the robot position to the goal. MPPI generated local velocity commands by sampling possible robot trajectories and selecting motion commands based on trajectory cost.

This configuration was useful for studying smooth local motion and obstacle response in a dynamic environment.

### NavFn with DWB

In this configuration, NavFn was again used as the global planner. The local controller was changed to DWB. DWB samples possible velocity commands and scores each trajectory using different critics such as path following, goal distance, obstacle distance, and rotation behavior.

This configuration was useful for comparing a trajectory-scoring local controller against the MPPI controller.

## Test Cases

Four total dynamic navigation tests were performed:

| Test | Configuration | Environment |
|---|---|---|
| Test 1 | NavFn + MPPI | Normal dynamic cafe environment |
| Test 2 | NavFn + MPPI | Dynamic cafe environment with added obstacles |
| Test 3 | NavFn + DWB | Normal dynamic cafe environment |
| Test 4 | NavFn + DWB | Dynamic cafe environment with added obstacles |

The additional obstacle tests included manually placed cylinders and cubes to reduce free space and make the navigation task more difficult.

## Performance Metrics

The following metrics were recorded for each navigation run:

| Metric | Description |
|---|---|
| Total navigation time | Time taken by the robot to complete the navigation task |
| Robot path distance | Total distance traveled by the robot |
| Minimum scan distance | Closest detected obstacle distance during the run |
| Close encounters | Number of times the robot came below the selected distance threshold |

These metrics were used together with RViz and Gazebo observations to understand the robot behavior.

## Results Summary

Both NavFn with MPPI and NavFn with DWB were able to complete the dynamic navigation tasks.

The MPPI controller showed smoother local motion and was able to react to dynamic pedestrians and added obstacles. However, in the more cluttered environment, the navigation time increased because the robot had to make more local adjustments.

The DWB controller also completed both test cases. It produced a more direct path in some cases, but its behavior depended strongly on trajectory scoring parameters and obstacle critic settings. In crowded regions, DWB required careful tuning to maintain safe and stable navigation behavior.

Overall, the results showed that local controller selection has a clear effect on path distance, navigation time, obstacle response, and robot behavior near pedestrians.

For detailed implementation steps, screenshots, terminal commands, performance results, and discussion, please refer to the final project report included in the `report/` folder.

## Repository Structure

```text
CPE631-Nav2-Controller-Comparison/
│
├── README.md
│
├── report/
│   └── Bhagyath_Cpe_631_final_report.pdf
│

│
├── config/
│   ├── nav2_dynamic_conservative_navfn_mppi.yaml
│   └── nav2_dynamic_conservative_navfn_dwb.yaml
│
├── scripts/
│   └── nav_metrics_logger.py
│
└── launch_commands.txt
