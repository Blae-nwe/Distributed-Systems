import socket


class Client:
    def __init__(self):
        pass

    def send(self, host, port, data):
        # Create a socket and connect to a server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Send the data and receive response
        client_socket.sendall(data)
        response = client_socket.recv(1024)

        # Close the connection
        client_socket.close()
        return response

