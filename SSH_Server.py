from socket import socket, AF_INET, SOCK_STREAM


# Funkcja do uruchamiania prostego serwera na określonym porcie
def ssh_server(port_number):
    # Otwórz plik dziennika w trybie dopisywania
    with open("server_log.txt", "a") as log_file:
        # Utwórz gniazdo
        server_socket = socket(AF_INET, SOCK_STREAM)
        # Przypisz gniazdo do określonego portu
        server_socket.bind(('localhost', port_number))
        # Nasłuchuj przychodzących połączeń
        server_socket.listen(5)

        # Wydrukuj status działania serwera
        print(f"Serwer działa na porcie {port_number}.")

        # Zaakceptuj przychodzące połączenia
        while True:
            # Zaakceptuj nowe połączenie klienta
            client_socket, client_address = server_socket.accept()
            print(f"Nawiązano połączenie z: {client_address[0]}")

            # Odbieraj i przetwarzaj polecenia od klienta
            while True:
                # Odbierz polecenie od klienta
                command = client_socket.recv(1024).decode()
                print(f"Otrzymano polecenie od {client_address[0]}: {command}")
                # Zapisz otrzymane polecenie do pliku dziennika
                log_file.write(
                    f"Otrzymano polecenie od {client_address[0]}: {command}\n")
                # Sprawdź, czy klient chce się rozłączyć
                if command.strip() == "exit":
                    print(
                        f"Klient {client_address[0]} poprosił o rozłączenie.")
                    # Wyślij wiadomość o rozłączeniu do klienta
                    client_socket.sendall(
                        "Rozłączanie z serwerem.".encode())
                    # Zapisz wiadomość o rozłączeniu do pliku dziennika
                    log_file.write(
                        f"Klient {client_address[0]} poprosił o rozłączenie.\n")
                    # Zamknij gniazdo klienta
                    client_socket.close()
                    break
                else:
                    # Wyślij odpowiedź do klienta
                    client_socket.sendall(f"Wprowadziłeś: {command}".encode())
                    # Zapisz odpowiedź do pliku dziennika
                    log_file.write(
                        f"Odpowiedź wysłana do {client_address[0]}: Wprowadziłeś: {command}\n")


if __name__ == "__main__":
    # Pobierz numer portu od użytkownika
    port_number = int(input("Podaj numer portu: "))
    # Uruchom serwer
    ssh_server(port_number)
