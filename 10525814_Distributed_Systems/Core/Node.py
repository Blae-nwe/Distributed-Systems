import time

from Core.Client import Client
from Core.Server import Server


class Node(Server, Client):
    def __init__(self, host, port, name, known_address):
        super(Node, self).__init__(host, port)
        self._name = name
        self._registered = False
        self._known_address = known_address

    def start_node(self):
        self.start_server()

    def run(self):
        if self._known_address == (self._host, self._port):
            return
        while not self._registered:
            try:
                response = self.send(self._known_address[0], self._known_address[1], f"Register {self._name} {self._host} {self._port}".encode())
                if response == b"OK":
                    self._registered = True
            except ConnectionRefusedError:
                print("Unable to connect")
                time.sleep(5)
