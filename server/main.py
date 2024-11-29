import socket
import threading
from cryptography.fernet import Fernet


key = b'lsfldLWochWnSPjPTraJ5UFzyp8vShEpYUJOPZZwLoM='
cipher = Fernet(key)

connected_clients = set()

def handle_client(conn, addr):
    client_id = f"{addr[0]}:{addr[1]}"

    if client_id in connected_clients:
        print(f"Подключение от {client_id} отклонено: уже отправил данные.")
        conn.sendall(b"You have already submitted your answers.")
        conn.close()
        return

    print(f"Подключение от {client_id}")

    encrypted_message = conn.recv(1024)

    try:
        message = cipher.decrypt(encrypted_message).decode()
        mc = message.replace(" ", "")
        if mc.isdigit():

            encrypted_data_to_save = cipher.encrypt(message.encode())
            with open('log.txt', 'ab') as log_file:
                log_file.write(encrypted_data_to_save + b'\n')

            print("Данные сохранены в log.txt")
            connected_clients.add(client_id)
            conn.sendall(b"Thank you for your submission.")

        else:
            with open('log.txt', 'rb') as log_file:
                first_line_encrypted = log_file.readline().strip()
                message_first_line = cipher.decrypt(first_line_encrypted).decode()
                print(f"Первая строка (декодированная): {message_first_line}")

                encrypted_check_message = cipher.encrypt(message.encode())

            if message == ("p" + message_first_line):
                print("Сообщение совпадает с первой строкой. Отправка файла.")
                with open('log.txt', 'rb') as log_file:
                    log_file.seek(0)
                    log_file.readline()
                    data_to_send = log_file.read()
                    conn.sendall(data_to_send)
            else:
                conn.sendall(b"Invalid message.", )

    except Exception as e:
        print(f"Ошибка: {e}")
        conn.sendall(b"Failed to process your request.")

    conn.close()

def start_server():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Сервер запущен на {host}:{port}. Ожидание подключения...")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()