Python Socket-Based GUI Chat Application
A real-time multi-client chat application built with Python sockets and Tkinter GUI.
Supports multiple clients, usernames, chat history logging, online user list, and admin commands like kick and ban.
Features
- Multi-client support using threading and sockets
- User authentication with usernames
- Real-time chat with timestamps
- Chat history saved to a text file (chat_history.txt)
- Online users displayed on the server GUI
- Admin commands (/kick username, /ban username) to manage users
- Ban list saved in a file (banned_users.txt) for persistent bans
- Modern, dark-themed Tkinter GUI for both server and clients
- Emoji support in messages
Requirements
- Python 3.x
- No external dependencies (only standard library)
How to Run
Run the server:
- python server.py
Run clients:
- python client.py
Enter your username when prompted. If your username is banned, connection will be refused.
Admin Commands:
Use username admin to enable special commands in chat:
Kick a user: /kick username
Ban a user (kicks and bans persistently): /ban username
