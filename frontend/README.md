# Claude Bank - Frontend

Aplicación Angular para una aplicación bancaria de ejemplo con funcionalidad de login y consulta de saldo.

## Requisitos

- Node.js
- npm
- Angular CLI

## Instalación

1. Instalar Angular CLI (si no está instalado):
```
npm install -g @angular/cli
```

2. Navegar al directorio y crear una nueva aplicación Angular:
```
ng new claude-bank-frontend --routing=true --style=scss
cd claude-bank-frontend
```

3. Instalar dependencias adicionales:
```
npm install @angular/material
```

## Desarrollo

Para iniciar el servidor de desarrollo:
```
ng serve
```

La aplicación estará disponible en `http://localhost:4200/`.

## Construcción

Para compilar la aplicación para producción:
```
ng build --prod
```

## Estructura de la Aplicación

- **LoginComponent**: Maneja la autenticación de usuarios
- **BalanceComponent**: Muestra el saldo de la cuenta del usuario
- **AuthService**: Maneja la autenticación y el almacenamiento del token JWT
- **AccountService**: Maneja las operaciones relacionadas con la cuenta bancaria

## Datos de Ejemplo

La aplicación utiliza el backend de Claude Bank, que incluye estos usuarios de ejemplo:

1. **Usuario 1**:
   - Username: `usuario1`
   - Password: `password1`

2. **Usuario 2**:
   - Username: `usuario2`
   - Password: `password2`