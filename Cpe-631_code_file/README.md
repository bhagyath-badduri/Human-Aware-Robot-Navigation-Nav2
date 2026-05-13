CPE 631-A Final Project Code
Performance Evaluation of Nav2 Controllers for Human-Aware Indoor Robot Navigation

Author:
Bhagyath Badduri

Description:
This folder contains the configuration files and metrics logger used for the final project. The project compares two Nav2 navigation configurations in a simulated cafe environment:

1. NavFn global planner with MPPI local controller
2. NavFn global planner with DWB local controller

The same cafe map, TurtleBot3 Burger robot model, and pedestrian-enabled simulation environment were used for both configurations.

Files Included:
1. navfn_mppi_controller.yaml
   Nav2 parameter file for the NavFn planner with the MPPI controller.

2. navfn_dwb_controller.yaml
   Nav2 parameter file for the NavFn planner with the DWB controller.

3. nav_metrics_logger.py
   Python script used to record navigation performance metrics such as:
   - Total navigation time
   - Robot path distance
   - Minimum laser scan distance
   - Number of close encounters below the selected threshold

4. launch_commands.txt
   Contains the terminal commands used to launch static navigation, dynamic navigation, and the metrics logger.

How to Run:
1. Open a terminal and source ROS 2 and the workspace:

   source /opt/ros/jazzy/setup.bash
   source install/setup.bash
   export TURTLEBOT3_MODEL=burger
   export RMW_FASTRTPS_USE_SHM=0

2. Launch the navigation simulation using the commands provided in launch_commands.txt.

3. To run the MPPI configuration, use the NavFn with MPPI parameter file:

   navfn_mppi_controller.yaml

4. To run the DWB configuration, use the NavFn with DWB parameter file:

   navfn_dwb_controller.yaml

5. Start the metrics logger before assigning the navigation goal:

   python3 nav_metrics_logger.py --run navfn_mppi_test1

   Example run names:
   - navfn_mppi_test1
   - navfn_mppi_test2
   - navfn_dwb_test1
   - navfn_dwb_test2

6. In RViz, set the robot initial pose using 2D Pose Estimate and assign the navigation goal using 2D Goal Pose.

Output:
The metrics logger saves the recorded results as CSV files in the /tmp directory.

Example:
/tmp/nav_metrics.csv
/tmp/navfn_mppi_test1_nav_metrics.csv
/tmp/navfn_dwb_test1_nav_metrics.csv

Notes:
The cafe map should be loaded before navigation. Pedestrians are disabled for static navigation testing and enabled for dynamic navigation testing. The global planner was kept as NavFn for both configurations so that the comparison focused on the local controller behavior.