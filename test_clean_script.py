from ur_easy_script import _clean_script, URScriptHelper
from urx.urscript import URScript

socket_host = "111.222.333.444"
socket_port = 12345
socket_name = "sock"
robot = None

s = URScriptHelper(socket_host, socket_port, socket_name, robot)
s.set_variable("var1", 0)
s.set_variable("var1", 1)
s.set_variable("var2", 2)
s.set_variable("var2", 3)

print("Original: ")
print(s.urscript())
print("\n")
# s.add_line_to_program("global var=1")
# s.add_line_to_program("global var=2")
# s.add_line_to_program("global var=3")
# s.add_line_to_program("global var=4")
# s.add_line_to_program("socket_open()")
# s.add_line_to_program("socket_send_string()")
# s.add_line_to_program("socket_close()")
# s.add_line_to_program("global var=4")

s.send()

# print("Orignal:")
# print(s())
#
# print("\nCleaned:")
# clean = _clean_script(s)
# print( clean() )

