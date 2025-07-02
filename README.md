# TaximetroF5 V.0

TaximetroF5 es una aplicación sencilla de línea de comandos para calcular la tarifa de un taxi basándose en el tiempo que el vehículo está detenido y en movimiento.

Funcionalidades

- Iniciar un viaje con el comando start.
- Cambiar el estado del taxímetro entre stop (parado) y move (movimiento).
- Finalizar el viaje y calcular el precio total con el comando finish.
- Salir de la aplicación con el comando exit.
- Cálculo automático del coste basado en las tarifas configuradas por segundo para estado parado y en movimiento.

## Tarifas

- Precio por segundo parado: 0.02 €

- Precio por segundo en movimiento: 0.05 €

## Uso

Ejecuta el script Python.
Utiliza los comandos para controlar el taxímetro:

- start: Inicia el viaje.

- stop: Marca que el taxi está detenido.

- move: Marca que el taxi está en movimiento.

- finish: Finaliza el viaje y muestra el resumen con la tarifa.

- exit: Salir de la aplicación.

## Ejemplo de uso
```
> start
Viaje iniciado
> move
el estado a cambiado: moviendose
> stop
el estado a cambiado: parado
> finish
Tiempo detenido: 12.5
Tiempo en movimiento: 45.3
Total a pagar: 2.58
> exit
Hasta luego
```


## Requisitos

- Python 3.x
- Librería estándar time (incluida en Python por defecto)
- Crear y activar un entorno virtual (recomendado para aislar dependencias)

## Cómo ejecutar
```
python nombre_del_archivo.py
```
## Estructura del código

- calculate_fare: Función que calcula el coste según tiempo parado y en movimiento.
- taximeter: Función principal que gestiona la interacción con el usuario y controla el estado del viaje.

---

# TaximetroF5 V.2

TaximetroF5 es una aplicación de línea de comandos para calcular tarifas de taxi, ahora con registro de eventos (logging), almacenamiento en archivo de texto y persistencia en base de datos SQLite.

## Funcionalidades

- Iniciar, pausar y continuar un viaje con control del estado: parado o en movimiento.
- Cálculo automático de tarifa según tiempo parado y en movimiento.
- Registro de eventos y errores en un archivo de log (`taximetro.log`).
- Guardado automático de registros de viajes en:
  - Archivo de texto (`registro_viajes.txt`) con formato legible.
  - Base de datos SQLite (`taximetro.db`) para gestión y consulta avanzada.
- Posibilidad de configurar tarifas dinámicas personalizadas.


## Estructura del proyecto

- `logging`: Captura de eventos importantes (inicio, cambio de estado, finalización, errores).
- `sqlite3`: Uso de base de datos SQLite para almacenar viajes históricos.
- Archivo `registro_viajes.txt`: historial simple en texto plano para consultas rápidas.
- Clase `Taximetro`: lógica principal del cálculo y gestión del viaje.
- Funciones auxiliares para crear tablas y guardar registros en la base de datos.


## Tarifas por defecto

- Precio por segundo parado: 0.02 €
- Precio por segundo en movimiento: 0.05 €


## Cómo usar

1. Ejecuta el script Python.
2. Usa los comandos en el menú:
   - `1` Iniciar viaje (puedes configurar tarifas dinámicas).
   - `2` Cambiar estado a parado.
   - `3` Cambiar estado a en movimiento.
   - `4` Finalizar viaje y mostrar resumen.
   - `5` Salir de la aplicación.
3. El programa guarda automáticamente cada viaje finalizado en la base de datos y en un archivo de texto, además de registrar eventos en el log.

## Ejemplo de salida en consola

```bash
--- Menú del Taxímetro ---
1. Iniciar Viaje
2. Poner en Parado
3. Poner en Movimiento
4. Finalizar Viaje y Calcular Tarifa
5. Salir de la aplicación (sin finalizar viaje)
--------------------------
Selecciona una opción: 1

--- Configuración de precios ---
1. Usar precio actual
2. Configurar precios
--------------------------
Selecciona una opción para configurar los precios: 1
Usando precios por defecto.
Viaje iniciado y taxímetro en estado Parado

Selecciona una opción: 3
Taxímetro en estado 'moviendose'.

Selecciona una opción: 2
Taxímetro en estado 'parado'.

Selecciona una opción: 4

--- RESUMEN DEL VIAJE ---
Tiempo total parado: 12.50 segundos
Tiempo total en movimiento: 45.30 segundos
Tarifa total calculada: €2.58
Viaje finalizado.
```
## Archivos generados

- taximetro.log: archivo con registro detallado de eventos y errores.
- registro_viajes.txt: texto plano con resumen de cada viaje.
- taximetro.db: base de datos SQLite con tabla viajes para almacenar datos históricos.

## Requisitos

- Python 3.x
- Librerías estándar: time, logging, sqlite3, datetime
- Crear y activar un entorno virtual (recomendado para aislar dependencias)
