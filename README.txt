To run the system:
PrimeNode.py needs to be run
2 ControlNode.py needs to be run    #crucial so that both FDS and Auth nodes can spawn
UserClient.py needs to be run

More info:
2 instances of the control nodes are needed to be run after starting the Prime node so that they can each be the Authentication and the FDS node respectively, after the Prime node has sent them a request to be a specific node that it needs.
UserClient has to login to use the FDS node functionality.

UserClient Commands:
REGISTER - Register with the Authentication node using a username and password
LOGIN - Login with the Authentication node using a username and password
LIST - Requests the song list from the FDS node and prints it
SONG - Plays a requested song for the user if the song is in the list
HELP - Displays all the commands for the UserClient

	