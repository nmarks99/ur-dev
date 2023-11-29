
def wrap_with_open_close(urscript_str: str, socket_host, socket_port, socket_name) -> str:
    s = urscript_str.split("\n")
    s.insert(1, f'\tsocket_open("{socket_host}", {socket_port}, "{socket_name}")')
    s.insert(len(s)-1, f'\tsocket_close("{socket_name}")')
    # for i in s:
    #     print(i)

a = "def main():\n\tprint('hello world')\n\tprint('goodbye')\nend"
print(a)
print("\n")
wrap_with_open_close(a, "123.456.789.123", 12345, "sock")
