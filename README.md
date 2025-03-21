# Claude Bank

Aplicación bancaria de ejemplo para consultar el saldo de cuenta corriente. Esta aplicación es accesible tanto desde dispositivos de escritorio como móviles.

## Inicio Rápido

Para iniciar la aplicación, ejecuta:

1. **Backend**:
   ```bash
   cd /Users/allosagu/dev/claude_mobile_app/claude_bank/backend
   source venv/bin/activate
   python app.py
   ```
   El servidor backend estará disponible en: http://localhost:5000

2. **Frontend**:
   ```bash
   # Instalar Angular CLI si no lo tienes
   npm install -g @angular/cli
   
   # Instalar dependencias y ejecutar
   cd /Users/allosagu/dev/claude_mobile_app/claude_bank/frontend/angular-app
   npm install
   ng serve --open
   ```

La aplicación será accesible en: http://localhost:4200

## Solución de problemas

Si experimentas problemas:

1. **Reinicia ambos servidores**:
   - Detén los servidores con Ctrl+C
   - Reinicia cada uno en su respectiva terminal

2. **Verifica que el backend esté funcionando**:
   - Abre en tu navegador: http://localhost:5000/api/status
   - Debería mostrar: `{"status":"online"}`

3. **Limpia caché del navegador**:
   - Borra cookies y caché del navegador
   - Cierra y vuelve a abrir el navegador

4. **Usuarios de prueba**:
   - Usuario: `usuario1` / Contraseña: `password1`
   - Usuario: `usuario2` / Contraseña: `password2`

## Estructura del Proyecto

El proyecto está dividido en dos partes:

- **Backend**: API REST en Python usando Flask y SQLite
- **Frontend**: Aplicación web en Angular con diseño adaptativo

## Backend

El backend proporciona una API REST para:
- Autenticación de usuarios (login)
- Consulta de saldo de cuenta

### Tecnologías utilizadas
- Python
- Flask
- SQLite
- JWT para autenticación

### Instalación y ejecución
Consulta el [README del backend](./backend/README.md) para más detalles.

## Frontend

El frontend es una aplicación Angular que proporciona:
- Interfaz de login
- Pantalla de consulta de saldo
- Diseño adaptativo para escritorio y móvil

### Tecnologías utilizadas
- Angular
- Angular Material
- CSS responsive

### Instalación y ejecución
Consulta el [README del frontend](./frontend/README.md) para más detalles.

## Datos de Ejemplo

La aplicación incluye dos usuarios de ejemplo:

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