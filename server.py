import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

LOG_FILE = "chat_history.txt"
BANNED_USERS_FILE = "banned_users.txt"

def log_message(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def load_banned_users():
    try:
        with open(BANNED_USERS_FILE, "r") as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

def ban_user(username):
    with open(BANNED_USERS_FILE, "a") as f:
        f.write(username + "\n")

HOST = '0.0.0.0'
PORT = 12345

clients = {}
usernames = {}
banned_users = load_banned_users()

# GUI Setup
root = tk.Tk()
root.title("Server Chat")
root.geometry("600x600")
root.configure(bg="#1e1e1e")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#2d2d2d", fg="#00ff00", font=("Consolas", 12))
chat_display.config(state='disabled')
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

users_label = tk.Label(root, text="Online Users", bg="#1e1e1e", fg="white")
users_label.pack()
user_listbox = tk.Listbox(root, bg="#333333", fg="white")
user_listbox.pack(fill=tk.X, padx=10)

msg_entry = tk.Entry(root, font=("Consolas", 12), bg="#3a3a3a", fg="#ffffff")
msg_entry.pack(padx=10, pady=(0,10), fill=tk.X)

def update_user_list():
    user_listbox.delete(0, tk.END)
    for user in usernames.values():
        user_listbox.insert(tk.END, user)

def display_message(msg):
    chat_display.config(state='normal')
    chat_display.insert(tk.END, msg + "\n")
    log_message(msg)
    chat_display.yview(tk.END)
    chat_display.config(state='disabled')

def broadcast(msg, sender_socket=None):
    for client in list(clients.keys()):
        if client != sender_socket:
            try:
                client.send(msg.encode('utf-8'))
            except:
                del clients[client]

def handle_client(client_socket, addr):
    try:
        username = client_socket.recv(1024).decode('utf-8')

        if username in banned_users:
            client_socket.send("🚫 You are banned.".encode('utf-8'))
            client_socket.close()
            return

        usernames[client_socket] = username
        clients[client_socket] = addr
        update_user_list()

        display_message(f"👋 {username} joined the chat.")
        broadcast(f"🔔 {username} joined the chat.", sender_socket=client_socket)

        while True:
            msg = client_socket.recv(1024).decode('utf-8')

            if msg.startswith("/kick "):
                if username == "admin":
                    target = msg.split(" ", 1)[1]
                    kick_user(target)
            elif msg.startswith("/ban "):
                if username == "admin":
                    target = msg.split(" ", 1)[1]
                    ban_user(target)
                    kick_user(target)
            else:
                timestamp = datetime.now().strftime('%I:%M %p')
                full_msg = f"[@{username} | {timestamp}]: {msg}"
                display_message(full_msg)
                broadcast(full_msg, sender_socket=client_socket)

    except:
        pass
    finally:
        username = usernames.get(client_socket, str(addr))
        display_message(f"❌ {username} disconnected.")
        broadcast(f"❌ {username} left the chat.", sender_socket=client_socket)
        clients.pop(client_socket, None)
        usernames.pop(client_socket, None)
        update_user_list()
        client_socket.close()

def kick_user(target_name):
    for sock, user in usernames.items():
        if user == target_name:
            sock.send("⚠️ You have been kicked by the admin.".encode('utf-8'))
            sock.close()
            return

def send_msg():
    msg = msg_entry.get()
    if msg.strip():
        display_message(f"🟢 Server: {msg}")
        broadcast(f"🟢 Server: {msg}")
        msg_entry.delete(0, tk.END)

tk.Button(root, text="Send", command=send_msg, bg="#007acc", fg="white").pack(pady=(0,10))

# Socket Setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

display_message("🚀 Server started... Waiting for clients...")

def accept_clients():
    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

threading.Thread(target=accept_clients, daemon=True).start()

root.mainloop()
