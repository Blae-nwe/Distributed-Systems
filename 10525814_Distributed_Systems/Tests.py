import multiprocessing
import time

from Client import UserClient
from Core import Client, Server, Node
from Server import PrimeNode, FDSNode, AuthenticationNode
import unittest


class TestCore(unittest.TestCase):
    def setUp(self) -> None:
        self.server = Server.Server("localhost", 50001)
        self.client = Client.Client()
        self.server_proc = multiprocessing.Process(target=self.server.start_server)
        self.server_proc.start()

    def tearDown(self) -> None:
        self.server_proc.terminate()

    def test_client_connects_to_server(self):
        response = self.client.send("localhost", 50001, b"data")
        self.assertEqual(response, b"Unknown command")  # add assertion here


class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        self._known_addr = ("localhost", 5001)

    def test_prime_node_starts(self):
        self.prime_node = PrimeNode.PrimeNode(self._known_addr)
        self.prime_node_proc = multiprocessing.Process(target=self.prime_node.start_node)
        self.prime_node_proc.start()
        self.node = Node.Node("localhost", 5002, "test", self._known_addr)
        self.node_proc = multiprocessing.Process(target=self.node.start_node)
        self.node_proc.start()

        time.sleep(5)
        print(self.prime_node._registered_nodes)

        self.prime_node_proc.terminate()
        self.node_proc.terminate()

    def test_fds_list(self):
        self.fds = FDSNode.FDSNode(self._known_addr)
        self.fds_proc = multiprocessing.Process(target=self.fds.start_node)
        self.fds_proc.start()
        self.client = Client.Client()
        response = self.client.send("localhost", 6001, b"List")
        print(response)
        self.fds_proc.terminate()

    def test_UserClient(self):
        self.prime_node = PrimeNode.PrimeNode(self._known_addr)
        self.prime_node_proc = multiprocessing.Process(target=self.prime_node.start_node)
        self.prime_node_proc.start()
        self.fds = FDSNode.FDSNode(self._known_addr)
        self.fds_proc = multiprocessing.Process(target=self.fds.start_node)
        self.fds_proc.start()
        self.userclient = UserClient.UserClient(self._known_addr)
        self.userclient.run()

    def test_authentication_node(self):
        self.prime_node = PrimeNode.PrimeNode(self._known_addr)
        self.prime_node_proc = multiprocessing.Process(target=self.prime_node.start_node)
        self.prime_node_proc.start()
        self.auth = AuthenticationNode.AuthenticationNode(self._known_addr)
        self.auth_proc = multiprocessing.Process(target=self.auth.start_node)
        self.auth_proc.start()
        self.fds = FDSNode.FDSNode(self._known_addr)
        self.fds_proc = multiprocessing.Process(target=self.fds.start_node)
        self.fds_proc.start()
        self.userclient = UserClient.UserClient(self._known_addr)
        self.userclient.run()


if __name__ == '__main__':
    unittest.main()
