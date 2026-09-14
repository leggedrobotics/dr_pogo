#!/bin/bash
# ROS 2 Jazzy lives in the radarsplat conda env of the base image
# (rslethz/fognav:radarsplat-jetson), not under /opt/ros.
set -e
source /opt/conda/etc/profile.d/conda.sh
conda activate radarsplat
source /ws/install/setup.bash
exec "$@"
