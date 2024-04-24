import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from threading import Thread


class EmployeeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee side Application")
        self.setGeometry(100, 100, 400, 300)

        # Apply style sheet for a more attractive appearance
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QTextEdit, QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.text_area = QTextEdit()
        self.layout.addWidget(self.text_area)

        self.input_field = QLineEdit()
        self.layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.host = '127.0.0.1'  # Change to your server host
        self.port = 65432  # Change to your server port
        self.employee_socket = None

        self.start_connection()

    def start_connection(self):
        self.employee_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.employee_socket.connect((self.host, self.port))
            self.text_area.append(f"Connected to server at {self.host}:{self.port}")
        except ConnectionRefusedError:
            self.text_area.append("Connection refused. Make sure the server is running.")

        # Start a separate thread to receive messages from the server
        self.receive_thread = Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                received_message = self.employee_socket.recv(1024).decode("utf-8")
                if received_message:
                    self.text_area.append("Server: " + received_message)
            except ConnectionResetError:
                self.text_area.append("Connection with server reset unexpectedly.")
                break

    def send_message(self):
        message_to_send = self.input_field.text()
        self.input_field.clear()

        self.text_area.append("You: " + message_to_send)

        if message_to_send.strip().lower() == "exit":
            self.text_area.append("Exiting...")
            self.employee_socket.close()
            return

        # Send message to the server
        self.employee_socket.sendall(message_to_send.encode("utf-8"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    employee_window = EmployeeApp()
    employee_window.show()
    sys.exit(app.exec_())
