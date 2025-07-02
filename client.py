import socket
import threading
import customtkinter as ctk
from tkinter import simpledialog


class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Socket Chat")
        self.root.geometry("500x550")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Получение ника
        self.username = simpledialog.askstring("Нікнейм", "Введіть нікнейм:", parent=root)
        if not self.username:
            self.username = "Гість"

        # Подключение к серверу (ручной ввод IP и порта)
        self.server_ip = simpledialog.askstring("IP сервера", "Введіть IP сервера (за замовченням 127.0.0.1):", parent=root)
        self.server_ip = self.server_ip if self.server_ip else "127.0.0.1"

        self.server_port = simpledialog.askinteger("Порт сервера", "Введіть порт (за замовченням 12345):", parent=root)
        self.server_port = self.server_port if self.server_port else "12345"

        # GUI
        self.messages_frame = ctk.CTkTextbox(root, width=480, height=400)
        self.messages_frame.pack(pady=10)
        self.messages_frame.configure(state="disabled")

        self.entry = ctk.CTkEntry(root, width=360)
        self.entry.pack(side="left", padx=(10, 0), pady=(0, 10))
        self.entry.bind("<Return>", self.send_message)
        self.entry.focus()

        self.send_button = ctk.CTkButton(root, text="Відправити", command=self.send_message)
        self.send_button.pack(side="left", padx=10, pady=(0, 10))

        # Сокет
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
        except ConnectionRefusedError:
            print("Не вдалось підключитись до сервера")
            self.root.destroy()
            return

        self.running = True
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        message = self.entry.get().strip()
        if message:
            full_message = f"{self.username}: {message}"
            try:
                self.client_socket.send(full_message.encode())
            except:
                pass
            self.entry.delete(0, ctk.END)

    def receive_messages(self):
        while self.running:
            try:
                msg = self.client_socket.recv(1024).decode()
                if msg:
                    self.messages_frame.configure(state="normal")
                    if msg.startswith(f"{self.username}:"):
                        self.messages_frame.insert("end", f"Вы: {msg.split(':', 1)[1]}\n")
                    else:
                        self.messages_frame.insert("end", msg + "\n")
                    self.messages_frame.configure(state="disabled")
                    self.messages_frame.yview("end")
            except:
                self.running = False
                break

    def on_closing(self):
        self.running = False
        try:
            self.client_socket.shutdown(socket.SHUT_RDWR)
            self.client_socket.close()
        except:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
