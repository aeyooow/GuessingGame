import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #change the host to the server's IPv4 address
    #the server and client must be connected in the same server (internet connection)
    client_socket.connect(('192.168.1.6', 12345))

    # Authentication
    authenticate(client_socket)

    # Play the game
    play_game(client_socket)

def authenticate(client_socket):
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        user_input = f"{username},{password}"
        client_socket.send(user_input.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        print(response)

        if response == "Authentication successful":
            break

def play_game(client_socket):
    while True:
        guess = int(input("Enter your guess (1-100): "))
        client_socket.send(str(guess).encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        print(response)

        if "Congratulations" in response or "Out of attempts" in response:
            break

    # Ask if the user wants to play again
    play_again = input("Do you want to play again? (yes/no): ")
    client_socket.send(play_again.encode('utf-8'))

    if play_again.lower() == 'yes':
        play_game(client_socket)
    else:
        client_socket.close()

if __name__ == "__main__":
    start_client()
