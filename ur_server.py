#!./.venv/bin/python3
import socket
from epics import caget, caput

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
PORT = 31111
BUFFER_SIZE = 1024
PREFIX = "8idgur3e"

def epics_handler(connection, data):
    data_recv = data.decode("ascii").strip().split(" ")
    print(data_recv)
    print(f"length = {len(data_recv)}")
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
