# librería para usar el tiempo
import time

# librería para usar un sistema de log
import logging

# librería para usar sql
import sqlite3

# Configurar el sistema de logs, indicando
# Donde se guardará
# Nivel mínimo de los mensajes
# Formato del mensaje
logging.basicConfig(
    filename="taximetro.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def crear_tabla():
    conexion = sqlite3.connect("taximetro.db")
    cursor = conexion.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS viajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        tiempo_parado REAL,
        tiempo_movimiento REAL,
        tarifa REAL
    )
    """
    )

    conexion.commit()
    conexion.close()


crear_tabla()


def guardar_viaje(fecha, tiempo_parado, tiempo_movimiento, tarifa):
    conexion = sqlite3.connect("taximetro.db")
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO viajes (fecha, tiempo_parado, tiempo_movimiento, tarifa)
        VALUES (?, ?, ?, ?)
    """,
        (fecha, tiempo_parado, tiempo_movimiento, tarifa),
    )

    conexion.commit()
    conexion.close()


# constantes para las tarifas
PRECIO_POR_SEGUNDO_PARADO = 0.02
PRECIO_POR_SEGUNDO_MOVIMIENTO = 0.05


# definir clase
class Taximetro:
    def __init__(self):
        # declaración de variables
        self.viaje_activo = False
        self.tiempo_inicio = 0
        self.tiempo_parado = 0
        self.tiempo_moviendose = 0
        # None se usa para declarar una variable sin valor
        # "parado" o "moviendose"
        self.estado_viaje = None
        # Momento en que inició el estado actual
        self.estado_tiempo_inicio = 0
        # Precio dinamico
        self.precio_parado_dinamico = 0.0
        self.precio_movimiento_dinamico = 0.0

    """
    el _ (un solo guión bajo)
    (o cualquier otro método o atributo con un solo guion bajo inicial) 
    es una convención para indicar privacidad/uso interno.
    Esta diseñado para ser usado solo desde dentro de la propia clase
    """

    def _actualizar_duracion(self):
        if self.estado_viaje:
            duracion = time.time() - self.estado_tiempo_inicio
            if self.estado_viaje == "parado":
                self.tiempo_parado += duracion
                logging.info(f"Tiempo parado actualizado: +{duracion:.2f}s")
            elif self.estado_viaje == "moviendose":
                self.tiempo_moviendose += duracion
                logging.info(f"Tiempo movimiento actualizado: +{duracion:.2f}s")

    def iniciar_viaje(self):
        if self.viaje_activo:
            logging.warning("Intento de iniciar un viaje ya activo")
            print("Error, el viaje ya ha iniciado")
            return

        self.viaje_activo = True
        self.tiempo_inicio = time.time()
        self.tiempo_parado = 0
        self.tiempo_moviendose = 0
        # El viaje empieza siempre parado
        self.estado_viaje = "parado"
        self.estado_tiempo_inicio = time.time()
        logging.info("Viaje iniciado correctamente")
        print("Viaje iniciado y taxímetro en estado Parado")

    def cambiar_estado(self, nuevo_estado):
        if not self.estado_viaje:
            logging.warning("Intento de cambiar estado sin haber iniciado el viaj")
            print("Error: El viaje no se ha iniciado. Inícialo primero (Opción 1).")
            return
        if self.estado_viaje == nuevo_estado:
            logging.warning(f"Estado '{nuevo_estado}' ya está activo")
            print(f"El taxímetro ya está en estado '{nuevo_estado}'.")
            return
        # Guarda el tiempo del estado actual antes de cambiar
        self._actualizar_duracion()
        self.estado_viaje = nuevo_estado
        self.estado_tiempo_inicio = (
            time.time()
        )  # Reinicia el contador para el nuevo estado
        logging.info(f"Estado cambiado a '{nuevo_estado}'")
        print(f"Taxímetro en estado '{nuevo_estado}'.")

    def configurar_precios_dinamicos(self, precio_parado, precio_movimiento):
        self.precio_parado_dinamico = precio_parado
        self.precio_movimiento_dinamico = precio_movimiento

    def finalizar_viaje(self, opcion_precio):
        if not self.viaje_activo:
            logging.error("Intento de finalizar un viaje no iniciado")
            print("Error, el viaje no ha iniciado")
            return
        self._actualizar_duracion()
        self.viaje_activo = False

        if opcion_precio == 1:
            fare = (
                self.tiempo_parado * PRECIO_POR_SEGUNDO_PARADO
                + self.tiempo_moviendose * PRECIO_POR_SEGUNDO_MOVIMIENTO
            )
        elif opcion_precio == 2:
            fare = (
                self.tiempo_parado * self.precio_parado_dinamico
                + self.tiempo_moviendose * self.precio_movimiento_dinamico  # type: ignore
            )

        logging.info(
            f"Viaje finalizado. Parado: {self.tiempo_parado:.2f}s, "
            f"Movimiento: {self.tiempo_moviendose:.2f}s, Tarifa: €{fare:.2f}"
        )

        # Guardar en archivo
        from datetime import datetime

        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("registro_viajes.txt", "a") as archivo:
            archivo.write(f"Viaje finalizado en: {ahora}\n")
            archivo.write(f"Tiempo parado: {self.tiempo_parado:.2f} segundos\n")
            archivo.write(
                f"Tiempo en movimiento: {self.tiempo_moviendose:.2f} segundos\n"
            )
            archivo.write(f"Tarifa calculada: €{fare:.2f}\n")
            archivo.write("------------\n")

        # Guardar en BBDD
        guardar_viaje(ahora, self.tiempo_parado, self.tiempo_moviendose, fare)

        print("\n--- RESUMEN DEL VIAJE ---")
        print(f"Tiempo total parado: {self.tiempo_parado:.2f} segundos")
        print(f"Tiempo total en movimiento: {self.tiempo_moviendose:.2f} segundos")
        print(f"Tarifa total calculada: €{fare:.2f}")
        print("Viaje finalizado.")

        # Reiniciar variables para un posible nuevo viaje
        self.tiempo_parado = 0
        self.tiempo_moviendose = 0
        self.estado_viaje = None
        self.tiempo_inicio = 0
        self.estado_tiempo_inicio = 0
        self.precio_parado_dinamico = 0.0
        self.precio_movimiento_dinamico = 0.0


