import socket
import time


host = 'localhost'                              
port = 7777 


username_lock = False
diff_lock = False

def display_file_contents(file_path):                   # Display File Contents [Up to 10 Lines]
    print('\n== Leaderboard ==\n')
    with open(file_path, 'r') as file:
        line_count = 0
        for line in file:
            if line_count < 10:
                print(line.strip())
                line_count += 1
            else:
                print("...")
                break

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

    if not diff_lock:
        diff_str = s.recv(1024)                         # Receive ['Difficulty' String]
        print(diff_str.decode())                        # Print ['Difficulty' String]
        diff_input = input('D: ').strip().upper()       # Input 'Difficulty'
        if diff_input == 'A': file_path = 'leaderboard_easy.txt'
        elif diff_input == 'B': file_path = 'leaderboard_medium.txt'
        elif diff_input == 'C': file_path = 'leaderboard_hard.txt'
        s.sendall(diff_input.encode())                  # Send ['Difficulty' Input]
        diff_lock = True                                # Lock 'Difficulty'

        display_file_contents(file_path)                # Display Txt File [Line by Line, Up To 10]

    guess_str = s.recv(1024)                            # Receive ['Guess' String]
    print(guess_str.decode())                           # Print ['Guess' String]
    guess_input = input('G: ').strip()                  # Input 'Guess'
    s.sendall(guess_input.encode())                     # Send ['Guess' Input]

    result_str = s.recv(1024).decode()                  # Receive ['Result' String]
    if "Correct" in result_str:
        print(result_str)
        again_input = input('R: ').strip().upper()      # Input 'Play Again'
        if again_input == 'Y': 
            diff_lock = False
            s.sendall(again_input.encode())             # Send ['Play Again' Input]
        elif again_input == 'N':
            username_lock = False
            diff_lock = False
            s.sendall(again_input.encode())             # Send ['Play Again' Input]

            display_file_contents(file_path)            # Display Txt File [Line by Line, Up To 10]

            break
    else:
        print(result_str)

s.close()
