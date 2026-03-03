from PyQt5.QtCore import Qt, QTimer, QTime, QLocale
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QFont
from PyQt5.QtWidgets import (
       QApplication, QWidget,
       QHBoxLayout, QVBoxLayout, QGridLayout,
       QGroupBox, QRadioButton,
       QPushButton, QLabel, QListWidget, QLineEdit,
       QSpinBox, QMessageBox)

from instr import *
from second_win import *

# Base de datos simple (simulando persistencia)
users_db = {}  # {user_id: {"first_name": str, "last_name": str, "pin": str}}
transactions_db = {}  # {user_id: [{"type": str, "amount": float, "currency": str, "counterparty": str, "description": str}]}


class MainWin(QWidget):
   def __init__(self):
       ''' la ventana de inicio de sesión '''
       super().__init__()

       # establece la apariencia de la ventana (etiqueta, tamaño, ubicación)
       self.set_appear()

       # creando y configurando elementos gráficos
       self.initUI()

       # establece la conexión entre los elementos
       self.connects()

       # inicio:
       self.show()

   def initUI(self):
       ''' crea elementos gráficos '''
       self.hello_text = QLabel(txt_hello)
       self.instruction = QLabel(txt_instruction)
       
       # Campos de login
       self.text_name = QLabel(txt_name)
       self.text_lastname = QLabel(txt_lastname)
       self.text_pin = QLabel(txt_pin)
       
       self.line_name = QLineEdit(txt_hintname)
       self.line_lastname = QLineEdit(txt_hintlastname)
       
       # PIN de 4 dígitos usando QSpinBox (como en tu ejemplo)
       self.pin_digits = []
       pin_layout = QHBoxLayout()
       for i in range(4):
           spin = QSpinBox()
           spin.setRange(0, 9)
           spin.setWrapping(True)
           spin.setAlignment(Qt.AlignCenter)
           spin.setFixedSize(50, 50)
           self.pin_digits.append(spin)
           pin_layout.addWidget(spin)
       
       self.pin_widget = QWidget()
       self.pin_widget.setLayout(pin_layout)
       
       self.btn_login = QPushButton(txt_next)
       self.btn_register = QPushButton(txt_register)

       self.layout = QVBoxLayout()
       self.layout.addWidget(self.hello_text, alignment=Qt.AlignCenter)
       self.layout.addWidget(self.instruction, alignment=Qt.AlignCenter)
       self.layout.addWidget(self.text_name, alignment=Qt.AlignLeft)
       self.layout.addWidget(self.line_name, alignment=Qt.AlignLeft)
       self.layout.addWidget(self.text_lastname, alignment=Qt.AlignLeft)
       self.layout.addWidget(self.line_lastname, alignment=Qt.AlignLeft)
       self.layout.addWidget(self.text_pin, alignment=Qt.AlignLeft)
       self.layout.addWidget(self.pin_widget, alignment=Qt.AlignCenter)
       
       btn_layout = QHBoxLayout()
       btn_layout.addWidget(self.btn_login)
       btn_layout.addWidget(self.btn_register)
       self.layout.addLayout(btn_layout)
       
       self.setLayout(self.layout)

   def get_pin(self):
       ''' obtiene el PIN de los 4 spinboxes '''
       return "".join(str(digit.value()) for digit in self.pin_digits)

   def next_click(self):
       ''' maneja el inicio de sesión '''
       first = self.line_name.text().strip()
       last = self.line_lastname.text().strip()
       pin = self.get_pin()
       
       if not all([first, last, pin]):
           QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
           return
       
       user_id = f"{first.lower()}_{last.lower()}"
       
       if user_id in users_db and users_db[user_id]["pin"] == pin:
           self.hide()
           self.tw = TestWin(user_id, first, last)
       else:
           QMessageBox.warning(self, "Error", "Credenciales incorrectas")

   def register_click(self):
       ''' maneja el registro de nuevos usuarios '''
       first = self.line_name.text().strip()
       last = self.line_lastname.text().strip()
       pin = self.get_pin()
       
       if not all([first, last, pin]):
           QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
           return
       
       if len(pin) != 4 or not pin.isdigit():
           QMessageBox.warning(self, "Error", "El PIN debe ser de 4 dígitos numéricos")
           return
       
       user_id = f"{first.lower()}_{last.lower()}"
       
       if user_id in users_db:
           QMessageBox.warning(self, "Error", "El usuario ya existe")
           return
       
       # Registrar nuevo usuario
       users_db[user_id] = {
           "first_name": first,
           "last_name": last,
           "pin": pin
       }
       transactions_db[user_id] = []
       
       QMessageBox.information(self, "Éxito", "Usuario registrado correctamente")
       
       # Limpiar campos
       self.line_name.clear()
       self.line_lastname.clear()
       for digit in self.pin_digits:
           digit.setValue(0)

   def connects(self):
       self.btn_login.clicked.connect(self.next_click)
       self.btn_register.clicked.connect(self.register_click)

   def set_appear(self):
       ''' establece la apariencia de la ventana (etiqueta, tamaño, ubicación) '''
       self.setWindowTitle(txt_title)
       self.resize(win_width, win_height)
       self.move(win_x, win_y)


def main():
   app = QApplication([])
   mw = MainWin()
   app.exec_()


if __name__ == "__main__":
   main()