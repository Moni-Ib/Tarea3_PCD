# Tarea3_PCD

Se elaboró esta tarea para implementar una API REST con FASTAPPI que permite crear, actualizar, obtener y eliminar usuarios en una base de datos SQLite.

LA API incluye endopints para gestionar los usuarios y hacer cada una de las acciones anteriormente mencionadas para crear, actualizar, obtener y eliminar a los usuarios con validación de email único, es decir que si ya se registró un usuario con un email y se detecta que se registra otro usuario con ese mismo emial no le permitirá registrarse.

## Requisitos previos

uv instalado

## Instalación y configuración

1) Clonar el repositorio

2) Crear ambiente virtual con uv
uv init para inicializar el ambiente

3) Instalar dependencias
uv add fastapi --extra standard
uv add sqlalchemy
uv add pydantic
uv add python-dotenv

## Configurar variables de entorno

Crea un archivo .env en la raíz del proyecto basado en .env.example.

.env.example: API_KEY=ejemplo

.env (ejemplo): API_KEY=(aquí se escribe la contraseña que es privada)

La API verificará la clave en el header X-API-Key

## Ejecutar la app

uv run fastapi dev main.py

## Endpoints

1) Crear usuario -> POST /api/v1/users/

Este endpoint permite crear nuevos usuarios

*Request*:

 ```json
   {
     "user_name": "name",
     "user_id": 123,
     "user_email": "email@example.com",
     "age": 30,
     "recommendations": ["a", "b", "c"],
     "ZIP": "44100"
   }
   ```
   
*Respuesta exitosa*:

```json
{
  "recommendations": [
    "Shrek 3"
  ],
  "user_id": 2,
  "user_name": "Cesar",
  "age": 24,
  "user_email": "cesar@gmail.com",
  "ZIP": "1111"
}
 ```

*Error*: 

Si el usuario se registra con un correo que ya había sido utilizado le aparecerá el siguiente mensaje:

The email 'email' is already registered.

2) Actualizar usuario por ID -> PUT /api/v1/users/{user_id}

Este endpoint permite actualizar la iformación del id del usuario que se ingrese, permitiendo modificar sus datos.

*Request*:

Ingresar el id del usuario que se quiere actualizar:

user_id: 2

Actualizar la información del usuario:

```json
   {

    "user_name": "Cesar",
    "user_id": 2,
    "user_email": "cesar@gmail.com",
    "age": 25,
    "recommendations": ["string"],
    "ZIP": "Shrek 3"
    }
```

Respuesta exitosa:

```json
   {

    "user_name": "Cesar",
    "user_id": 2,
    "user_email": "cesar@gmail.com",
    "age": 25,
    "recommendations": ["string"],
    "ZIP": "Shrek 3"
    }
```
*Error*:

Si el Id del usuario que se quiere actualizar no existe, aparecerá el siguiente mensaje:

ID 2 : Does not exist

3) Obtener usuario por ID -> GET /api/v1/users/{user_id}

Este endpoint permite obtener la información del usuario que se ingrese.

*Request*:

Ingresar el id del usuario que se quiere obtener:

user_id: 2

Respuesta exitosa:

```json
   {

    "user_name": "Cesar",
    "user_id": 2,
    "user_email": "cesar@gmail.com",
    "age": 25,
    "recommendations": ["string"],
    "ZIP": "Shrek 3"
    }
```
*Error*:

Si el Id del usuario que se quiere actualizar no existe, aparecerá el siguiente mensaje:

ID 2 : Does not exist

4) Eliminar usuario por ID -> DELETE /api/v1/users/{user_id}

Este endpoint permite borrar de la base de datos el usuario que se ingrese.

*Request*:

Ingresar el id del usuario que se quiere eliminar:

user_id: 2

Respuesta exitosa:

"deleted_id": 2

*Error*:

Si el Id del usuario que se quiere actualizar no existe, aparecerá el siguiente mensaje:

ID 2 : Does not exist

