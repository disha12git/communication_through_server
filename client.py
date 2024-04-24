import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from threading import Thread


class ClientEmployeeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client Side Application")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.text_area = QTextEdit()
        self.layout.addWidget(self.text_area)

        self.input_field = QLineEdit()
        self.layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.host = '127.0.0.1'
        self.port = 65432
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.employee_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.start_connections()

    def start_connections(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.text_area.append(f"Connected to server at {self.host}:{self.port}")
        except ConnectionRefusedError:
            self.text_area.append("Connection refused for client. Make sure the server is running.")

        try:
            self.employee_socket.connect((self.host, self.port))
            self.text_area.append(f"Connected to server at {self.host}:{self.port}")
        except ConnectionRefusedError:
            self.text_area.append("Connection refused for employee. Make sure the server is running.")

        # Start separate threads for handling client and employee messages
        client_thread = Thread(target=self.receive_messages, args=(self.client_socket,))
        employee_thread = Thread(target=self.receive_messages, args=(self.employee_socket,))
        client_thread.start()
        employee_thread.start()

    def receive_messages(self, socket):
        while True:
            try:
                received_message = socket.recv(1024).decode("utf-8")
                if received_message:
                    self.text_area.append(received_message)
            except ConnectionResetError:
                self.text_area.append("Connection with server reset unexpectedly.")
                break

    def send_message(self):
        message_to_send = self.input_field.text()
        self.input_field.clear()

        self.text_area.append("You: " + message_to_send)

        if message_to_send.strip().lower() == "exit":
            self.text_area.append("Exiting...")
            self.client_socket.close()
            self.employee_socket.close()
            return

        # Send message to client
        self.client_socket.sendall(message_to_send.encode("utf-8"))
        # Send message to employee
        self.employee_socket.sendall(message_to_send.encode("utf-8"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_employee_window = ClientEmployeeApp()
    client_employee_window.show()
    sys.exit(app.exec_())
