import socket
import random

# Function to generate a random number for the game
def generate_number():
    return random.randint(1, 100)

# Function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #localhost: 0.0.0.0
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(1)
    print("Server listening on port 12345")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Authentication
        authenticate(client_socket)

        # Play the game
        play_game(client_socket)

# Function to authenticate the client
def authenticate(client_socket):
    auth_attempts = 0
    while auth_attempts < 3:
        user_input = client_socket.recv(1024).decode('utf-8')
        username, password = user_input.split(',')
        
        if username == 'admin' and password == 'admin123':
            client_socket.send("Authentication successful".encode('utf-8'))
            print("Authentication successful")
            return
        else:
            auth_attempts += 1
            client_socket.send("Authentication failed. Please try again.".encode('utf-8'))

    # If authentication fails after 3 attempts, close the connection
    print("Authentication failed. Closing connection.")
    client_socket.close()

# Function to play the guessing game
def play_game(client_socket):
    number_to_guess = generate_number()
    attempts_left = 9

    while attempts_left > 0:
        guess = int(client_socket.recv(1024).decode('utf-8'))
        if guess == number_to_guess:
            client_socket.send("Congratulations! You guessed the number.".encode('utf-8'))
            break
        elif guess < number_to_guess:
            client_socket.send("Too low. Try again.".encode('utf-8'))
        else:
            client_socket.send("Too high. Try again.".encode('utf-8'))

        attempts_left -= 1

    if attempts_left == 0:
        client_socket.send("Out of attempts. The correct number was {}".format(number_to_guess).encode('utf-8'))

    # Ask if the user wants to play again
    play_again = client_socket.recv(1024).decode('utf-8')
    if play_again.lower() == 'yes':
        play_game(client_socket)
    else:
        client_socket.send("Goodbye!".encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    start_server()
