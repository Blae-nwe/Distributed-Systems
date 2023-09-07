import time

from Core.Node import Node


class PrimeNode(Node):
    def __init__(self, known_address):
        super().__init__(known_address[0], known_address[1], "Prime", known_address)
        self._known_address = known_address
        self._registered_nodes = {}

    def process_data(self, data, conn):
        message = data.decode()
        message = message.split(" ")
        if message[0] == "Register":
            if message[1] in self._registered_nodes:
                counter = 0
                for key,value in self._registered_nodes.items():
                    if key.split("_")[0] == message[1]:
                        counter+=1
                message[1] = f"{message[1]}_{counter}"
            self._registered_nodes[message[1]] = (message[2], message[3])
            print(self._registered_nodes, "all the registered nodes")
            print(conn.getpeername(), "connection socket")
            return b"OK"
        if message[0] == "FDS":
            fdsconn = self._registered_nodes.get("FDS", None)
            print(fdsconn, "getting the fds conn from the dict")
            return f"{fdsconn}".encode()
        if message[0] == "Auth":
            authconn = self._registered_nodes.get("Auth", None)
            print(authconn, "getting the auth conn from the dict")
            return f"{authconn}".encode()
        else:
            return b"Unknown command"

    def run(self):
        while True:
            nodes_needed = ["Auth", "FDS"]
            for node in nodes_needed:
                if node not in self._registered_nodes:
                    for name,addr in self._registered_nodes.items():
                        if "Control" in name and self.send(addr[0], int(addr[1]), b"Free") == b"Free":
                            self.send(addr[0], int(addr[1]), node.encode())
            time.sleep(2)
            print(self._registered_nodes)


if __name__ == "__main__":
    PrimeNode(("localhost", 5001)).start_node()
