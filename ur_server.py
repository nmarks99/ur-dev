#!/usr/bin/env python3
import socket
from epics import caget

HOST = "164.54.116.80" # pepper IP address
PORT = 31111
BUFFER_SIZE = 1024
PREFIX = "8idgur3e"
count = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    while True:
        try: 
            # print("Waiting for connection...")
            connection, address = sock.accept()
            with connection:
                # print(f"[{count}] Connection opened on {address}")
                while True:
                    data = connection.recv(1024)
                    if not data:
                        break
                    data_recv = data.decode("ascii")
                    # print(f"Recieved: {repr(data_recv)}")
                   
                    var = data_recv.split(" ")[1].strip()
                    value = caget(f"{PREFIX}:{var}.VAL")
                    reply = f"{var} {value}\n"
                    # print(f"To send: {repr(reply)}")
                    connection.sendall(reply.encode("utf-8"))

            # print(f"Connection to client closed\n")
            count += 1
        except KeyboardInterrupt:
            print("\nServer quit by user")
            break

