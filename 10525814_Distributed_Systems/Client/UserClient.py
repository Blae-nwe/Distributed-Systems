import json
import multiprocessing
import socket
import time
from playsound import playsound

from Core.Client import Client


class UserClient(Client):
    def __init__(self, known_address):
        super().__init__()
        self._nodes = {}
        self._known_address = known_address
        self._token = 0
        self._running = True
        self._songplay = None

    def run(self):
        print("Client is now running")
        while self._running:
            userinput = input("Enter a command")
            if userinput.lower() == "register":
                self.register_with_auth()
            elif userinput.lower() == "help":
                print("The available commands are: Register, Login, List, Song")
            elif userinput.lower() == "login":
                self.login_with_auth()
            elif userinput.lower() == "list":
                self.get_fds_list()
            elif userinput.lower() == "song":
                self.get_song()
            else:
                print("Unknown command")

    def request_fds_node(self):
        # getting and storing the fds node address
        response = self.send(self._known_address[0], self._known_address[1], b"FDS")
        message = response.decode()
        message = message[1:-1]
        message = message.split(", ")
        message[0] = message[0].strip("'")
        message[1] = message[1].strip("'")
        message[1] = int(message[1])
        print(message)
        self._nodes["FDS"] = message

    def get_fds_list(self):
        if "FDS" not in self._nodes:
            self.request_fds_node()
        # requesting song list from fds node
        response2 = self.send(self._nodes["FDS"][0], self._nodes["FDS"][1], f"List {self._token}".encode())
        print(self._nodes["FDS"], " client thinks fds node")
        if response2 == b"Invalid token":
            print("You are not logged in please login")
        else:
            message2 = json.loads(response2.decode())
            print(message2)

    def request_auth_node(self):
        # getting and storing auth address
        response = self.send(self._known_address[0], self._known_address[1], b"Auth")
        message = response.decode()
        message = message[1:-1]
        message = message.split(", ")
        message[0] = message[0].strip("'")
        message[1] = message[1].strip("'")
        message[1] = int(message[1])
        print(message)
        self._nodes["Auth"] = message

    def register_with_auth(self):
        if "Auth" not in self._nodes:
            self.request_auth_node()
        # registering with the client
        while True:
            username = input("Enter a username")
            password = input("Enter a password")
            response = self.send(self._nodes["Auth"][0], self._nodes["Auth"][1], f"Register {username} {password}".encode())
            message = response.decode()
            print(message)
            if message == "A user already has this name":
                print("Please enter another username and password")
            elif message == "Registered with auth node":
                break
            elif message == "There was a error registering":
                print("Please enter another username and password")
            else:
                print("Please enter another username and password")

    def login_with_auth(self):
        if "Auth" not in self._nodes:
            self.request_auth_node()
        username = input("Enter a username")
        password = input("Enter a password")
        # login to auth and get token
        response = self.send(self._nodes["Auth"][0], self._nodes["Auth"][1], f"Login {username} {password}".encode())
        message = response.decode()
        print(message)
        if message == "Invalid login":
            print("You have failed to login")
        else:
            self._token = message

    def get_song(self):
        if "FDS" not in self._nodes:
            self.request_fds_node()
        song_name = input("Enter the song you would like")
        # requesting song from fds
        if self.receive_file(self._nodes["FDS"][0], self._nodes["FDS"][1], self._token, song_name):
            time.sleep(3)
            if self._songplay:
                self._songplay.terminate()
            self._songplay = multiprocessing.Process(target=playsound,args=("song.mp3",))
            self._songplay.start()
            time.sleep(0.1)

    def receive_file(self, host, port, token, song):
        s = socket.socket()
        message3 = f"Send {token} {song}".encode()
        s.connect((host, port))
        s.send(message3)

        response = s.recv(1024)
        if response == b"Ready":
            data = b""
            while True:
                chunk = s.recv(1024)
                if chunk == b"":
                    break
                data += chunk
            with open("song.mp3", "wb") as song_file:
                song_file.write(data)
        else:
            s.close()
            return False
        s.close()
        return True


if __name__ == "__main__":
    UserClient(("localhost", 5001)).run()
