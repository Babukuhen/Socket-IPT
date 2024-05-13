import socket
import time

username_lock = False


host = 'localhost'                              
port = 7777 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
time.sleep(0)

while True:
    if not username_lock:                   
        username_str = s.recv(1024)                     # Receive 'Username' String
        print(username_str.decode())                    # Print 'Username' String
        username_input = input('U: ').strip()           # Input 'Username'
        s.sendall(username_input.encode())              # Send 'Username' Input
        username_lock = True                            # Lock 'Username'

    guess_str = s.recv(1024)                            # Receive ['Guess' String]
    print(guess_str.decode())                           # Print ['Guess' String]
    guess_input = input('G: ').strip()                  # Input 'Guess'
    s.sendall(guess_input.encode())                     # Send ['Guess' Input]

    result_str = s.recv(1024).decode()                  # Receive ['Result' String]
    if "Correct" in result_str:
        print(result_str)
        # 'Play Again' Feature
        # Yes - New Difficulty, Unlock Difficulty
        # No - Exit, New User Can Play, Unlock User & Difficulty

    else:
        print(result_str)

s.close()
