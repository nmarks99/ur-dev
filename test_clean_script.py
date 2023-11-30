from ur_easy_script import URScriptHelper
from urx.urscript import URScript

socket_host = "111.222.333.444"
socket_port = 12345
socket_name = "sock"
robot = None

s = URScriptHelper(socket_host, socket_port, socket_name, robot)

TEST = 3

if TEST == 1:
    s.set_variable("one", 0)
    s.set_variable("one", 1)
    s.set_variable("two", 2)
    s.set_variable("two", 3)
    print("Original: ")
    print(s.urscript())
    print("\n")
    s.send()

elif TEST == 2:
    s.set_variable("one", 111)
    s.send()

    s.set_variable("two", 222)
    s.send()

elif TEST == 3:
    s.enable_interpreter_mode()
    s.send(socket=False)

else:
    print(f"No test {TEST}")
