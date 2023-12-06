# For quick testing:
# $ python3
# $ from test_script_helper import *
# $ script.set_variable("my_var", 123)

from urx.urscript import URScript
from urx import Robot
from ur_easy_script import URScriptHelper

# Connect to robot
robot_host = "164.54.104.148"
robot = Robot(robot_host)
print("Connected!")

# Construct a URScriptHelper
pc_host = "164.54.104.7"
port = 31001
name = "ursocket0"
script = URScriptHelper(pc_host, port, name, robot)