def display_menu():
    """Muestra las opciones del menú para el usuario."""
    print("\n--- Menú del Taxímetro ---")
    print("1. Iniciar Viaje")
    print("2. Poner en Parado")
    print("3. Poner en Movimiento")
    print("4. Finalizar Viaje y Calcular Tarifa")
    print("5. Salir de la aplicación (sin finalizar viaje)")
    print("--------------------------")


def display_menu_precios():

    print("\n--- Configuración de precios ---")
    print("1. Usar precio actual")
    print("2. Configurar precios")
    print("--------------------------")


def run_taximeter_app():
    """Función principal que ejecuta la aplicación del taxímetro."""
    taximetro = Taximetro()  # Crea una instancia de la clase Taximetro
    opcion_precio = 1

    while True:
        display_menu()
        command = input("Selecciona una opción: ").strip()

        if command == "1":
            if taximetro.viaje_activo:
                print(
                    "Error: ya hay un viaje en curso. Finalízalo antes de iniciar uno nuevo."
                )
                continue

            while True:
                display_menu_precios()
                opcion = input(
                    "Selecciona una opción para configurar los precios: "
                ).strip()

                if opcion == "1":
                    opcion_precio = 1
                    print("Usando precios por defecto.")
                    break
                elif opcion == "2":
                    """
                    A diferencia de los otros if-opcion, comparamos el input con un str
                    y mandamos una función/instrucción, aquí se necesita el uso de try/except ya que
                    necesitamos convertir el input en float, si se introduce un str
                    se rompería el programa creando una excepción
                    """
                    try:
                        precio_parado = float(
                            input("Introduce precio por segundo parado: ")
                        )
                        precio_movimiento = float(
                            input("Introduce precio por segundo en movimiento: ")
                        )
                        taximetro.configurar_precios_dinamicos(
                            precio_parado, precio_movimiento
                        )
                        opcion_precio = 2
                        print("Precios personalizados configurados correctamente.")
                        break
                    except ValueError:
                        print("Error: Debes introducir un número válido.")
                else:
                    print("Opción no válida. Por favor, elige 1 o 2.")
            taximetro.iniciar_viaje()
        elif command == "2":
            taximetro.cambiar_estado("parado")
        elif command == "3":
            taximetro.cambiar_estado("moviendose")
        elif command == "4":
            taximetro.finalizar_viaje(opcion_precio)
        elif command == "5":
            if taximetro.viaje_activo:
                print("Advertencia: Saliendo sin finalizar el viaje actual.")
            print("Saliendo de la aplicación del taxímetro.")
            break
        else:
            print("Opción no válida. Por favor, selecciona un número del 1 al 5.")


if __name__ == "__main__":
    run_taximeter_app()
