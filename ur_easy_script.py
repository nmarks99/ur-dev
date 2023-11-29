import socket
from urx.urscript import URScript
from urx import Robot
import time

def _clean_script(urscript: URScript) -> URScript:
    # Get a string of the urscript
    script_str = urscript()

    # split by newline and removing "def myProg():" and "end"
    lines = script_str.strip().split("\n")[1:-1]

    # remove spaces from indentation
    lines = [i.strip() for i in lines]

    # find the lines with global variable assignments
    var_dict = dict() # {var : lines where it is found}
    line_num = 0
    for line in lines:
        line = line.replace(" ", "")
        if "global" in line:
            eq_ind = line.find("=")
            var_str = line[len("global"):eq_ind]
            if var_str not in var_dict.keys():
                var_dict[var_str] = [line_num]
            else:
                var_dict[var_str].append(line_num)
        line_num += 1
    
    # get a list of the line we need to skip
    skip = []
    for ind_list in var_dict.values():
        ind_list_copy = ind_list.copy()
        ind_list_copy.pop(-1)
        for i in ind_list_copy:
            skip.append(i)
    
    # lines which are to be added to a URScript object
    lines_new = [lines[i] for i in range(len(lines)) if i not in skip]
    lines_new.insert(0, "TEST_START")
    lines_new.append("TEST_END")

    # Create a new urscript with shadowed variable assignments removed
    urscript = URScript()
    for n in lines_new:
        urscript.add_line_to_program(n)

    return urscript


class FakeRobot():
    def __init__(self):
        print("Using fake robot")
    def close(self):
        pass

class URScriptHelper():
    '''
    Provides and easy to use interface for sending URscript commands to
    a Univeral Robots robot arm
    '''

    def __init__(self, socket_host, socket_port, socket_name, robot):
        assert isinstance(robot, Robot) or robot is None
        assert isinstance(socket_host, str)
        assert isinstance(socket_port, str) or isinstance(socket_port, int)
        assert isinstance(socket_name, str)
        self.socket_host = socket_host
        self.socket_port = socket_port
        self.socket_name = socket_name
        self.urscript = URScript()
        if robot is None:
            self.robot = FakeRobot()
        else:
            self.robot = robot

        # Open TCP socket to PC
        # self.urscript._socket_close(self.socket_name)
        # self.urscript._socket_open(self.socket_host, self.socket_port, self.socket_name)
        # self.robot.send_program(self.urscript())
        # self.urscript.reset()

    def __del__(self):
        self.robot.close()

    def disconnect(self):
        self.robot.close()

    def send(self):
        if isinstance(self.robot, FakeRobot):
            self.urscript = _clean_script(self.urscript)
            print("Sending:")
            print(self.urscript())
        else:
            self.robot.send_program(self.urscript())

    def set_variable(self, variable, value):

        msg = f"global {variable}={value}" 
        self.urscript.add_line_to_program(msg)

        # self.urscript._socket_send_string(f"variables : to_str('{variable}')", self.socket_name)
        # print(f"Sending the following script to the robot\n{self.urscript()}\n")
        # self.urscript = _clean_script(self.urscript())
        # self.robot.send_program(self.urscript())
        # print("\nSent!")

    def socket_send_string(self, msg):
        self.urscript._socket_open(self.socket_host, self.socket_port, self.socket_name)
        self.urscript.add_line_to_program(f'socket_send_string("{msg}","{self.socket_name}")')
        self.urscript._socket_close(self.socket_name)
        self.robot.send_program(self.urscript())
        self.urscript.reset()

    def send_script_from_file(self, script_path):
        with open(script_path, "r") as f:
            file_string = f.read()
        print(f"Sending the following script to the robot\n{file_string}\n")
        self.robot.send_program(file_string)
        print("\nSent!")

    def info(self):
        print(f"Robot host: {self.robot.host}")
        print(f"Socket host: {self.socket_host}")
        print(f"Socket port: {self.socket_port}")
        print(f"Socket name: {self.socket_name}")


