import socket
import threading


class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._listening_socket = None

    def start_server(self):
        # Create a socket and bind it to the host and port
        self._listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listening_socket.bind((self._host, self._port))
        self._port = self._listening_socket.getsockname()[1]

        # Listen for incoming connections
        self._listening_socket.listen()
        print(f"Server listening for incoming connections on {self._host}:{self._port}")
        threading.Thread(target=self.run).start()

        # Accept incoming connections and handle them in a separate thread
        while True:
            conn, addr = self._listening_socket.accept()
            print(f"Accepting incoming connection from {addr}")

            threading.Thread(target=self.handle_connection, args=(conn,)).start()

    def handle_connection(self, conn):
        # Receive data
        data = conn.recv(1024)
        print(f"Received data {data.decode()}")
        # Process data and send response
        response = self.process_data(data, conn)
        conn.sendall(response)
        conn.close()

    def process_data(self, data, conn):
        return b"Unknown command"

    def run(self):
        pass


if __name__ == "__main__":
    server = Server("localhost", 50001)
