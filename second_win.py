from PyQt5.QtCore import Qt, QTimer, QTime, QLocale
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QFont
from PyQt5.QtWidgets import (
       QApplication, QWidget,
       QHBoxLayout, QVBoxLayout, QGridLayout,
       QGroupBox, QRadioButton,
       QPushButton, QLabel, QListWidget, QLineEdit,
       QComboBox, QDoubleSpinBox, QTableWidget, QTableWidgetItem,
       QHeaderView, QMessageBox)

from instr import *
from final_win import *
from my_app import transactions_db


class Experiment():
   ''' Clase para pasar datos entre ventanas (como en tu ejemplo) '''
   def __init__(self, user_id, first_name, last_name):
       self.user_id = user_id
       self.first_name = first_name
       self.last_name = last_name


class TestWin(QWidget):
   def __init__(self, user_id, first_name, last_name):
       ''' la ventana del menú principal '''
       super().__init__()

       self.user_id = user_id
       self.first_name = first_name
       self.last_name = last_name
       self.exp = Experiment(user_id, first_name, last_name)

       # creando y configurando elementos gráficos
       self.initUI()

       # establece la conexión entre los elementos
       self.connects()

       # establece la apariencia de la ventana (etiqueta, tamaño, ubicación)
       self.set_appear()
      
       # inicio:
       self.show()

   def set_appear(self):
       ''' establece la apariencia de la ventana (etiqueta, tamaño, ubicación) '''
       self.setWindowTitle(txt_menu_title)
       self.resize(win_width, win_height)
       self.move(win_x, win_y)

   def initUI(self):
       ''' crea elementos gráficos del menú principal '''
       self.welcome_text = QLabel(f"¡Hola {self.first_name} {self.last_name}!\n{txt_welcome}")
       self.welcome_text.setFont(QFont("Times", 18, QFont.Bold))
       
       # Botones del menú
       self.btn_new = QPushButton(txt_new_transaction)
       self.btn_history = QPushButton(txt_view_history)
       self.btn_balance = QPushButton(txt_view_balance)
       self.btn_logout = QPushButton(txt_logout)
       
       # Estilo para botones grandes
       for btn in [self.btn_new, self.btn_history, self.btn_balance, self.btn_logout]:
           btn.setMinimumHeight(80)
           btn.setFont(QFont("Times", 14))

       self.layout = QVBoxLayout()
       self.layout.addWidget(self.welcome_text, alignment=Qt.AlignCenter)
       self.layout.addWidget(self.btn_new)
       self.layout.addWidget(self.btn_history)
       self.layout.addWidget(self.btn_balance)
       self.layout.addWidget(self.btn_logout)
       
       self.setLayout(self.layout)

   def next_click(self):
       ''' abre pantalla de nueva transacción '''
       self.hide()
       self.fw = FinalWin(self.exp, mode="transaction")

   def history_click(self):
       ''' abre pantalla de historial '''
       self.hide()
       self.fw = FinalWin(self.exp, mode="history")

   def balance_click(self):
       ''' abre pantalla de saldos '''
       self.hide()
       self.fw = FinalWin(self.exp, mode="balance")

   def logout_click(self):
       ''' cierra sesión y vuelve al login '''
       self.hide()
       from my_app import MainWin
       self.mw = MainWin()

   def connects(self):
       self.btn_new.clicked.connect(self.next_click)
       self.btn_history.clicked.connect(self.history_click)
       self.btn_balance.clicked.connect(self.balance_click)
       self.btn_logout.clicked.connect(self.logout_click)