import socket

def start_server(host, port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Enable the server to accept connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        # Wait for a connection
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Handle the connection
        handle_client(client_socket)


def handle_client(client_socket):
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Echo the data back to the client
            client_socket.sendall(data)
            print(f"Received and echoed back: {data.decode('utf-8')}")

    except ConnectionResetError:
        print("Connection reset by peer")
    finally:
        # Close the client socket
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    # Set the host and port for the server
    host = "164.54.104.7"  # Use "0.0.0.0" to allow connections from other devices on the network
    port = 31001

    start_server(host, port)
