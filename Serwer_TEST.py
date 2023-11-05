import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def simple_server(port_number):
    with open("server_log.txt", "a") as log_file:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', port_number))
        server_socket.listen(2)

        ip_address = get_ip()
        print(f"Server is running on {ip_address}, port:{port_number}.")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established from: {client_address[0]}")

            while True:
                command = client_socket.recv(1024).decode()
                print(f"Command received from {client_address[0]}: {command}")
                log_file.write(
                    f"Command received from {client_address[0]}: {command}\n")
                if command.strip() == "exit":
                    print(
                        f"Client {client_address[0]} has requested to disconnect.")
                    client_socket.sendall(
                        "Disconnecting from the server.".encode())
                    log_file.write(
                        f"Client {client_address[0]} has requested to disconnect.\n")
                    client_socket.close()
                    break
                else:
                    client_socket.sendall(f"You entered: {command}".encode())
                    log_file.write(
                        f"Response sent to {client_address[0]}: You entered: {command}\n")


if __name__ == "__main__":
    port_number = int(input("Enter the port number: "))
    simple_server(port_number)
