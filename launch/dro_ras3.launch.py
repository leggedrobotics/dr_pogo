"""DRO on the leggedrobotics B2W / Navtech RAS-3, headless.

Consumes the polar-frame pipeline directly (/radar_data/radar_frame) and the
robot IMU, and publishes dro_odom -> radar_link on /dro_odometry (so
holistic_fusion can give this source its own alignment state next to CFEAR's)
plus dro_odom -> base on /tf. Everything is a launch argument
so the compose service and a bag replay can override topics without editing.
"""
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    cfg = LaunchConfiguration
    default_config = PathJoinSubstitution(
        [FindPackageShare("dr_pogo"), "config", "config_dro_ras3.yaml"])
    return LaunchDescription([
        DeclareLaunchArgument("config_file", default_value=default_config),
        DeclareLaunchArgument("imu_topic", default_value="/imu_sensor_broadcaster/imu"),
        DeclareLaunchArgument("radar_frame_topic", default_value="/radar_data/radar_frame"),
        DeclareLaunchArgument("odom_frame_id", default_value="dro_odom"),
        DeclareLaunchArgument("child_frame_id", default_value="radar_link"),
        # odom_frame_id -> tf_body_frame on /tf, composed with the static
        # radar_link <- base mount from /tf_static (CFEAR's scheme). Set
        # publish_tf:=false when CFEAR is running with its own publish_tf, or
        # base gets two parents.
        DeclareLaunchArgument("publish_tf", default_value="true"),
        DeclareLaunchArgument("tf_body_frame", default_value="base"),
        DeclareLaunchArgument("output_path", default_value=os.path.join(os.sep, "tmp", "dro_output")),
        Node(
            package="dr_pogo",
            executable="dro_node",
            name="dro_node",
            output="screen",
            parameters=[{
                "input_mode": "radar_frame",
                "config_file": cfg("config_file"),
                "imu_topic": cfg("imu_topic"),
                "radar_frame_topic": cfg("radar_frame_topic"),
                "odom_frame_id": cfg("odom_frame_id"),
                "child_frame_id": cfg("child_frame_id"),
                "publish_tf": cfg("publish_tf"),
                "tf_body_frame": cfg("tf_body_frame"),
                "output_path": cfg("output_path"),
                "metadata_columns": 11,
                "encoder_size": 16000,
                "clockwise_radar": True,
                "chirp_down": True,
            }],
        ),
    ])
