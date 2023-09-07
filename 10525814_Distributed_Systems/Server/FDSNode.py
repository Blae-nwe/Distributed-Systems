from Core.Node import Node
import os
import json


class FDSNode(Node):
    def __init__(self, known_address):
        super().__init__("localhost", 0, "FDS", known_address)
        self._registered_function_nodes = {}

    def process_data(self, data, conn):
        message = data.decode()
        message = message.split(" ")
        valid_token = self.check_token(message[1])
        print(message[1], " this is the token passed")
        if valid_token == "Valid":
            print("Token is valid response")
            if message[0] == "List":
                print("Client wants song list")
                song_list = self._list()
                print("song list", song_list)
                return f"{song_list}".encode()
            elif message[0] == "Send":
                print("Client wants the song sent")
                self._send(" ".join(message[2:]), conn)
                return b"Done"
        else:
            print(valid_token, "Token is invalid or unknown response")
            return b"Invalid token"

    def _list(self):
        # directory path
        path = "..\\Data\\"
        # get all filenames in the directory
        filenames = [f.strip(".mp3") for f in os.listdir(path)]
        json_data = json.dumps(filenames)
        return json_data

    def _send(self, song, conn):
        conn.send(b"Ready")
        with open("..\\Data\\" + song + ".mp3", "rb") as song_file:
            data = song_file.read(1024)
            print(song_file)
            while data:
                conn.send(data)
                data = song_file.read(1024)

    def check_token(self, token):
        response = self.send(self._known_address[0], self._known_address[1], b"Auth")
        message = response.decode()
        message = message[1:-1]
        message = message.split(", ")
        message[0] = message[0].strip("'")
        message[1] = message[1].strip("'")
        message[1] = int(message[1])
        self._registered_function_nodes["Auth"] = message
        print(self._registered_function_nodes["Auth"], "this is the registered function nodes to fds")
        response = self.send(self._registered_function_nodes["Auth"][0], self._registered_function_nodes["Auth"][1], f"Check {token}".encode())
        message = response.decode()
        print(message, "Response from Auth node to check the given token for FDS node")
        if message == "Valid":
            return "Valid"
        else:
            return "Invalid token"



