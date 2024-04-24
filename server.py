import socket
import threading

def handle_connection(client_socket, employee_socket):
    try:
        while True:
            # Receive message from client
            received_message_client = client_socket.recv(1024).decode("utf-8")
            print("Client:", received_message_client)

            # If client sends "exit", close the connection
            if received_message_client.strip().lower() == "exit":
                print("Client requested to close the connection. Closing...")
                break

            # Send message from client to employee
            print("Sending to employee:", received_message_client)
            employee_socket.sendall(received_message_client.encode("utf-8"))

            # Receive message from employee
            received_message_employee = employee_socket.recv(1024).decode("utf-8")
            print("Employee:", received_message_employee)

            # If employee sends "exit", close the connection
            if received_message_employee.strip().lower() == "exit":
                print("Employee requested to close the connection. Closing...")
                break

            # Send message from employee to client
            print("Sending to client:", received_message_employee)
            client_socket.sendall(received_message_employee.encode("utf-8"))
    except ConnectionResetError:
        print("Connection reset unexpectedly.")

    finally:
        # Close sockets after each conversation
        client_socket.close()
        employee_socket.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
        server_socket.listen(5)  # Listen for multiple connections
        print(f"Server listening on {host}:{port}")

        while True:
            # Accept connection from client
            client_socket, client_address = server_socket.accept()
            print(f"Connection from client: {client_address}")

            # Accept connection from employee
            employee_socket, employee_address = server_socket.accept()
            print(f"Connection from employee: {employee_address}")

            # Handle client and employee in separate threads
            client_employee_thread = threading.Thread(target=handle_connection, args=(client_socket, employee_socket))
            client_employee_thread.start()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432  # Change to an available port number
    start_server(HOST, PORT)
