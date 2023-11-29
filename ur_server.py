import socket

HOST = "127.0.0.1" # localhost
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    while True:
        try: 
            print("Waiting for connection...")
            connection, address = sock.accept()
            with connection:
                print(f"Connection established with {address}")
                while True:
                    data = connection.recv(1024)
                    if not data:
                        break
                    print(f"Recieved: {data.decode('utf-8')}")
                    # connection.sendall(data) # echoes the message back to the client
            print(f"Connection to client closed")
        except KeyboardInterrupt:
            print("\nServer quit by user")
            break

