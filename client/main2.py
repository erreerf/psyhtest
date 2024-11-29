import sys
import socket
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt


key = b'lsfldLWochWnSPjPTraJ5UFzyp8vShEpYUJOPZZwLoM='
cipher = Fernet(key)


class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ответы на вопросы")
        self.setFixedSize(600, 500)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.questions = [
            "Насколько часто вы чувствуете себя подавленным или унылым?\n1 - Никогда\n10 - Постоянно",
            "Как вы оцениваете свою способность справляться со стрессом?\n1 - Очень плохо\n10 - Отлично",
            "Насколько вы чувствительны к критике?\n1 - Совсем не чувствителен\n10 - Очень чувствителен",
            "Как часто вы испытываете тревогу или беспокойство?\n1 - Никогда\n10 - Постоянно",
            "Насколько легко вы теряете интерес к любимым занятиям?\n1 - Очень сложно\n10 - Очень легко",
            "Как вы оцениваете свои навыки управления эмоциями?\n1 - Очень низкие\n10 - Очень высокие",
            "Насколько вы уверены в своем будущем?\n1 - Совсем не уверен\n10 - Полностью уверен",
            "Как часто вы чувствуете себя уставшим или истощенным?\n1 - Никогда\n10 - Постоянно",
            "Как вы оцениваете свою способность сосредотачиваться на задачах?\n1 - Очень плохо\n10 - Отлично",
            "Насколько часто вы испытываете чувство безнадежности?\n1 - Никогда\n10 - Постоянно",
            "Как вы оцениваете свои навыки общения с другими людьми?\n1 - Очень низкие\n10 - Очень высокие",
            "Насколько легко вы справляетесь с изменениями в жизни?\n1 - Очень сложно\n10 - Очень легко",
            "Как вы оцениваете свою самооценку?\n1 - Очень низкая\n10 - Очень высокая",
            "Как часто вы чувствуете себя одиноким?\n1 - Никогда\n10 - Постоянно",
            "Насколько вы открыты к новым идеям и опыту?\n1 - Совсем не открыты\n10 - Очень открыты",
            "Как вы оцениваете свою способность просить о помощи?\n1 - Очень низкая\n10 - Очень высокая",
            "Как часто вы испытываете гнев или раздражение?\n1 - Никогда\n10 - Постоянно",
            "Насколько вы уверены в своих социальных навыках?\n1 - Совсем не уверен\n10 - Полностью уверен",
            "Как вы оцениваете свою способность справляться с неудачами?\n1 - Очень плохо\n10 - Отлично",
            "Насколько вы эмоционально близки к своей семье и друзьям?\n1 - Совсем не близки\n10 - Очень близки",
            "Как часто вы испытываете физические симптомы стресса (например, головную боль)?\n1 - Никогда\n10 - Постоянно",
            "Насколько вы уверены в своем мнении и суждениях?\n1 - Совсем не уверен\n10 - Полностью уверен",
            "Как вы оцениваете свою способность к саморазвитию?\n1 - Очень низкая\n10 - Очень высокая",
            "Насколько вы счастливы в своей жизни в целом?\n1 - Совсем не счастливы\n10 - Очень счастливы",
            "Как часто вы испытываете страх перед будущим?\n1 - Никогда\n10 - Постоянно",
            "Как вы оцениваете свою способность прощать других?\n1 - Очень низкая\n10 - Очень высокая",
            "Насколько вы эмоционально устойчивы в сложных ситуациях?\n1 - Совсем не устойчив\n10 - Очень устойчив",
            "Как часто вы стремитесь к позитивным изменениям в своей жизни?\n1 - Никогда\n10 - Постоянно",
            "Насколько вы уверены в своих творческих способностях?\n1 - Совсем не уверен\n10 - Полностью уверен",
            "Как вы оцениваете свою способность к самоорганизации?\n1 - Очень низкая\n10 - Очень высокая"
        ]

        self.answers = []
        self.current_question = 0

        self.question_label = QLabel(self.questions[self.current_question])
        self.question_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.question_label)

        self.answer_input = QLineEdit()
        self.answer_input.setFixedHeight(40)
        self.answer_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.answer_input)

        self.submit_button = QPushButton("Отправить")
        self.submit_button.setFixedHeight(40)
        self.submit_button.setStyleSheet("font-size: 16px;")
        self.submit_button.clicked.connect(self.submit_answer)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        self.answer_input.setFocus()

    def submit_answer(self):
        answer = self.answer_input.text()
        if answer.isdigit() and 1 <= int(answer) <= 10:
            if self.current_question in [1, 4, 6, 9, 12, 18, 20, 26]:
                self.answers.append(str(10 - int(answer)))
            else:
                self.answers.append(answer)

            self.answer_input.clear()
            self.current_question += 1

            if self.current_question < len(self.questions):
                self.question_label.setText(self.questions[self.current_question])
                self.answer_input.setFocus()
            else:
                self.send_answers()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите число от 1 до 10.")
            self.answer_input.clear()
            self.answer_input.setFocus()

    def send_answers(self):
        host = '127.0.0.1'
        port = 12345

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        message = ' '.join(self.answers)
        encrypted_message = cipher.encrypt(message.encode())
        client_socket.sendall(encrypted_message)

        client_socket.close()
        QMessageBox.information(self, "Успех", "Ответы успешно отправлены.")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ClientApp()
    client.show()
    sys.exit(app.exec_())
