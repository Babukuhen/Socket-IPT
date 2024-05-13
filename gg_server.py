import socket
import random


host = ''       
port = 7777

correct_guess = 0
client_socket = None

username_str = '== Guessing Game ==\nEnter Username: '
username_lock = False

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
        correct_guess = random.randint(1, 100)

    else:
        if not username_lock:
            client_socket.sendall(username_str.encode())                    # Send 'Username' String
            username_input = client_socket.recv(1024)                       # Receive 'Username' Input
            username_ans = str(username_input.decode().strip())             # Decode 'Username' Input
            username_lock = True                                            # Lock 'Username'
            print(f'Username: {username_ans}')

        guess_str = f'\n[{correct_guess}] Enter Your Guess: '
        client_socket.sendall(guess_str.encode())                           # Send ['Guess' Input]
        guess_input = client_socket.recv(1024)                              # Receive ['Guess' Input]
        guess_ans = int(guess_input.decode().strip())                       # Decode ['Guess' Input]
        print(f'User Guess Attempt: {guess_ans}')
        
        if guess_ans == correct_guess:
            client_socket.sendall(b'Correct Answer!')                       # Send ['Result' String]
            # 'Play Again' Feature
            # Yes - New Difficulty, Unlock Difficulty
            # No - Exit, New User Can Play, Unlock User & Difficulty
            

            print()
            client_socket.close()
            client_socket = None

        elif guess_ans > correct_guess:
            client_socket.sendall(b'Wrong Answer! (Lower)\n\nEnter Your Guess:')        # Send ['Result' String]
        elif guess_ans < correct_guess:
            client_socket.sendall(b'Wrong Answer! (Higher)\n\nEnter Your Guess:')       # Send ['Result' String]
s.close()
