#!./.venv/bin/python3
import socket
from epics import caget, caput

# HOST = "164.54.116.80" # pepper IP address
# PORT = 31111
# BUFFER_SIZE = 1024
# PREFIX = "8idgur3e"
# count = 0

HOST = "localhost" # pepper IP address
PORT = 31111
BUFFER_SIZE = 1024
PREFIX = "urdev"
count = 0

def epics_handler(connection, data_recv):
    if len(data_recv) >= 2 and len(data_recv) <= 3:
        cmd = data_recv[0]
        if cmd == "GET":
            var = data_recv[1]
            value = caget(f"{PREFIX}:{var}.VAL")
            if value is None:
                value = 0
                print(f"PV {var} not found. Sending {var}=0 to socket")
            reply = f"{var} {value}\n"
            connection.sendall(reply.encode("utf-8"))
        elif cmd == "SET":
            var = data_recv[1]
            val = data_recv[2]
            result = caput(f"{PREFIX}:{var}.VAL", val)
            if result is None:
                print(f"PV {var} not found. No action taken")

    else:
        print(f"Invalid input received {data_recv}\nNo action taken.")

if __name__ == "__main__":
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
                        data_recv = data.decode("ascii").strip().split(" ")
                        epics_handler(connection, data_recv)

                print(f"Connection to client closed\n")
                count += 1
            except KeyboardInterrupt:
                print("\nServer quit by user")
                break
