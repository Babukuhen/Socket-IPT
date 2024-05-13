import socket
import random


host = ''       
port = 7777


client_socket = None

username_str = '== Guessing Game ==\nEnter Username: '
username_lock = False

diff_str = '''
> Choose Difficulty <
[A] Easy (1 - 50)
[B] Medium (1 - 100)
[C] Hard (1 - 500)'''
diff_ans = 'A'
diff_lock = False

correct_guess = 0
repeat_ans = None


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

    else:
        if not username_lock:
            client_socket.sendall(username_str.encode())                    # Send 'Username' String
            username_input = client_socket.recv(1024)                       # Receive 'Username' Input
            username_ans = str(username_input.decode().strip())             # Decode 'Username' Input
            username_lock = True                                            # Lock 'Username'
            print(f'Username: {username_ans}')

        if not diff_lock:
            client_socket.sendall(diff_str.encode())                        # Send ['Difficulty' String]
            diff_input = client_socket.recv(1024)                           # Receive ['Difficulty' Input]
            diff_ans = str(diff_input.decode().strip())                     # Decode ['Difficulty' Input]
            print(f'Game Difficulty: {diff_ans}')
            if diff_ans == 'A': 
                correct_guess = random.randint(1,50)
                # Leaderboard Stuff [Easy]
            elif diff_ans == 'B': 
                correct_guess = random.randint(1,100)
                # Leaderboard Stuff [Medium]
            elif diff_ans == 'C': 
                correct_guess = random.randint(1,500)
                # Leaderboard Stuff [Hard]

            # Display Leaderboard [Separated by Difficulty]
            diff_lock = True        

        guess_str = f'\n[{correct_guess}] Enter Your Guess: '
        client_socket.sendall(guess_str.encode())                           # Send ['Guess' Input]
        guess_input = client_socket.recv(1024)                              # Receive ['Guess' Input]
        guess_ans = int(guess_input.decode().strip())                       # Decode ['Guess' Input]
        print(f'User Guess Attempt: {guess_ans}')
        
        if guess_ans == correct_guess:
            client_socket.sendall(b'Correct Answer!\n\nPlay Again? [Y/N]')                       # Send ['Result' String]
            repeat_input = client_socket.recv(1024)
            repeat_ans = str(repeat_input.decode().strip())
            if repeat_ans == 'Y':
                print('Again!')
                diff_lock = False
            elif repeat_ans == 'N':
                username_lock = False
                diff_lock = False
                print()
                client_socket.close()
                client_socket = None

        elif guess_ans > correct_guess:
            client_socket.sendall(b'Wrong Answer! (Lower)\n\nEnter Your Guess:')        # Send ['Result' String]
        elif guess_ans < correct_guess:
            client_socket.sendall(b'Wrong Answer! (Higher)\n\nEnter Your Guess:')       # Send ['Result' String]
s.close()

# LEADERBOARD FEATURE [TO BE ADDED]
# Server initializes NEW dictionaries each time it runs
# Data is based on the txt files 

# Write Mode - checks the respective dictionary (based on difficulty) and it sorts the scores 
# THEN rewrites the entire txt file with the new sorted order
# Display the TOP 10 in Client Side