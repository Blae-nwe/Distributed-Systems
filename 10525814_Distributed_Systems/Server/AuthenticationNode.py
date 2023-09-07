from Core.Node import Node
import secrets


class AuthenticationNode(Node):
    def __init__(self, known_address):
        super().__init__("localhost", 0, "Auth", known_address)
        self._registered_clients = {}
        self._token_index = []

    def process_data(self, data, conn):
        message = data.decode()
        message = message.split(" ")
        print(message)
        if message[0] == "Register":
            print("Registering client")
            # return ok
            response = self.register(message[1], message[2])
            return f"{response}".encode()
        # log client in and give token
        if message[0] == "Login":
            isValid = self.login(message[1], message[2])
            if isValid == "Valid":
                token = self.token()
                print("Logged in now giving token")
                return f"{token}".encode()
            else:
                return b"Invalid login"
        # check if user token is valid
        if message[0] == "Check":
            is_valid = self.check_token(message[1])
            return f"{is_valid}".encode()

    def register(self, username, password):
        if username in self._registered_clients:
            print("There is already this username stored")
            return "A user already has this name"
        elif username not in self._registered_clients:
            self._registered_clients[username] = password
            print(self._registered_clients)
            return "Registered with auth node"
        else:
            return "There was a error registering"

    def login(self, username, password):
        key_to_check = username
        password_to_check = password
        if key_to_check in self._registered_clients and self._registered_clients[key_to_check] == password_to_check:
            print("Login Valid")
            return "Valid"
        else:
            print("Login Invalid")
            return "Invalid"

    def token(self):
        # generate token
        token = secrets.token_hex(16)
        self._token_index.append(token)
        print("These are the stored tokens:", self._token_index)
        return token

    def check_token(self, client_token):
        if client_token in self._token_index:
            print("Client token valid")
            return "Valid"
        else:
            print("Client token invalid")
            return "Invalid"
