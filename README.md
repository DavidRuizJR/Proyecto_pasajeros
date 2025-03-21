# Proyecto de Microservicios de Transporte

Este proyecto implementa un sistema de reservas de transporte utilizando microservicios.

## Descripción

El sistema se compone de dos microservicios principales:

* **Pasajeros:** Gestiona la información de los pasajeros.
* **Reservas:** Gestiona las reservas de transporte.

Estos microservicios se comunican entre sí a través de RabbitMQ para el intercambio de mensajes asíncronos y utilizan bases de datos PostgreSQL para el almacenamiento persistente de datos.

## Requisitos

* Docker
* Docker Compose
* Python 3.x

## Configuración

1.  **Configuración de variables de entorno:**
    * Verifica que las variables de entorno para la conexión a la base de datos y RabbitMQ estén correctamente configuradas en los archivos `docker-compose.yml`

2.  **Construcción y ejecución de los contenedores:**

    ```bash
    docker-compose up --build -d
    ```

    Este comando construirá las imágenes Docker y ejecutará los contenedores en segundo plano.

## Uso

* Los microservicios estarán disponibles en los siguientes puertos:
    * **Reservas:** `http://localhost:5000`
    * **Pasajeros:** `http://localhost:5001`

* Puedes utilizar herramientas como `curl` o Postman para interactuar con las APIs de los microservicios.

## Puntos importantes.

* Para poder generar las tablas de la base de datos, los microservicios deben de estar en ejecución.
* Si se hacen modificaciones a los dockerfiles, es obligatorio volver a generar las imagenes.
* En el archivo docker-compose.yml, se definen los volumenes, por lo cual la persistencia de la información esta garantizada.

## Dependencias

Las dependencias de Python para cada microservicio se encuentran en los archivos `requirements.txt` correspondientes.

## Contribución

Las contribuciones son bienvenidas. Si encuentras algún problema o tienes alguna sugerencia, no dudes en abrir un issue o enviar un pull request.

## Licencia

Este proyecto está bajo la licencia [Indica aquí la licencia].