#!/usr/bin/env python3

import math
import csv
import signal
import sys
import time
import argparse

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class NavigationMetricsLogger(Node):
    def __init__(self, run_name):
        super().__init__('navigation_metrics_logger')

        self.run_name = run_name
        self.started = False
        self.start_time = None

        self.last_x = None
        self.last_y = None
        self.current_x = None
        self.current_y = None

        self.total_distance = 0.0

        self.closest_scan = float('inf')
        self.encounter_threshold = 1.0
        self.encounter_count = 0
        self.in_encounter = False

        self.rows = []

        self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)

        self.timer = self.create_timer(1.0, self.log_sample)

        self.get_logger().info("Metrics logger started")
        self.get_logger().info("Give the goal in RViz now")
        self.get_logger().info("Timer starts when robot first moves or cmd_vel becomes nonzero")
        self.get_logger().info("Press Ctrl+C after robot reaches or stops")

    def start_logger(self):
        if not self.started:
            self.started = True
            self.start_time = time.time()
            self.get_logger().info("Navigation timing started")

    def cmd_callback(self, msg):
        linear = abs(msg.linear.x)
        angular = abs(msg.angular.z)

        if linear > 0.001 or angular > 0.001:
            self.start_logger()

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        self.current_x = x
        self.current_y = y

        if self.last_x is not None and self.last_y is not None:
            dx = x - self.last_x
            dy = y - self.last_y
            step_dist = math.sqrt(dx * dx + dy * dy)

            if step_dist > 0.001:
                self.start_logger()
                if self.started:
                    self.total_distance += step_dist

        self.last_x = x
        self.last_y = y

    def scan_callback(self, msg):
        valid_ranges = []

        for r in msg.ranges:
            if math.isfinite(r) and msg.range_min < r < msg.range_max:
                valid_ranges.append(r)

        if not valid_ranges:
            return

        current_min = min(valid_ranges)

        if current_min < self.closest_scan:
            self.closest_scan = current_min

        if current_min < self.encounter_threshold and not self.in_encounter:
            self.encounter_count += 1
            self.in_encounter = True

        if current_min >= self.encounter_threshold:
            self.in_encounter = False

    def log_sample(self):
        if not self.started:
            return

        elapsed = time.time() - self.start_time

        x = self.current_x if self.current_x is not None else 0.0
        y = self.current_y if self.current_y is not None else 0.0
        closest = self.closest_scan if math.isfinite(self.closest_scan) else -1.0

        self.rows.append([
            round(elapsed, 3),
            round(x, 3),
            round(y, 3),
            round(self.total_distance, 3),
            round(closest, 3),
            self.encounter_count
        ])

    def save_results(self):
        if not self.started:
            print()
            print("Metrics logger stopped before robot moved.")
            print("No valid navigation metrics recorded.")
            print()
            return

        elapsed = time.time() - self.start_time
        csv_path = f'/tmp/{self.run_name}_nav_metrics.csv'

        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'time_sec',
                'robot_x',
                'robot_y',
                'path_distance_m',
                'closest_scan_distance_m',
                'encounters_below_1m'
            ])
            writer.writerows(self.rows)

        closest_print = self.closest_scan if math.isfinite(self.closest_scan) else -1.0

        print()
        print("FINAL NAVIGATION METRICS")
        print(f"Run name                  : {self.run_name}")
        print(f"Total navigation time     : {elapsed:.2f} sec")
        print(f"Robot path distance       : {self.total_distance:.2f} m")
        print(f"Encounters below 1.0 m    : {self.encounter_count}")
        print(f"Minimum scan distance     : {closest_print:.2f} m")
        print(f"CSV saved at              : {csv_path}")
        print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', default='nav_test')
    args = parser.parse_args()

    rclpy.init()
    node = NavigationMetricsLogger(args.run)

    def shutdown_handler(sig, frame):
        node.save_results()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.save_results()
    finally:
        try:
            node.destroy_node()
        except Exception:
            pass
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
