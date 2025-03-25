from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sqlite3
import os

app = Flask(__name__)
# Configurar CORS para permitir cualquier origen y métodos
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}}, supports_credentials=True)

# Configuración JWT
app.config['JWT_SECRET_KEY'] = 'claude-bank-secret-key'  # Cambiar esto en producción
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # No expiración para pruebas
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
jwt = JWTManager(app)

# Asegurar que existe la base de datos
def init_db():
    conn = sqlite3.connect('claude_bank.db')
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        address TEXT,
        email TEXT,
        phone TEXT,
        marketing_consent BOOLEAN DEFAULT 0,
        data_processing_consent BOOLEAN DEFAULT 0,
        third_party_consent BOOLEAN DEFAULT 0
    )
    ''')
    
    # Crear tabla de cuentas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        account_number TEXT UNIQUE NOT NULL,
        balance REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Crear tabla de movimientos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        date TEXT NOT NULL,
        concept TEXT NOT NULL,
        amount REAL NOT NULL,
        balance_after REAL NOT NULL,
        category TEXT,
        is_expense BOOLEAN,
        FOREIGN KEY (account_id) REFERENCES accounts (id)
    )
    ''')
    
    # Insertar datos de ejemplo si no existen
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Insertar usuarios de ejemplo
        cursor.execute("""
            INSERT INTO users (
                username, password, first_name, last_name, address, email, phone,
                marketing_consent, data_processing_consent, third_party_consent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ('usuario1', 'password1', 'Juan', 'Pérez', 'Calle Principal 123', 
              'juan@example.com', '555-123-4567', 1, 1, 0))
        
        cursor.execute("""
            INSERT INTO users (
                username, password, first_name, last_name, address, email, phone,
                marketing_consent, data_processing_consent, third_party_consent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ('usuario2', 'password2', 'María', 'García', 'Avenida Central 456', 
              'maria@example.com', '555-987-6543', 0, 1, 0))
        
        # Insertar cuentas de ejemplo
        cursor.execute("INSERT INTO accounts (user_id, account_number, balance) VALUES (?, ?, ?)", 
                      (1, '10001', 1500.75))
        cursor.execute("INSERT INTO accounts (user_id, account_number, balance) VALUES (?, ?, ?)", 
                      (2, '10002', 2750.50))
        
        # Generar transacciones para usuario1
        account1_id = 1
        balance = 1500.75
        
        # Lista de conceptos para generar movimientos aleatorios
        ingresos = [
            ("Nómina", "Ingreso", 1200.00),
            ("Transferencia recibida", "Ingreso", 150.00),
            ("Devolución Hacienda", "Ingreso", 320.50),
            ("Intereses", "Ingreso", 2.30),
            ("Reembolso", "Ingreso", 45.99)
        ]
        
        gastos = [
            ("Supermercado", "Alimentación", -85.43),
            ("Netflix", "Entretenimiento", -17.99),
            ("Luz", "Hogar", -62.50),
            ("Agua", "Hogar", -35.20),
            ("Internet", "Servicios", -45.00),
            ("Restaurante", "Ocio", -38.50),
            ("Gasolina", "Transporte", -60.00),
            ("Farmacia", "Salud", -22.35),
            ("Transfer", "Diversos", -150.00),
            ("Seguro", "Seguros", -120.00)
        ]
        
        # Generar transacciones para los últimos 3 meses
        import random
        import datetime
        
        # Comenzar hace 3 meses
        start_date = datetime.datetime.now() - datetime.timedelta(days=90)
        
        for i in range(30):  # Generar 30 transacciones
            # Elegir entre un ingreso (20% probabilidad) o un gasto (80% probabilidad)
            if random.random() < 0.2:  # 20% de probabilidad de ingreso
                concept, category, amount = random.choice(ingresos)
                is_expense = False
            else:
                concept, category, amount = random.choice(gastos)
                is_expense = True
            
            # Fecha aleatoria dentro de los últimos 3 meses
            days_to_add = random.randint(0, 90)
            transaction_date = start_date + datetime.timedelta(days=days_to_add)
            date_str = transaction_date.strftime("%Y-%m-%d %H:%M:%S")
            
            # Actualizar saldo
            balance += amount
            
            # Insertar transacción
            cursor.execute('''
                INSERT INTO transactions 
                (account_id, date, concept, amount, balance_after, category, is_expense) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (account1_id, date_str, concept, amount, balance, category, is_expense))
        
        # Actualizar saldo final en la cuenta
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (balance, account1_id))
        
        # Lo mismo para el usuario2
        account2_id = 2
        balance = 2750.50
        
        for i in range(25):  # Generar 25 transacciones
            if random.random() < 0.2:
                concept, category, amount = random.choice(ingresos)
                is_expense = False
            else:
                concept, category, amount = random.choice(gastos)
                is_expense = True
            
            days_to_add = random.randint(0, 90)
            transaction_date = start_date + datetime.timedelta(days=days_to_add)
            date_str = transaction_date.strftime("%Y-%m-%d %H:%M:%S")
            
            balance += amount
            
            cursor.execute('''
                INSERT INTO transactions 
                (account_id, date, concept, amount, balance_after, category, is_expense) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (account2_id, date_str, concept, amount, balance, category, is_expense))
        
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (balance, account2_id))
    
    conn.commit()
    conn.close()

