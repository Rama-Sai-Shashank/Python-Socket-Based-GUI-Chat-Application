import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

HOST = 'localhost'  # Change to server IP for LAN/internet use
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

root = tk.Tk()
root.withdraw()
username = simpledialog.askstring("Username", "Enter your name:")
client.send(username.encode('utf-8'))

chat_win = tk.Tk()
chat_win.title(f"{username}'s Chat")
chat_win.geometry("450x550")
chat_win.configure(bg="#1e1e1e")

chat_display = scrolledtext.ScrolledText(chat_win, wrap=tk.WORD, bg="#2d2d2d", fg="#ffffff", font=("Consolas", 12))
chat_display.config(state='disabled')
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

msg_entry = tk.Entry(chat_win, font=("Consolas", 12), bg="#3a3a3a", fg="#ffffff")
msg_entry.pack(padx=10, pady=(0,10), fill=tk.X)

def display_message(msg):
    chat_display.config(state='normal')
    chat_display.insert(tk.END, msg + "\n")
    chat_display.yview(tk.END)
    chat_display.config(state='disabled')

def receive_msg():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            display_message(msg)
        except:
            display_message("⚠️ Disconnected from server.")
            break

def send_msg():
    msg = msg_entry.get()
    if msg.strip():
        client.send(msg.encode('utf-8'))
        msg_entry.delete(0, tk.END)

tk.Button(chat_win, text="Send", command=send_msg, bg="#00b386", fg="white").pack(pady=(0,10))

threading.Thread(target=receive_msg, daemon=True).start()

chat_win.mainloop()
