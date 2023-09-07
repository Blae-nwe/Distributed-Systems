import time
import multiprocessing

from Core.Node import Node
from Server import FDSNode, AuthenticationNode


class ControlNode(Node):
    def __init__(self, known_address):
        super().__init__("localhost", 0, "Control", known_address)
        self._known_address = known_address
        self._functionality = None
        self._connected = False

    def process_data(self, data, conn):
        message = data.decode()
        message = message.split(" ")
        if message[0] == "FDS":
            self._functionality = message[0]
            fds = FDSNode.FDSNode(self._known_address)
            multiprocessing.Process(target=fds.start_node).start()
            return b"OK"
        elif message[0] == "Free":
            if self._functionality is None:
                return b"Free"
            else:
                return b"No"
        elif message[0] == "Auth":
            self._functionality = message[0]
            auth = AuthenticationNode.AuthenticationNode(self._known_address)
            multiprocessing.Process(target=auth.start_node).start()

            return b"ok"
        else:
            return b"Unknown command"

    def run(self):
        while not self._connected:
            try:
                connect = self.send(self._known_address[0], self._known_address[1], f"Register Control {self._host} {self._port}".encode())
                if connect == b"OK":
                    self._connected = True
                    break
            except:
                pass
            time.sleep(2)


if __name__ == "__main__":
    ControlNode(("localhost", 5001)).start_node()