# Inicializar la base de datos
init_db()

# Ruta para login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Faltan credenciales'}), 400
    
    username = data['username']
    password = data['password']
    
    conn = sqlite3.connect('claude_bank.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", 
                  (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        # Generar token
        access_token = create_access_token(identity=user[0])
        return jsonify({
            'message': 'Login exitoso',
            'user_id': user[0],
            'username': user[1],
            'access_token': access_token
        }), 200
    else:
        return jsonify({'message': 'Credenciales inválidas'}), 401

# Ruta para comprobar estado 
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({'status': 'online'}), 200

# Ruta para comprobar el token
@app.route('/api/check-token', methods=['GET'])
@jwt_required()
def check_token():
    current_user_id = get_jwt_identity()
    return jsonify({'valid': True, 'user_id': current_user_id}), 200

# Ruta para obtener datos de usuario
@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    
    conn = sqlite3.connect('claude_bank.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, first_name, last_name, address, email, phone,
               marketing_consent, data_processing_consent, third_party_consent
        FROM users 
        WHERE id = ?
    """, (user_id,))
    
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return jsonify({
            'username': user_data[0],
            'first_name': user_data[1] or '',
            'last_name': user_data[2] or '',
            'address': user_data[3] or '',
            'email': user_data[4] or '',
            'phone': user_data[5] or '',
            'marketing_consent': bool(user_data[6]),
            'data_processing_consent': bool(user_data[7]),
            'third_party_consent': bool(user_data[8])
        }), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

# Ruta para actualizar datos de usuario
@app.route('/api/user/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Campos permitidos para actualizar
    allowed_fields = [
        'first_name', 'last_name', 'address', 'email', 'phone',
        'marketing_consent', 'data_processing_consent', 'third_party_consent'
    ]
    
    # Filtrar solo los campos permitidos
    update_data = {k: v for k, v in data.items() if k in allowed_fields}
    
    if not update_data:
        return jsonify({'message': 'No se proporcionaron campos válidos para actualizar'}), 400
    
    # Construir la consulta SQL dinámica
    set_clause = ', '.join([f"{field} = ?" for field in update_data.keys()])
    values = list(update_data.values())
    values.append(user_id)  # Para el WHERE id = ?
    
    conn = sqlite3.connect('claude_bank.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
        conn.commit()
        
        if cursor.rowcount > 0:
            return jsonify({'message': 'Perfil actualizado correctamente'}), 200
        else:
            return jsonify({'message': 'No se encontró el usuario o no se realizaron cambios'}), 404
            
    except Exception as e:
        conn.rollback()
        return jsonify({'message': f'Error al actualizar el perfil: {str(e)}'}), 500
        
    finally:
        conn.close()

# Ruta para depuración (sin JWT) - SOLO PARA DESARROLLO
@app.route('/api/balance-debug/<int:user_id>', methods=['GET'])
def get_balance_debug(user_id):
    conn = sqlite3.connect('claude_bank.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.account_number, a.balance, a.id
        FROM accounts a 
        WHERE a.user_id = ?
    """, (user_id,))
    account = cursor.fetchone()
    conn.close()
    
    if account:
        return jsonify({
            'account_number': account[0],
            'balance': account[1],
            'account_id': account[2]
        }), 200
    else:
        return jsonify({'message': 'Cuenta no encontrada'}), 404

# Ruta para obtener movimientos sin JWT (para depuración)
@app.route('/api/transactions-debug/<int:account_id>', methods=['GET'])
def get_transactions_debug(account_id):
    # Parámetros opcionales para paginación
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Calcular offset para paginación
    offset = (page - 1) * per_page
    
    conn = sqlite3.connect('claude_bank.db')
    cursor = conn.cursor()
    
    # Obtener el total de transacciones
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE account_id = ?", (account_id,))
    total = cursor.fetchone()[0]
    
    # Obtener las transacciones paginadas, ordenadas por fecha (más reciente primero)
    cursor.execute("""
        SELECT id, date, concept, amount, balance_after, category, is_expense
        FROM transactions
        WHERE account_id = ?
        ORDER BY date DESC
        LIMIT ? OFFSET ?
    """, (account_id, per_page, offset))
    
    transactions = []
    for row in cursor.fetchall():
        transaction = {
            'id': row[0],
            'date': row[1],
            'concept': row[2],
            'amount': row[3],
            'balance_after': row[4],
            'category': row[5],
            'is_expense': bool(row[6])
        }
        transactions.append(transaction)
    
    conn.close()
    
    return jsonify({
        'transactions': transactions,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }), 200

# Ruta para obtener un movimiento específico por ID (para depuración)
@app.route('/api/transaction-debug/<int:transaction_id>', methods=['GET'])
def get_transaction_debug(transaction_id):
    conn = sqlite3.connect('claude_bank.db')
    cursor = conn.cursor()
    
    # Obtener la transacción por ID
    cursor.execute("""
        SELECT t.id, t.date, t.concept, t.amount, t.balance_after, t.category, t.is_expense, a.account_number, a.user_id
        FROM transactions t
        JOIN accounts a ON t.account_id = a.id
        WHERE t.id = ?
    """, (transaction_id,))
    
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return jsonify({'message': 'Transacción no encontrada'}), 404
    
    # Obtener la transacción anterior y siguiente
    cursor.execute("""
        SELECT id FROM transactions 
        WHERE account_id = (SELECT account_id FROM transactions WHERE id = ?)
        AND date > (SELECT date FROM transactions WHERE id = ?)
        ORDER BY date ASC LIMIT 1
    """, (transaction_id, transaction_id))
    prev_transaction = cursor.fetchone()
    
    cursor.execute("""
        SELECT id FROM transactions 
        WHERE account_id = (SELECT account_id FROM transactions WHERE id = ?)
        AND date < (SELECT date FROM transactions WHERE id = ?)
        ORDER BY date DESC LIMIT 1
    """, (transaction_id, transaction_id))
    next_transaction = cursor.fetchone()
    
    # Construir el objeto de respuesta
    transaction = {
        'id': row[0],
        'date': row[1],
        'concept': row[2],
        'amount': row[3],
        'balance_after': row[4],
        'category': row[5],
        'is_expense': bool(row[6]),
        'account_number': row[7],
        'user_id': row[8],
        'prev_transaction_id': prev_transaction[0] if prev_transaction else None,
        'next_transaction_id': next_transaction[0] if next_transaction else None
    }
    
    conn.close()
    
    return jsonify(transaction), 200

# Ruta para obtener el saldo
@app.route('/api/balance', methods=['GET'])
@jwt_required()
def get_balance():
    user_id = get_jwt_identity()
    print(f"ID de usuario del token: {user_id}")
    
    conn = sqlite3.connect('claude_bank.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.account_number, a.balance, a.id
        FROM accounts a 
        WHERE a.user_id = ?
    """, (user_id,))
    account = cursor.fetchone()
    conn.close()
    
    if account:
        return jsonify({
            'account_number': account[0],
            'balance': account[1],
            'account_id': account[2]
        }), 200
    else:
        return jsonify({'message': 'Cuenta no encontrada'}), 404

# Ruta para obtener movimientos con JWT
@app.route('/api/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    
    # Parámetros opcionales para paginación
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Calcular offset para paginación
    offset = (page - 1) * per_page
    
    conn = sqlite3.connect('claude_bank.db')
    cursor = conn.cursor()
    
    # Primero obtenemos el ID de la cuenta del usuario
    cursor.execute("SELECT id FROM accounts WHERE user_id = ?", (user_id,))
    account_result = cursor.fetchone()
    
    if not account_result:
        conn.close()
        return jsonify({'message': 'Cuenta no encontrada'}), 404
    
    account_id = account_result[0]
    
    # Obtener el total de transacciones
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE account_id = ?", (account_id,))
    total = cursor.fetchone()[0]
    
    # Obtener las transacciones paginadas, ordenadas por fecha (más reciente primero)
    cursor.execute("""
        SELECT id, date, concept, amount, balance_after, category, is_expense
        FROM transactions
        WHERE account_id = ?
        ORDER BY date DESC
        LIMIT ? OFFSET ?
    """, (account_id, per_page, offset))
    
    transactions = []
    for row in cursor.fetchall():
        transaction = {
            'id': row[0],
            'date': row[1],
            'concept': row[2],
            'amount': row[3],
            'balance_after': row[4],
            'category': row[5],
            'is_expense': bool(row[6])
        }
        transactions.append(transaction)
    
    conn.close()
    
    return jsonify({
        'transactions': transactions,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }), 200

# Ruta para crear una nueva transacción
@app.route('/api/transactions', methods=['POST'])
@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validar datos de entrada
    required_fields = ['concept', 'amount', 'category', 'is_expense']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Falta el campo obligatorio: {field}'}), 400
    
    # Obtener datos de la transacción
    concept = data['concept']
    amount = float(data['amount'])
    category = data['category']
    is_expense = bool(data['is_expense'])
    
    # Si es un gasto, convertir el monto a negativo
    if is_expense and amount > 0:
        amount = -amount
    
    # Si es un ingreso, asegurarse de que el monto sea positivo
    if not is_expense and amount < 0:
        amount = abs(amount)
    
    conn = sqlite3.connect('claude_bank.db')
    cursor = conn.cursor()
    
    try:
        # Obtener el ID de la cuenta del usuario
        cursor.execute("SELECT id, balance FROM accounts WHERE user_id = ?", (user_id,))
        account_result = cursor.fetchone()
        
        if not account_result:
            conn.close()
            return jsonify({'message': 'Cuenta no encontrada'}), 404
        
        account_id, current_balance = account_result
        
        # Calcular el nuevo saldo
        new_balance = current_balance + amount
        
        # Fecha actual
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insertar la transacción
        cursor.execute("""
            INSERT INTO transactions (account_id, date, concept, amount, balance_after, category, is_expense)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (account_id, date_str, concept, amount, new_balance, category, is_expense))
        
        # Actualizar el saldo de la cuenta
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
        
        # Confirmar la transacción
        conn.commit()
        
        # Obtener el ID de la nueva transacción
        transaction_id = cursor.lastrowid
        
        return jsonify({
            'message': 'Transacción creada exitosamente',
            'transaction_id': transaction_id,
            'new_balance': new_balance
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'message': f'Error al crear la transacción: {str(e)}'}), 500
    
    finally:
        conn.close()

# Ruta para crear una nueva transacción (modo debug)
@app.route('/api/transactions-debug/<int:account_id>', methods=['POST'])
def create_transaction_debug(account_id):
    print(f"Recibida solicitud POST para crear transacción en cuenta {account_id}")
    print(f"Headers: {request.headers}")
    
    # Obtener los datos JSON con manejo de errores
    try:
        data = request.get_json()
        print(f"Datos recibidos: {data}")
    except Exception as e:
        print(f"Error al parsear JSON: {str(e)}")
        return jsonify({'message': f'Error al parsear JSON: {str(e)}'}), 400
    
    # Validar datos de entrada
    required_fields = ['concept', 'amount', 'category', 'is_expense']
    for field in required_fields:
        if field not in data:
            print(f"Falta el campo obligatorio: {field}")
            return jsonify({'message': f'Falta el campo obligatorio: {field}'}), 400
    
    # Obtener datos de la transacción
    concept = data['concept']
    amount = float(data['amount'])
    category = data['category']
    is_expense = bool(data['is_expense'])
    
    # Si es un gasto, convertir el monto a negativo
    if is_expense and amount > 0:
        amount = -amount
    
    # Si es un ingreso, asegurarse de que el monto sea positivo
    if not is_expense and amount < 0:
        amount = abs(amount)
    
    conn = sqlite3.connect('claude_bank.db')
    cursor = conn.cursor()
    
    try:
        # Obtener el saldo actual de la cuenta
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        account_result = cursor.fetchone()
        
        if not account_result:
            print(f"Cuenta no encontrada con ID: {account_id}")
            conn.close()
            return jsonify({'message': 'Cuenta no encontrada'}), 404
        
        current_balance = account_result[0]
        print(f"Saldo actual: {current_balance}")
        
        # Calcular el nuevo saldo
        new_balance = current_balance + amount
        print(f"Nuevo saldo calculado: {new_balance}")
        
        # Fecha actual
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insertar la transacción
        cursor.execute("""
            INSERT INTO transactions (account_id, date, concept, amount, balance_after, category, is_expense)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (account_id, date_str, concept, amount, new_balance, category, is_expense))
        
        # Actualizar el saldo de la cuenta
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
        
        # Confirmar la transacción
        conn.commit()
        
        # Obtener el ID de la nueva transacción
        transaction_id = cursor.lastrowid
        print(f"Transacción creada con ID: {transaction_id}")
        
        response = {
            'message': 'Transacción creada exitosamente',
            'transaction_id': transaction_id,
            'new_balance': new_balance
        }
        print(f"Respuesta: {response}")
        
        return jsonify(response), 201
        
    except Exception as e:
        print(f"Error al crear la transacción: {str(e)}")
        conn.rollback()
        return jsonify({'message': f'Error al crear la transacción: {str(e)}'}), 500
    
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)