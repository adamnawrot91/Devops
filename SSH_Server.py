from socket import socket, AF_INET, SOCK_STREAM


# SSH Server function
def ssh_server(port_number):


    '''
            # Open the file and read the credentials
        with open("access.txt", "r") as access_file:
            username, password = access_file.read().splitlines()
            
            #Still missing auth info inside "talking with server part"
    '''


    # Create log file
    with open("server_log.txt", "a") as log_file:
        # Create socket
        server_socket = socket(AF_INET, SOCK_STREAM)
        # Bind socket to port
        server_socket.bind(('localhost', port_number))
        # Listen for incoming connections, max 5
        server_socket.listen(5)

        print(f"Server is running on a port: {port_number}.")

        # Accept incoming connections
        while True:
            # Accept connection with the client
            client_socket, client_address = server_socket.accept()
            print(f"Connected with: {client_address[0]}")

            # Communication with client
            while True:
                # Receive command from client, number of bytes - 1000, then translate to a string
                command_from_client = client_socket.recv(1000).decode()
                print(f" Received command from: {client_address[0]}: {command_from_client}")
                # Save info to log file:
                log_file.write(
                    f"Receive command from: {client_address[0]}: {command_from_client}\n")
                # Check if client wants to quit the connection
                if command_from_client == "exit":
                    print(
                        f"Client {client_address[0]} ended the connection.")
                    # Send info to the client
                    client_socket.sendall(
                        "Disconnected with the server.".encode())
                    # Save info to log file:
                    log_file.write(
                        f"Client {client_address[0]} ended the connection.\n")
                    # Close  client socket
                    client_socket.close()
                    break
                else:
                    # Send info to the client
                    client_socket.sendall(f"I'm a parrot, You have said: {command_from_client}".encode())
                    # Save info to log file:
                    log_file.write(
                        f"Message has been sent to the: {client_address[0]}: You have wrote: {command_from_client}\n")

# if run this script as a main file (not a on of the module) then...
if __name__ == "__main__":
    # Ask for port
    port_number = int(input("Select port number: "))
    # Run server
    ssh_server(port_number)
