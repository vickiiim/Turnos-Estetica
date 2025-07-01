from datetime import datetime
from collections import Counter
from agregar_turno import agregar_turno, cargar_clientes
from cancelar_turnos import guardar_turnos

from validaciones import (
    validar_nombre_completo,
    validar_fecha,
    validar_hora,
    validar_dia_valido,
    turno_duplicado,
    validar_anticipacion,
    validar_capacidad_categoria,
    validar_limite_4_meses,
)
from horarios import cargar_feriados

CATEGORIAS = {
    "Cabello": [
        "Corte de cabello",
        "Tinte de cabello",
        "Peinado",
        "Tratamiento capilar",
        "Lavado y peinado",
        "Alisado permanente",
        "Extensiones",
        "Mechas",
        "Hidratación profunda"
    ],
    "Uñas": [
        "Manicura",
        "Pedicura",
        "Acrilicas",
        "Gel semipermanente"
    ],
    "Facial": [
        "Masaje facial",
        "Limpieza facial",
        "Maquillaje",
    ],
    "Depilación": [
        "Depilación con cera",
        "Depilación con hilo",
        "Depilación láser",
        "Depilación con azucar"
    ]
}

FERIADOS_ARG = cargar_feriados()

def seleccionar_categoria_servicio():
    print("Seleccione una categoría (0 para salir):")
    categorias_list = list(CATEGORIAS.keys())
    for i, cat in enumerate(categorias_list, 1):
        print(f"{i}. {cat}")
    print("0. Volver atrás")

    while True:
        opcion_cat = input("Ingrese el número de la categoría: ").strip()
        if opcion_cat == "0":
            return None, None
        try:
            opcion_cat = int(opcion_cat)
            if 1 <= opcion_cat <= len(categorias_list):
                categoria_seleccionada = categorias_list[opcion_cat - 1]
                break
            else:
                print(f"Debe ingresar un número entre 0 y {len(categorias_list)}.")
        except ValueError:
            print("Debe ingresar un número válido.")

    servicios_list = CATEGORIAS[categoria_seleccionada]
    print(f"Servicios disponibles para {categoria_seleccionada} (0 para salir):")
    for i, serv in enumerate(servicios_list, 1):
        print(f"{i}. {serv}")
    print("0. Volver atrás")

    while True:
        opcion_serv = input("Ingrese el número del servicio: ").strip()
        if opcion_serv == "0":
            return None, None
        try:
            opcion_serv = int(opcion_serv)
            if 1 <= opcion_serv <= len(servicios_list):
                servicio_seleccionado = servicios_list[opcion_serv - 1]
                break
            else:
                print(f"Debe ingresar un número entre 0 y {len(servicios_list)}.")
        except ValueError:
            print("Debe ingresar un número válido.")

    return categoria_seleccionada, servicio_seleccionado

def registrar_turno_cmd():
    print("=== Registrar nuevo turno ===")
    clientes = cargar_clientes()
    feriados = FERIADOS_ARG

    while True:
        nombre = input("Nombre completo (0 para salir): ").strip()
        if nombre == "0":
            print("Operación cancelada, regresando al menú principal.")
            return
        if not validar_nombre_completo(nombre):
            print("El nombre debe tener al menos 4 letras y solo contener letras y espacios.")
        else:
            break

    categoria, servicio = seleccionar_categoria_servicio()
    if categoria is None or servicio is None:
        print("Operación cancelada, regresando al menú principal.")
        return

    while True:
        fecha = input("Fecha (YYYY-MM-DD) (0 para salir): ").strip()
        if fecha == "0":
            print("Operación cancelada, regresando al menú principal.")
            return
        if not validar_fecha(fecha):
            print("Fecha inválida. Use formato YYYY-MM-DD y no puede ser pasada.")
            continue

        try:
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
            if fecha_dt.strftime("%Y-%m-%d") in feriados:
                print("No se pueden registrar turnos en días feriados.")
                continue
        except ValueError:
            print("Formato de fecha inválido.")
            continue

        if not validar_dia_valido(fecha):
            print("No se pueden registrar turnos los domingos.")
            continue
        if not validar_limite_4_meses(fecha):
            print("No se pueden crear turnos con más de 4 meses de anticipación.")
            continue

        break

    while True:
        hora = input("Hora (HH:MM) (0 para salir): ").strip()
        if hora == "0":
            print("Operación cancelada, regresando al menú principal.")
            return
        if not validar_hora(hora):
            print("Hora inválida. Solo horarios en punto o y media entre 10:00 y 18:00.")
            continue
        if not validar_anticipacion(fecha, hora):
            print("Los turnos deben solicitarse con al menos 2 horas de anticipación.")
            continue
        break

    turno = {
        "nombre": nombre,
        "categoria": categoria,
        "servicio": servicio,
        "fecha": fecha,
        "hora": hora
    }

    if turno_duplicado(clientes, turno):
        print(f"{nombre} ya tiene un turno registrado el {fecha} a las {hora}.")
        return

    disponible, mensaje = validar_capacidad_categoria(clientes, categoria, fecha, hora)
    if not disponible:
        print(f"{mensaje}")
        return

    resultado = agregar_turno(turno)
    print(f"{resultado}")

