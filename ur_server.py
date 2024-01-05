#!./.venv/bin/python3
'''
A TCP server designed to connect EPICS PVs to a URScript running on the UR controller.

Run this program on the IOC's host machine and it listens for messages
of the form "GET pv" and "SET pv value". If a "GET" message is received,
the value of the corresponding PV in the given IOC is sent back on server.
If a "SET" message is received, the given value of the PV is set.

From the URScript program on the UR controller, first open the socket:
socket_open("HOST_IP", PORT)

To get the value of a PV:
my_pv = socket_get_var("my_pv")

To set the value of a PV:
socket_set_var("my_pv", 42)
'''

import socket
import argparse
from epics import caget, caput

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
PORT = 31111
BUFFER_SIZE = 1024
PREFIX = "8idgur3e"

parser = argparse.ArgumentParser(description='TCP server to connect EPICS to UR robot scripts')
parser.add_argument('--port', default=PORT, help='TCP port number')
parser.add_argument('--host', default=HOST, help='IP address')
parser.add_argument('--prefix', default=PREFIX, help='EPICS IOC prefix')
args = parser.parse_args()
HOST = args.host
PORT = args.port
PREFIX = args.prefix


def epics_handler(connection, data):
    data_recv = data.decode("ascii").strip().split(" ")
    cmd = data_recv[0]

    ok = True
    if cmd == "GET":
        if len(data_recv) == 2:
            var = data_recv[1]
            value = caget(f"{PREFIX}:{var}.VAL")
            if value is None:
                value = 0
                print(f"PV {var} not found. Sending {var}=0 to socket")
            reply = f"{var} {value}\n"
            connection.sendall(reply.encode("utf-8"))
        else:
            ok = False

    elif cmd == "SET":
        if len(data_recv) == 3:
            var = data_recv[1]
            val = data_recv[2]
            result = caput(f"{PREFIX}:{var}.VAL", val)
            if result is None:
                print(f"PV {var} not found. No action taken")
        else:
            ok = False

    else:
        ok = False

    if not ok:
        print(f"Invalid input received {data_recv}\nNo action taken.")


def main():
    count = 0
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen()
            while True:
                try: 
                    print("Waiting for connection...")
                    connection, address = sock.accept()
                    with connection:
                        print(f"[{count}] Connection opened on {address}")

                        while True:
                            data = connection.recv(1024)
                            if not data:
                                break
                            epics_handler(connection, data)

                    print(f"Connection to client closed\n")
                    count += 1
                except KeyboardInterrupt:
                    print("\nServer quit by user")
                    break
    except Exception as e:
        print(f"Exception occured {e}")

if __name__ == "__main__":
    main()
