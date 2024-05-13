import socket
import time

host = 'localhost'                              
port = 7777 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
time.sleep(0)

data = s.recv(1024)                             # Receive [UI]
print(data.decode().strip())                    # Print [UI]

while True:
    user_input = input('').strip()
    s.sendall(user_input.encode())              # Send [User Input] (Encode)
    result = s.recv(1024).decode().strip()      # Receive [Result]
    if "Correct" in result:
        print(result)
        break
    else:
        print(result)

s.close()
