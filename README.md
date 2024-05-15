## Guessing Game - Server and Client (README)

This project implements a multiplayer guessing game server and client using Python sockets. 

### Server

The server listens for incoming connections on port 7777. Once a connection is established, it facilitates the following gameplay:

1. **User Authentication:** The server prompts the client for a username.
2. **Difficulty Selection:** The client chooses a difficulty level (Easy, Medium, Hard) from a predefined list.
3. **Game Loop:** 
    - The server generates a random number based on the chosen difficulty.
    - The client is prompted to guess the number.
    - The server provides feedback based on the guess (higher, lower, or correct).
    - If the guess is correct, the game offers the option to play again. User score is saved based on difficulty.
4. **Leaderboard:** Scores are stored in separate text files for each difficulty. The top 10 entries are displayed upon difficulty selection and after a game ends.

**Server Functionality:**

- Handles client connections and manages communication.
- Generates random numbers based on difficulty.
- Stores and updates user scores in leaderboards.
- Manages game flow and provides feedback to clients.

**Server Code:**

The `gg_server.py` file contains the server implementation.

### Client

The client connects to the server on port 7777. It interacts with the server to participate in the guessing game.

**Client Functionality:**

- Connects to the server.
- Provides a username.
- Selects a difficulty level.
- Guesses the randomly generated number.
- Receives feedback from the server.
- Chooses to play again or exit the game.
- Displays the leaderboard for the chosen difficulty.

**Client Code:**

The `gg_client.py` file contains the client implementation.

### Note:

- The server maintains separate leaderboard files for each difficulty (`leaderboard_easy.txt`, `leaderboard_medium.txt`, `leaderboard_hard.txt`).
- The leaderboard displays the top 10 entries with name and score.
- The code includes comments to explain functionality.

### Running the Game:

1. Run the server: `py gg_server.py`
2. Run multiple client instances: `py gg_client.py` (for multiple players)

Enjoy the guessing game!
