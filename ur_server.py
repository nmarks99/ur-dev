import socket

HOST = "164.54.104.7"
PORT = 31001
count = 0

var_dict = {
    'BlockID' : 999,
}

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
                    data_recv = data.decode("ascii")
                    print(f"Recieved: {repr(data_recv)}")
                   
                    var = data_recv.split(" ")[1].strip() # fails if bad received data
                    if var in var_dict.keys():
                        value = var_dict[var]
                        reply = f"{var} {value}\n"
                        print(f"To send: {repr(reply)}")
                        connection.sendall(reply.encode("utf-8"))
                    else:
                        print(f"variable {var} not found")
                        connection.sendall("1".encode("utf-8"))
            print(f"Connection to client closed\n")
            count += 1
        except KeyboardInterrupt:
            print("\nServer quit by user")
            break

