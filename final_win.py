from PyQt5.QtCore import Qt, QTimer, QTime, QLocale
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QFont
from PyQt5.QtWidgets import (
       QApplication, QWidget,
       QHBoxLayout, QVBoxLayout, QGridLayout,
       QGroupBox, QRadioButton,
       QPushButton, QLabel, QListWidget, QLineEdit,
       QComboBox, QDoubleSpinBox, QTableWidget, QTableWidgetItem,
       QHeaderView, QMessageBox, QFrame)

from instr import *
from my_app import transactions_db


class FinalWin(QWidget):
   def __init__(self, exp, mode="transaction"):
       ''' la ventana de transacciones, historial o saldos '''
       super().__init__()

       self.exp = exp
       self.mode = mode
       self.user_id = exp.user_id

       # creando y configurando elementos gráficos
       self.initUI()

       # establece la apariencia de la ventana (etiqueta, tamaño, ubicación)
       self.set_appear()
      
       # inicio:
       self.show()

   def set_appear(self):
       ''' establece la apariencia de la ventana (etiqueta, tamaño, ubicación) '''
       if self.mode == "transaction":
           self.setWindowTitle(txt_transaction_title)
       elif self.mode == "history":
           self.setWindowTitle(txt_history_title)
       else:
           self.setWindowTitle(txt_balance_title)
       self.resize(win_width, win_height)
       self.move(win_x, win_y)

   def initUI(self):
       ''' crea elementos gráficos según el modo '''
       if self.mode == "transaction":
           self.init_transaction_ui()
       elif self.mode == "history":
           self.init_history_ui()
       else:
           self.init_balance_ui()

   def init_transaction_ui(self):
       ''' interfaz para nueva transacción '''
       self.text_type = QLabel(txt_type)
       self.combo_type = QComboBox()
       self.combo_type.addItems([txt_send, txt_receive])
       
       self.text_currency = QLabel(txt_currency)
       self.combo_currency = QComboBox()
       self.combo_currency.addItems(["USD", "EUR", "GBP", "MXN", "ARS", "COP", "CLP", "PEN", "OTRA"])
       self.combo_currency.setEditable(True)
       
       self.text_amount = QLabel(txt_amount)
       self.spin_amount = QDoubleSpinBox()
       self.spin_amount.setRange(0, 999999999)
       self.spin_amount.setDecimals(2)
       self.spin_amount.setPrefix("$ ")
       
       self.text_counterparty = QLabel(txt_counterparty)
       self.line_counterparty = QLineEdit()
       
       self.text_description = QLabel(txt_description)
       self.line_description = QLineEdit()
       
       self.btn_save = QPushButton(txt_save)
       self.btn_back = QPushButton(txt_back)
       
       self.layout = QVBoxLayout()
       self.layout.addWidget(self.text_type)
       self.layout.addWidget(self.combo_type)
       self.layout.addWidget(self.text_currency)
       self.layout.addWidget(self.combo_currency)
       self.layout.addWidget(self.text_amount)
       self.layout.addWidget(self.spin_amount)
       self.layout.addWidget(self.text_counterparty)
       self.layout.addWidget(self.line_counterparty)
       self.layout.addWidget(self.text_description)
       self.layout.addWidget(self.line_description)
       
       btn_layout = QHBoxLayout()
       btn_layout.addWidget(self.btn_back)
       btn_layout.addWidget(self.btn_save)
       self.layout.addLayout(btn_layout)
       
       self.setLayout(self.layout)
       
       # Conexiones
       self.btn_save.clicked.connect(self.save_transaction)
       self.btn_back.clicked.connect(self.back_to_menu)

   def init_history_ui(self):
       ''' interfaz para ver historial '''
       # Filtros
       filter_layout = QHBoxLayout()
       self.combo_filter_type = QComboBox()
       self.combo_filter_type.addItems([txt_all, txt_send_filter, txt_receive_filter])
       self.combo_filter_type.currentTextChanged.connect(self.load_history)
       
       self.combo_filter_currency = QComboBox()
       self.combo_filter_currency.addItem(txt_all_currencies)
       # Agregar monedas existentes
       currencies = set()
       for trans in transactions_db.get(self.user_id, []):
           currencies.add(trans["currency"])
       self.combo_filter_currency.addItems(sorted(currencies))
       self.combo_filter_currency.currentTextChanged.connect(self.load_history)
       
       filter_layout.addWidget(QLabel(txt_filter_type))
       filter_layout.addWidget(self.combo_filter_type)
       filter_layout.addStretch()
       filter_layout.addWidget(QLabel(txt_filter_currency))
       filter_layout.addWidget(self.combo_filter_currency)
       
       # Tabla
       self.table = QTableWidget()
       self.table.setColumnCount(5)
       self.table.setHorizontalHeaderLabels(["Tipo", "Monto", "Moneda", "Contraparte", "Descripción"])
       self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
       
       self.btn_back = QPushButton(txt_back)
       
       self.layout = QVBoxLayout()
       self.layout.addLayout(filter_layout)
       self.layout.addWidget(self.table)
       self.layout.addWidget(self.btn_back)
       
       self.setLayout(self.layout)
       
       self.load_history()
       self.btn_back.clicked.connect(self.back_to_menu)

   def init_balance_ui(self):
       ''' interfaz para ver saldos '''
       self.layout = QVBoxLayout()
       
       title = QLabel(txt_balance_title)
       title.setFont(QFont("Times", 20, QFont.Bold))
       title.setAlignment(Qt.AlignCenter)
       self.layout.addWidget(title)
       
       # Calcular saldos
       balance = self.calculate_balance()
       
       if not balance:
           no_data = QLabel("No hay movimientos registrados")
           no_data.setAlignment(Qt.AlignCenter)
           self.layout.addWidget(no_data)
       else:
           total_rec = 0
           total_sent = 0
           
           for currency, amount in sorted(balance.items()):
               frame = QFrame()
               frame.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px;")
               frame_layout = QHBoxLayout(frame)
               
               curr_label = QLabel(f"💱 {currency}")
               curr_label.setFont(QFont("Times", 16, QFont.Bold))
               
               amount_label = QLabel(f"{amount:,.2f}")
               amount_label.setFont(QFont("Times", 18, QFont.Bold))
               
               if amount > 0:
                   amount_label.setStyleSheet("color: rgb(0, 200, 0);")
                   total_rec += amount
               elif amount < 0:
                   amount_label.setStyleSheet("color: rgb(200, 0, 0);")
                   total_sent += abs(amount)
               else:
                   amount_label.setStyleSheet("color: rgb(100, 100, 100);")
               
               frame_layout.addWidget(curr_label)
               frame_layout.addStretch()
               frame_layout.addWidget(amount_label)
               
               self.layout.addWidget(frame)
           
           # Resumen
           summary = QLabel(f"{txt_total_received} {total_rec:,.2f} | {txt_total_sent} {total_sent:,.2f} | {txt_net_balance} {total_rec - total_sent:,.2f}")
           summary.setAlignment(Qt.AlignCenter)
           summary.setFont(QFont("Times", 12))
           self.layout.addWidget(summary)
       
       self.btn_back = QPushButton(txt_back)
       self.layout.addWidget(self.btn_back)
       
       self.setLayout(self.layout)
       self.btn_back.clicked.connect(self.back_to_menu)

   def calculate_balance(self):
       ''' calcula el saldo por moneda '''
       balance = {}
       for trans in transactions_db.get(self.user_id, []):
           curr = trans["currency"]
           if curr not in balance:
               balance[curr] = 0
           if trans["type"] == "receive":
               balance[curr] += trans["amount"]
           else:
               balance[curr] -= trans["amount"]
       return balance

   def save_transaction(self):
       ''' guarda una nueva transacción '''
       trans_type = "send" if self.combo_type.currentIndex() == 0 else "receive"
       currency = self.combo_currency.currentText().upper()
       amount = self.spin_amount.value()
       counterparty = self.line_counterparty.text().strip()
       description = self.line_description.text().strip()
       
       if amount <= 0:
           QMessageBox.warning(self, "Error", "El monto debe ser mayor a cero")
           return
       
       if not counterparty:
           QMessageBox.warning(self, "Error", "Ingrese la contraparte")
           return
       
       transaction = {
           "type": trans_type,
           "amount": amount,
           "currency": currency,
           "counterparty": counterparty,
           "description": description
       }
       
       if self.user_id not in transactions_db:
           transactions_db[self.user_id] = []
       
       transactions_db[self.user_id].append(transaction)
       
       QMessageBox.information(self, "Éxito", "Movimiento registrado correctamente")
       self.back_to_menu()

   def load_history(self):
       ''' carga el historial filtrado '''
       self.table.setRowCount(0)
       
       filter_type = self.combo_filter_type.currentText()
       filter_curr = self.combo_filter_currency.currentText()
       
       row = 0
       for trans in transactions_db.get(self.user_id, []):
           # Aplicar filtros
           if filter_type == txt_send_filter and trans["type"] != "send":
               continue
           if filter_type == txt_receive_filter and trans["type"] != "receive":
               continue
           if filter_curr != txt_all_currencies and trans["currency"] != filter_curr:
               continue
           
           self.table.insertRow(row)
           
           # Tipo
           type_text = "📤 Envío" if trans["type"] == "send" else "📥 Recepción"
           type_item = QTableWidgetItem(type_text)
           if trans["type"] == "send":
               type_item.setForeground(Qt.red)
           else:
               type_item.setForeground(Qt.green)
           self.table.setItem(row, 0, type_item)
           
           # Monto
           amount_item = QTableWidgetItem(f"{trans['amount']:,.2f}")
           amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
           self.table.setItem(row, 1, amount_item)
           
           # Moneda
           self.table.setItem(row, 2, QTableWidgetItem(trans["currency"]))
           
           # Contraparte
           self.table.setItem(row, 3, QTableWidgetItem(trans["counterparty"]))
           
           # Descripción
           self.table.setItem(row, 4, QTableWidgetItem(trans["description"]))
           
           row += 1

   def back_to_menu(self):
       ''' vuelve al menú principal '''
       self.hide()
       from second_win import TestWin
       self.tw = TestWin(self.user_id, self.exp.first_name, self.exp.last_name)