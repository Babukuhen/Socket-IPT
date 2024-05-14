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

leaderboard_dict = {} 
diff_info = ['leaderboard_easy.txt', 100, 5]                                    # Default Values | file path, max score, deduction

def read_file_to_dict(file_path):                                               # File to Dictionary
    leaderboard_dict = {}                                                       # Fills Dictionary with Data from Txt
    with open(file_path, 'r') as file:
        for line in file:
            name, value = line.strip().split(' : ')
            leaderboard_dict[name] = int(value)
    return leaderboard_dict

def sort_and_write_to_file(data_dict, file_path):                               # Sorts Dictionary Based on 'Scores' (Highest to Lowest)
    sorted_items = sorted(data_dict.items(), key=lambda x: x[1], reverse=True)  # Write Mode - Writes the Sorted Items -> Txt File
    with open(file_path, 'w') as file:
        for name, value in sorted_items:
            file.write(f"{name} : {value}\n")


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
            client_socket.sendall(username_str.encode())                        # Send 'Username' String
            username_input = client_socket.recv(1024)                           # Receive 'Username' Input
            username_ans = str(username_input.decode().strip())                 # Decode 'Username' Input
            username_lock = True                                                # Lock 'Username'
            print(f'Username: {username_ans}')

        if not diff_lock:
            client_socket.sendall(diff_str.encode())                            # Send ['Difficulty' String]
            diff_input = client_socket.recv(1024)                               # Receive ['Difficulty' Input]
            diff_ans = str(diff_input.decode().strip())                         # Decode ['Difficulty' Input]
            print(f'Game Difficulty: {diff_ans}')
            if diff_ans == 'A': 
                correct_guess = random.randint(1,50)
                diff_info = ['leaderboard_easy.txt', 100, 5]
                leaderboard_dict = read_file_to_dict(diff_info[0])              # File to Dictionary [Easy]                  
            elif diff_ans == 'B': 
                correct_guess = random.randint(1,100)
                diff_info = ['leaderboard_medium.txt', 200, 10]
                leaderboard_dict = read_file_to_dict(diff_info[0])              # File to Dictionary [Medium]
            elif diff_ans == 'C': 
                correct_guess = random.randint(1,500)
                diff_info = ['leaderboard_hard.txt', 300, 15]
                leaderboard_dict = read_file_to_dict(diff_info[0])              # File to Dictionary [Hard]
            print(f'Correct Guess: {correct_guess}')

            # Display Leaderboard [Client Side]

            diff_lock = True        

        guess_str = f'\n[{correct_guess}] Enter Your Guess: '
        client_socket.sendall(guess_str.encode())                               # Send ['Guess' Input]
        guess_input = client_socket.recv(1024)                                  # Receive ['Guess' Input]
        guess_ans = int(guess_input.decode().strip())                           # Decode ['Guess' Input]
        
        print(f'User Guess Attempt: {guess_ans}')
        
        if guess_ans == correct_guess:
            leaderboard_dict[username_ans] = diff_info[1]                       # Save New Score [Dictionary]

            sort_and_write_to_file(leaderboard_dict, diff_info[0])              # Update Dictionary and Txt File [Write Mode]

            client_socket.sendall(b'Correct Answer!\n\nPlay Again? [Y/N]')      # Send ['Result' String]
            repeat_input = client_socket.recv(1024)                             # Receive ['Play Again' Input]
            repeat_ans = str(repeat_input.decode().strip())
            if repeat_ans == 'Y':
                print('Again!')
                diff_lock = False
            elif repeat_ans == 'N':

                # Display Leaderboard [Client Side]

                username_lock = False
                diff_lock = False
                print()
                client_socket.close()
                client_socket = None

        elif guess_ans > correct_guess:
            diff_info[1] -= diff_info[2]
            client_socket.sendall(b'Wrong Answer! (Lower)')                     # Send ['Result' String]
        elif guess_ans < correct_guess:
            diff_info[1] -= diff_info[2]
            client_socket.sendall(b'Wrong Answer! (Higher)')                    # Send ['Result' String]
s.close()