from PyQt5.QtCore import QTime

# Configuración de ventana (mismas variables que en tus archivos)
win_x, win_y = 100, 100
win_width, win_height = 1000, 600

# Pantalla 1 - Login
txt_title = 'Gestión Monetaria'
txt_hello = '¡Bienvenido a su Sistema de Gestión Monetaria!'
txt_instruction = ('Esta aplicación le permite llevar un registro diario de sus movimientos monetarios.\n'
                   'Podrá registrar envíos y recepciones de divisas, consultar su historial de movimientos\n'
                   'y ver sus saldos actualizados en tiempo real.\n\n'
                   'Por favor, inicie sesión con sus credenciales para continuar.')
txt_next = 'Iniciar Sesión'
txt_register = 'Registrarse'

# Campos de login
txt_name = 'Nombre:'
txt_lastname = 'Apellido:'
txt_pin = 'PIN (4 dígitos):'
txt_hintname = "Ingrese su nombre"
txt_hintlastname = "Ingrese su apellido"

# Pantalla 2 - Menú Principal
txt_menu_title = 'Menú Principal'
txt_welcome = '¿Qué desea hacer hoy?'
txt_new_transaction = 'Nuevo Movimiento'
txt_view_history = 'Ver Movimientos'
txt_view_balance = 'Ver Saldos'
txt_logout = 'Cerrar Sesión'

# Pantalla 3 - Transacciones
txt_transaction_title = 'Registrar Movimiento'
txt_type = 'Tipo de movimiento:'
txt_send = 'Enviar Dinero'
txt_receive = 'Recibir Dinero'
txt_currency = 'Moneda:'
txt_amount = 'Monto:'
txt_counterparty = 'Contraparte:'
txt_description = 'Descripción:'
txt_save = 'Guardar Movimiento'
txt_back = 'Volver al Menú'

# Pantalla 4 - Historial
txt_history_title = 'Historial de Movimientos'
txt_filter_type = 'Filtrar por tipo:'
txt_filter_currency = 'Filtrar por moneda:'
txt_all = 'Todos'
txt_send_filter = 'Envíos'
txt_receive_filter = 'Recepciones'
txt_all_currencies = 'Todas las monedas'

# Pantalla 5 - Saldos
txt_balance_title = 'Saldos por Divisa'
txt_total_received = 'Total Recibido:'
txt_total_sent = 'Total Enviado:'
txt_net_balance = 'Balance Neto:'

# Resultados y mensajes
txt_index = 'Índice de Ruffier: '  # Mantenido por compatibilidad
txt_workheart = 'Rendimiento cardíaco: '  # Mantenido por compatibilidad
txt_res1 = "bajo. ¡Acuda al médico de inmediato!"
txt_res2 = "satisfactorio. ¡Vea a su médico!"
txt_res3 = "promedio. Puede valer la pena ver a su médico para que lo revise."
txt_res4 = "por encima del promedio"
txt_res5 = "alto"

# Configuración de tiempo (mantenido de tus archivos)
time = QTime(0, 0, 15)
txt_timer = time.toString("hh:mm:ss")