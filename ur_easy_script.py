import socket
from urx.urscript import URScript
from urx import Robot
import time

def pop2(arr, i1, i2):
    i1_new = i1
    i2_new = i2
    if i1 > i2:
        i1_new = i2
        i2_new = i1
    arr_copy = arr.copy() 
    arr_copy.pop(i1_new)
    arr_copy.pop(i2_new-1)
    return arr_copy

class FakeRobot():
    def __init__(self):
        print("Using fake robot")
        self.host = "FAKEHOST"
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


    def __del__(self):
        self.robot.close()


    def disconnect(self):
        self.robot.close()

    
    def _clean_script(self):

        script_str = self.urscript()
        lines = script_str.strip().split("\n")[1:-1]
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
                for i in range(i, i+3):
                    skip.append(i)
        
        # lines which are to be added to a URScript object
        lines_new = [lines[i] for i in range(len(lines)) if i not in skip]

        # open the socket at the start and close it at the end
        topop = []
        for i,v in enumerate(lines_new):
            if "socket_open" in v:
                topop.append(i)
            elif "socket_close" in v:
                topop.append(i)
        if len(topop) == 2:
            lines_new = pop2(lines_new, topop[0], topop[1])
        lines_new.insert(0, f'socket_open("{self.socket_host}", {self.socket_port}, "{self.socket_name}")')
        lines_new.append(f'socket_close("{self.socket_name}")')

        # Create a new urscript with shadowed variable assignments removed
        urscript = URScript()
        for n in lines_new:
            urscript.add_line_to_program(n)

        self.urscript = urscript


    def send(self):
        self._clean_script()
        if isinstance(self.robot, FakeRobot):
            print("Sending...")
            print(self.urscript())
        else:
            self.robot.send_program(self.urscript())


    def set_variable(self, variable, value):
        msg = f"global {variable}={value}" 
        self.urscript.add_line_to_program(msg)
        self.urscript._socket_send_string(f'{variable}={value}', self.socket_name)


    def send_script_from_file(self, script_path):
        with open(script_path, "r") as f:
            file_string = f.read()
        print(f"Sending the following script to the robot\n{file_string}\n")
        self.robot.send_program(file_string)
        print("\nSent!")


    def info(self):
        print("\n------------INFO---------------")
        print(f"Robot host: {self.robot.host}")
        print(f"Socket host: {self.socket_host}")
        print(f"Socket port: {self.socket_port}")
        print(f"Socket name: {self.socket_name}\n")
        print(f"URScript:\n{self.urscript()}")