def mostrar_turnos():
    clientes = cargar_clientes()
    if not clientes:
        print("\nNo hay turnos cargados.\n")
        return

    print("\nTurnos agendados")
    print("----------------------")
    for i, turno in enumerate(clientes, 1):
        nombre = turno.get("nombre", "Sin nombre")
        fecha = turno.get("fecha", "Sin fecha")
        hora = turno.get("hora", "Sin hora")
        categoria = turno.get("categoria", "Sin categoría")
        servicio = turno.get("servicio", "Sin servicio")
        print(f"{i}. {fecha} {hora} - {nombre} ({categoria} - {servicio})")
    print()

def clasificar_banda_horaria(hora_str):
    try:
        hora = datetime.strptime(hora_str, "%H:%M").time()
        if datetime.strptime("10:00", "%H:%M").time() <= hora <= datetime.strptime("15:00", "%H:%M").time():
            return "Mañana"
        elif datetime.strptime("15:30", "%H:%M").time() <= hora <= datetime.strptime("18:00", "%H:%M").time():
            return "Tarde"
        else:
            return "Desconocido"
    except ValueError:
        return "Desconocido"

def mostrar_estadisticas():
    clientes = cargar_clientes()
    if not clientes:
        print("\nNo hay turnos registrados para mostrar estadísticas.\n")
        return

    nombres = [t.get("nombre", "Sin nombre") for t in clientes]
    ranking_clientes = Counter(nombres).most_common(5)

    categorias = [t.get("categoria", "Sin categoría") for t in clientes]
    conteo_categorias = Counter(categorias)

    bandas = [clasificar_banda_horaria(t.get("hora", "")) for t in clientes]
    conteo_bandas = Counter(bandas)

    print("\nEstadísticas del sistema de turnos")
    print("--------------------------------------")

    print("\nTop 5 clientes con más turnos:")
    for i, (nombre, cantidad) in enumerate(ranking_clientes, 1):
        print(f"   {i}. {nombre} - {cantidad} turno(s)")

    print("\nCantidad de turnos por categoría:")
    for categoria, cantidad in conteo_categorias.items():
        print(f"   - {categoria}: {cantidad} turno(s)")

    print("\nCantidad de turnos por franja horaria:")
    for banda in ["Mañana", "Tarde", "Desconocido"]:
        if banda in conteo_bandas:
            print(f"   - {banda}: {conteo_bandas[banda]} turno(s)")
    print()


def cancelar_turno_cmd():
    clientes = cargar_clientes()
    if not clientes:
        print("No hay turnos para cancelar.")
        return

    print("Seleccione el turno a cancelar (0 para volver atrás):")
    for i, turno in enumerate(clientes, 1):
        print(f"{i}. {turno.get('fecha', 'Sin fecha')} {turno.get('hora', 'Sin hora')} - {turno.get('nombre', 'Sin nombre')} ({turno.get('categoria', 'Sin categoría')} - {turno.get('servicio', 'Sin servicio')})")
    print("0. Volver atrás")

    while True:
        opcion = input("Ingrese el número del turno a cancelar: ").strip()
        if opcion == "0":
            print("Cancelación no realizada: Volviendo al menú principal")
            return
        try:
            opcion = int(opcion)
            if 1 <= opcion <= len(clientes):
                turno_seleccionado = clientes[opcion - 1]
                break
            else:
                print(f"Debe ingresar un número entre 0 y {len(clientes)}.")
        except ValueError:
            print("Debe ingresar un número válido.")

    confirm = input(f"Confirma cancelar el turno de {turno_seleccionado.get('nombre', 'Sin nombre')} el {turno_seleccionado.get('fecha', 'Sin fecha')} a las {turno_seleccionado.get('hora', 'Sin hora')}? (s/n): ").strip().lower()
    if confirm == 's':
        clientes.remove(turno_seleccionado)
        guardar_turnos(clientes)
        print("Turno cancelado con éxito.")
    else:
        print("Cancelación no realizada.")

