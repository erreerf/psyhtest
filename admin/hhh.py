import socket
from cryptography.fernet import Fernet
import matplotlib.pyplot as plt
import random

key = b'lsfldLWochWnSPjPTraJ5UFzyp8vShEpYUJOPZZwLoM='  # Ваш ключ
cipher = Fernet(key)

def send_password(password):
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    encrypted_password = cipher.encrypt(password.encode())
    client_socket.sendall(encrypted_password)

    response = client_socket.recv(4096)
    decoded_response = response.decode()

    print("Ответ от сервера:", decoded_response)

    with open('dan.txt', 'a') as file:  # 'a' для добавления в конец файла
        file.write(decoded_response + '\n')

    client_socket.close()

def clean_file(input_filename):
    try:
        with open(input_filename, 'r') as file:
            lines = file.readlines()

        non_empty_lines = [line for line in lines if line.strip()]

        with open(input_filename, 'w') as file:
            file.writelines(non_empty_lines)

    except Exception as e:
        print("Ошибка при очистке файла:", e)

def decrypt_file(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as file:
            encrypted_lines = file.readlines()

        decrypted_lines = []

        for line in encrypted_lines:
            encrypted_message = line.strip().encode()
            decrypted_message = cipher.decrypt(encrypted_message).decode()
            decrypted_lines.append(decrypted_message)
            print("Расшифрованное сообщение:", decrypted_message)

        with open(output_filename, 'w') as file:
            for decrypted_message in decrypted_lines:
                file.write(decrypted_message + '\n')

    except Exception as e:
        print("Ошибка при дешифровке файла:", e)

def generate_random_color():
    while True:
        r, g, b = random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)
        if (r + g + b) < 550:  # Если сумма каналов меньше 550, цвет не будет слишком светлым
            return (r / 255, g / 255, b / 255)

def plot_data_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = file.readlines()

        plt.figure(figsize=(12, 6))

        for index, line in enumerate(data):
            values = [float(num) for num in line.strip().split()]

            if len(values) != 30:
                print(f"Ошибка: в строке {index + 1} ожидается ровно 30 значений.")
                continue

            x = list(range(1, 31))
            y = values

            if any(value < 1 or value > 10 for value in y):
                print(f"Ошибка: в строке {index + 1} значения Y должны быть в диапазоне от 1 до 10.")
                continue

            random_color = generate_random_color()
            plt.plot(x, y, marker='o', color=random_color, label=f'Ученик {index + 1}')

        plt.title('Графики данных из файла des.txt')
        plt.xlabel('Номер вопроса')
        plt.ylabel('Ответ')
        plt.xticks(x)
        plt.yticks(range(1, 11))
        plt.grid(True)
        plt.legend(loc='upper right')
        plt.savefig('plot_combined.png')
        plt.show()

    except Exception as e:
        print("Ошибка при построении графика:", e)

if __name__ == "__main__":
    password = input("Введите пароль: ")
    send_password(password)

    clean_file('dan.txt')

    decrypt_file('dan.txt', 'des.txt')

    plot_data_from_file('des.txt')
