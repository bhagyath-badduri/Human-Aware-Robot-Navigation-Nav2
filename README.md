# Human-Aware-Robot-Navigation-Nav2

ROS 2 Nav2 project comparing MPPI and DWB controllers for TurtleBot3 human-aware navigation in a dynamic cafe environment with moving pedestrians.

> **Note:** Please refer to the uploaded final project report (**Bhagyath final_report.pdf**) for complete implementation details, controller configurations, parameter settings, and experimental analysis.

---

# Performance Evaluation of Nav2 Controllers for Human-Aware Indoor Robot Navigation

This repository contains the final project work for **CPE 631-A: Cooperative Autonomous Mobile Robots** at **Stevens Institute of Technology**.

The project evaluates autonomous robot navigation in a simulated indoor cafe environment using **ROS 2 Jazzy**, **Gazebo**, **RViz**, **TurtleBot3 Burger**, and the **Nav2 Navigation Stack**. The objective is to compare the performance of **MPPI** and **DWB** local planners while navigating safely around static obstacles and moving pedestrians.

---

# Project Objective

Autonomous mobile robots operating in indoor human environments must safely reach a goal while avoiding walls, furniture, static obstacles, and moving pedestrians.

This project compares two controller configurations:

- **NavFn + MPPI Controller**
- **NavFn + DWB Controller**

The global planner (NavFn) remained unchanged while only the local controller was modified to evaluate navigation performance fairly.

---

# Simulation Environment

The project was carried out inside a simulated cafe environment containing static furniture and dynamic pedestrians.

![Cafe Environment](cafe_environment.png)

---

# Project Workflow

## 1. Environment Setup

- Configured ROS 2 Jazzy and Gazebo simulation
- Loaded TurtleBot3 Burger model
- Enabled pedestrian plugins to create a dynamic indoor environment

---

## 2. Mapping

The robot was manually teleoperated to generate a 2D occupancy grid map using LiDAR data.

The generated map was later reused for localization and autonomous navigation.

### Generated Occupancy Grid Map

![Generated Map](Generated%20Map.png)

---

## 3. Static Navigation Validation

Before enabling moving pedestrians, the generated map was loaded into Nav2.

AMCL localization, map server, planner server and controller server were verified by sending navigation goals from RViz.

### Static Navigation

![Static Navigation](Static%20Navigation.png)

---

## 4. Dynamic Navigation

After successful localization, pedestrians were enabled and the robot navigated through a dynamic cafe environment.

The robot continuously replanned its trajectory while avoiding moving people and static obstacles.

### Dynamic Navigation

![Dynamic Navigation](Dynamic%20Navigation.png)

---

## Navigation Configurations

### NavFn + MPPI Controller

The MPPI controller generates local trajectories by sampling multiple control sequences and selecting the trajectory with the minimum cost.

Advantages:

- Smooth trajectory generation
- Better obstacle avoidance
- Stable behavior around moving pedestrians

*(Representative navigation behavior can be found in the final report.)*

---

### NavFn + DWB Controller

The Dynamic Window Approach evaluates multiple velocity commands using trajectory critics and selects the optimal command.

Advantages:

- Fast local planning
- Efficient path following
- Lower computational complexity

### DWB Navigation Example

![DWB Result](DWB%20Result.png)

---

# Additional Obstacle Scenario

Besides the normal cafe environment, additional cylindrical and box obstacles were manually placed to increase navigation difficulty.

This allowed evaluation of controller robustness under more cluttered conditions.

![Additional Obstacles](Additional%20Obstacles.png)

---

# Performance Evaluation

Navigation performance was evaluated using a custom Python metrics logger.

The following metrics were recorded:

- Navigation Time
- Path Distance
- Minimum Obstacle Distance
- Number of Close Encounters

### Performance Metrics

![Performance Metrics](Performance%20Metrics.png)

---

# Results Summary

Both controller configurations successfully completed the navigation task.

### MPPI

- Produced smoother trajectories
- Better handled pedestrian interactions
- Required longer navigation time in cluttered environments due to conservative obstacle avoidance

### DWB

- Produced shorter paths in several scenarios
- More dependent on critic tuning
- Required careful parameter adjustment in crowded environments

Overall, the project demonstrates how the choice of local planner significantly influences:

- Navigation time
- Path smoothness
- Obstacle avoidance
- Human-aware navigation behavior

---

# Repository Structure

```text
Human-Aware-Robot-Navigation-Nav2/
│
├── README.md
├── Bhagyath final_report.pdf
│
├── Cpe-631_code_file/
│
├── Cafe Environment.png
├── Generated Map.png
├── Static Navigation.png
├── Dynamic Navigation.png
├── Additional Obstacles.png
├── DWB Result.png
├── Performance Metrics.png
│
└── LICENSE
