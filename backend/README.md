# Claude Bank - Backend

API REST simple para una aplicación bancaria de ejemplo con funcionalidad de login y consulta de saldo.

## Requisitos

- Python 3.x
- Flask
- Flask-CORS
- Flask-JWT-Extended

## Instalación

1. Crear y activar entorno virtual:
```
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```
pip install flask flask-cors flask-jwt-extended
```

## Ejecución

```
python app.py
```

El servidor se iniciará en `http://localhost:5000`.

## Endpoints

### Login
- **URL**: `/api/login`
- **Método**: `POST`
- **Datos**: `{ "username": "usuario1", "password": "password1" }`
- **Respuesta exitosa**: 
```json
{
  "message": "Login exitoso",
  "user_id": 1,
  "username": "usuario1",
  "access_token": "eyJ0eXAiOiJKV..."
}
```

### Consulta de Saldo
- **URL**: `/api/balance`
- **Método**: `GET`
- **Headers**: `Authorization: Bearer {token}`
- **Respuesta exitosa**:
```json
{
  "account_number": "10001",
  "balance": 1500.75
}
```

## Datos de Ejemplo

La base de datos incluye dos usuarios de ejemplo:

1. **Usuario 1**:
   - Username: `usuario1`
   - Password: `password1`
   - Cuenta: `10001`
   - Saldo: `1500.75`

2. **Usuario 2**:
   - Username: `usuario2`
   - Password: `password2`
   - Cuenta: `10002`
   - Saldo: `2750.50`