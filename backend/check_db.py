import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('claude_bank.db')
cursor = conn.cursor()

# Verificar usuarios
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print("Usuarios:")
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}")

# Verificar cuentas
cursor.execute("SELECT * FROM accounts")
accounts = cursor.fetchall()
print("\nCuentas:")
for account in accounts:
    print(f"ID: {account[0]}, User ID: {account[1]}, Número: {account[2]}, Saldo: {account[3]}")

# Verificar movimientos
cursor.execute("SELECT COUNT(*) FROM transactions")
count = cursor.fetchone()[0]
print(f"\nTotal de movimientos: {count}")

# Movimientos por cuenta
cursor.execute("SELECT account_id, COUNT(*) FROM transactions GROUP BY account_id")
for row in cursor.fetchall():
    print(f"Cuenta {row[0]}: {row[1]} movimientos")

# Algunos movimientos de ejemplo
print("\nEjemplo de movimientos:")
cursor.execute("""
    SELECT id, account_id, date, concept, amount, category 
    FROM transactions 
    ORDER BY date DESC 
    LIMIT 5
""")
for m in cursor.fetchall():
    print(f"ID: {m[0]}, Cuenta: {m[1]}, Fecha: {m[2]}, Concepto: {m[3]}, Importe: {m[4]}, Categoría: {m[5]}")

conn.close()
print("\nVerificación completada.")