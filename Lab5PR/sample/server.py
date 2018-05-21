import socket
import datetime
from pytz import reference
import random
import string

first_names=('John','Andy','Joe', 'Mark', 'Chester')
last_names=('Johnson','Smith','Williams', 'Doe', 'Pier')

ListOfCommands = [
    '/help - Get all available commands',
    '/hello <text> - Output a text',
    '/flip - Flips the coin',
    '/random_name - Generates random Full Name',
    '/timezone - Returns servers timezone'
]

def start_server(address, port, max_connections=5):
    # We're using TCP/IP as transport
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to the given address and port
    server_socket.bind((address, port))
    # Listen for incoming connection (with max connections)
    server_socket.listen(max_connections)
    print("=== Listening for connections at %s:%s" % (address, port))
    while True:
        # Accept an incomming connection
        # Note: this is blocking and synchronous processing of incoming connection
        incoming_socket, address = server_socket.accept()
        print("=== New connection from %s" % (address,))
        # Recv up to 1kB of data
        data = incoming_socket.recv(1024)
        print(">>> Received data %s" % (data,))

        if(data[0] == '/'):
            command = data[1:]
            if command == 'help':
                string_response = '\n'
                for i in range(len(ListOfCommands)):
                    string_response = string_response + ListOfCommands[i] + '\n'
                incoming_socket.send(string_response)
                incoming_socket.close()
            elif command == 'flip':
                coin = random.randint(1, 2)
                coinText = ""
                if(coin == 1):
                    coinText = "Heads"
                else:
                    coinText = "Tails"
                incoming_socket.send("Coin has been flipped : " + coinText)
                incoming_socket.close()
            elif command == 'random_name':
                random_name = random.choice(first_names)+" "+random.choice(last_names)
                incoming_socket.send('Your random generated name : ' + random_name)
                incoming_socket.close()
            elif command == 'timezone':
                today = datetime.datetime.now()
                localtime = reference.LocalTimezone()
                timezone = localtime.tzname(today)

                incoming_socket.send('Servers timezone : ' + timezone)
                incoming_socket.close()
            else:
                list_of_commands = command.split()
                if(list_of_commands[0] == 'hello'):
                    incoming_socket.send(command[6:])
                else:
                    incoming_socket.send('No such function')
                    incoming_socket.close()
        else:
            incoming_socket.send('Error 404 : Functions starts with / by instructions')
            incoming_socket.close()


if __name__ == '__main__':
    start_server('127.0.0.1', 8000)