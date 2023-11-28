from ursock import _clean_script, URScriptHelper
from urx.urscript import URScript

s = URScript()
s.add_line_to_program("global var=1")
s.add_line_to_program("global var=2")
s.add_line_to_program("global var=3")
s.add_line_to_program("global var=4")
s.add_line_to_program("socket_open()")
s.add_line_to_program("socket_send_string()")
s.add_line_to_program("socket_close()")
s.add_line_to_program("global var=4")

print("Orignal:")
print(s())

print("\nCleaned:")
clean = _clean_script(s)
print( clean() )
