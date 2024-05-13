import socket
import random


host = ''       
port = 7777
ui = '''== Guessing Game ==
Enter You Guess: '''
correct_guess = 0
client_socket = None


# Initialize Socket Object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print(f'Server listening on port {port}...')


while True:
    if client_socket is None:
        print('Waiting for Connection...')
        client_socket, client_address = s.accept()
        print(f'Accepted Connection from {client_address[0]}')
        client_socket.sendall(ui.encode())                      # Send [UI] (Encode)
        correct_guess = random.randint(1, 100)

    else:
        client_input = client_socket.recv(1024)                 # Receive [User Input]
        guess = int(client_input.decode().strip())              # Decode [User Input]
        print(f'User Guess Attempt: {guess}')
        if guess == correct_guess:
            client_socket.sendall(b'Correct Answer!')           # Send [Result]         # b'' == ''.encode()
            client_socket.close()
            print()
            client_socket = None
        elif guess > correct_guess:
            client_socket.sendall(b'Wrong Answer! (Lower)\n\nEnter Your Guess:')        # Send [Result]
        elif guess < correct_guess:
            client_socket.sendall(b'Wrong Answer! (Higher)\n\nEnter Your Guess:')       # Send Result]
s.close()
