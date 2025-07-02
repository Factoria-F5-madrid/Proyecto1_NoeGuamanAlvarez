#calcular el precio
import time

def calculate_fare(second_stopped, second_moving):
    fare = second_stopped * 0.02 + second_moving * 0.05
    return fare

def taximeter():
    print("Bienvenido a TaximetroF5")
    print("Comandos:  start, stop, move, finish, exit")

    trip_active = False
    start_time = 0
    stop_time = 0
    moving_time = 0
    state = None
    state_start_time = 0
    while True:
        command = input("> ").strip().lower()
        if command == "start":
            if trip_active:
                print("Error: El viaje ya ha iniciado")
                continue
            trip_active = True
            start_time = time.time()
            stop_time = 0
            moving_time = 0
            state = "stop"
            state_start_time = time.time()
            print(state_start_time)
            print("Viaje iniciado")
        elif command in ("stop", "move"):
            if not trip_active:
                print("Error, el viaje no se ha iniciado")
                continue
            duration = time.time() - state_start_time
            if state == "stop":
                stop_time += duration
            else:
                moving_time += duration
            
            state = "stop" if command == "stop" else "moving"
            state_start_time =  time.time()
            print(f"el estado a cambiado: {state}")
        elif command == "finish":
            if not trip_active:
                print("error: el viaje ha finalizado")
                continue
            duration = time.time() - state_start_time
            if state == "stop":
                stop_time += duration
            else:
                moving_time += duration
            
            
            total_fare = calculate_fare(stop_time, moving_time)
            print(f"Tiempo detenido: {stop_time: .1f}")
            print(f"Tiempo en movimiento: {moving_time: .1f}")
            print(f"Total a pagar: {total_fare: .1f}")
            trip_active = False
            state = None
        elif command == "exit":
            print("Hasta luego")
            break


if __name__ == "__main__":
    taximeter()