def modificar_turno_cmd():
    clientes = cargar_clientes()
    feriados = FERIADOS_ARG

    if not clientes:
        print("No hay turnos para modificar.")
        return

    print("Seleccione el turno a modificar (0 para volver atrás):")
    for i, turno in enumerate(clientes, 1):
        print(f"{i}. {turno.get('fecha', 'Sin fecha')} {turno.get('hora', 'Sin hora')} - {turno.get('nombre', 'Sin nombre')} ({turno.get('categoria', 'Sin categoría')} - {turno.get('servicio', 'Sin servicio')})")
    print("0. Volver atrás")

    while True:
        opcion = input("Ingrese el número del turno a modificar: ").strip()
        if opcion == "0":
            print("Modificación abortada, regresando al menú principal.")
            return
        try:
            opcion = int(opcion)
            if 1 <= opcion <= len(clientes):
                turno_seleccionado = clientes[opcion - 1]
                break
            else:
                print(f"Debe ingresar un número entre 0 y {len(clientes)}.")
        except ValueError:
            print("Debe ingresar un número válido.")

    nombre = turno_seleccionado["nombre"]
    categoria = turno_seleccionado["categoria"]

    while True:
        nueva_fecha = input("Ingrese la nueva fecha (YYYY-MM-DD) (0 para salir): ").strip()
        if nueva_fecha == "0":
            print("Modificación abortada, regresando al menú principal.")
            return
        if not validar_fecha(nueva_fecha):
            print("Fecha inválida. Use formato YYYY-MM-DD y no puede ser pasada.")
            continue

        try:
            fecha_dt = datetime.strptime(nueva_fecha, "%Y-%m-%d").date()
            if fecha_dt.strftime("%Y-%m-%d") in feriados:
                print("No se pueden registrar turnos en días feriados.")
                continue
        except ValueError:
            print("Formato de fecha inválido.")
            continue

        if not validar_dia_valido(nueva_fecha):
            print("No se pueden registrar turnos los domingos.")
            continue
        if not validar_limite_4_meses(nueva_fecha):
            print("No se pueden crear turnos con más de 4 meses de anticipación.")
            continue

        break

    while True:
        nueva_hora = input("Ingrese la nueva hora (HH:MM) (0 para salir): ").strip()
        if nueva_hora == "0":
            print("Modificación abortada, regresando al menú principal.")
            return
        if not validar_hora(nueva_hora):
            print("Hora inválida. Solo horarios en punto o y media entre 10:00 y 18:00.")
            continue
        if not validar_anticipacion(nueva_fecha, nueva_hora):
            print("Los turnos deben solicitarse con al menos 2 horas de anticipación.")
            continue
        break

    nuevo_turno = {
        "nombre": nombre,
        "categoria": categoria,
        "servicio": turno_seleccionado["servicio"],
        "fecha": nueva_fecha,
        "hora": nueva_hora
    }

    otros_turnos = [t for t in clientes if t != turno_seleccionado]

    if turno_duplicado(otros_turnos, nuevo_turno):
        print(f"{nombre} ya tiene un turno registrado el {nueva_fecha} a las {nueva_hora}.")
        return

    disponible, mensaje = validar_capacidad_categoria(otros_turnos, categoria, nueva_fecha, nueva_hora)
    if not disponible:
        print(f"{mensaje}")
        return

    turno_seleccionado['fecha'] = nueva_fecha
    turno_seleccionado['hora'] = nueva_hora

    guardar_turnos(clientes)
    print("Turno modificado con éxito.")

def menu():
    while True:
        print("""
===============================
Sistema de Gestión de Estética
===============================

1. Agendar turno
2. Cancelar turno
3. Ver turnos agendados
4. Modificar turno
5. Ver estadísticas
6. Salir
""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_turno_cmd()

        elif opcion == "2":
            cancelar_turno_cmd()

        elif opcion == "3":
            mostrar_turnos()

        elif opcion == "4":
            modificar_turno_cmd()

        elif opcion == "5":
            mostrar_estadisticas()

        elif opcion == "6":
            print("¡Hasta pronto!")
            break

        else:
            print("Opción no válida. Intente nuevamente.\n")

if __name__ == "__main__":
    menu()