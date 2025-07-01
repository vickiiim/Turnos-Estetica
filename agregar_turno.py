import json
import os
import csv
from horarios import cargar_feriados
from validaciones import (
    validar_anticipacion,
    validar_capacidad_categoria,
    validar_fecha,
    validar_hora,
    validar_dia_valido,
    validar_limite_4_meses
)
from datetime import datetime, timedelta

ARCHIVO_CLIENTES = "clientes.json"

def cargar_clientes():
    """Carga los turnos desde el archivo JSON."""
    if os.path.exists(ARCHIVO_CLIENTES):
        with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_clientes(clientes):
    """Guarda los turnos en el archivo JSON."""
    with open(ARCHIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False, indent=4)

def agregar_turno(turno):
    """Agrega un nuevo turno, evitando conflictos, duplicados y otras restricciones."""
    clientes = cargar_clientes()
    feriados = cargar_feriados()

    try:
        fecha_turno = datetime.strptime(turno["fecha"], "%Y-%m-%d")
        fecha_actual = datetime.now()
        if fecha_turno.date() < fecha_actual.date():
            return f"No puedes agendar turnos en fechas pasadas ({turno['fecha']})."
    except ValueError:
        return "Formato de fecha incorrecto. Use YYYY-MM-DD."

    if turno["fecha"] in feriados:
        return f"No se pueden agendar turnos en días feriados ({turno['fecha']})."

    try:
        fecha_hora_turno = datetime.strptime(f"{turno['fecha']} {turno['hora']}", "%Y-%m-%d %H:%M")
        if fecha_hora_turno < datetime.now() + timedelta(hours=2):
            return "Los turnos deben solicitarse con al menos 2 horas de anticipación."
    except ValueError:
        return "Hora inválida o formato incorrecto."

    for t in clientes:
        if (
            t.get("nombre", "").strip().lower() == turno["nombre"].strip().lower()
            and t.get("fecha") == turno["fecha"]
            and t.get("hora") == turno["hora"]
        ):
            return f"{turno['nombre']} ya tiene un turno registrado el {turno['fecha']} a las {turno['hora']}."

    mismos_turnos = [
        t for t in clientes
        if t.get("categoria") == turno["categoria"]
        and t.get("fecha") == turno["fecha"]
        and t.get("hora") == turno["hora"]
    ]
    if len(mismos_turnos) >= 2:
        return "Ya hay 2 turnos registrados en esta categoría a esa hora."
    
    if not validar_limite_4_meses(turno["fecha"]):
        return "No se pueden crear turnos con más de 4 meses de anticipación."
    
    # Generar nuevo ID único
    nuevo_id = max([t.get("id", 0) for t in clientes], default=0) + 1
    turno["id"] = nuevo_id

    clientes.append(turno)
    guardar_clientes(clientes)
    return f"Turno de {turno['nombre']} (ID: {nuevo_id}) agendado correctamente."

def cancelar_turno(nombre):
    """Elimina un turno según el nombre del cliente."""
    clientes = cargar_clientes()
    clientes_filtrados = [t for t in clientes if t.get("nombre") != nombre]

    if len(clientes_filtrados) == len(clientes):
        return "Turno no encontrado."

    guardar_clientes(clientes_filtrados)
    return f"Turno de {nombre} cancelado."

def modificar_turno(nombre, nueva_fecha, nueva_hora):
    """Modifica la fecha y hora de un turno existente, con todas las validaciones necesarias."""
    clientes = cargar_clientes()
    feriados = cargar_feriados()

    turno_actual = next((t for t in clientes if t.get("nombre") == nombre), None)
    if not turno_actual:
        return "Turno no encontrado."

    if not validar_fecha(nueva_fecha):
        return f"Fecha inválida. Use formato YYYY-MM-DD y una fecha no pasada."

    if not validar_hora(nueva_hora):
        return f"Hora inválida. Solo se permiten horas entre 10:00 y 18:00, en punto o y media."

    if not validar_dia_valido(nueva_fecha):
        return "No se pueden registrar turnos los domingos."

    if nueva_fecha in feriados:
        return f"No se pueden programar turnos en días feriados ({nueva_fecha})."

    if not validar_anticipacion(nueva_fecha, nueva_hora):
        return "Los turnos deben modificarse con al menos 2 horas de anticipación."
    
    if not validar_limite_4_meses(nueva_fecha):
        return "No se pueden crear turnos con más de 4 meses de anticipación."
    

    clientes_sin_actual = [t for t in clientes if t != turno_actual]
    ok, mensaje = validar_capacidad_categoria(
        clientes_sin_actual,
        turno_actual["categoria"],
        nueva_fecha,
        nueva_hora
    )
    if not ok:
        return mensaje

    turno_actual["fecha"] = nueva_fecha
    turno_actual["hora"] = nueva_hora
    guardar_clientes(clientes)

    return f"Turno de {nombre} modificado a {nueva_fecha} a las {nueva_hora}."

def buscar_turno(nombre):
    """Busca turnos por nombre de cliente."""
    clientes = cargar_clientes()
    resultados = [t for t in clientes if nombre.lower() in t.get("nombre", "").lower()]

    if not resultados:
        return ["No se encontraron turnos para ese nombre."]

    return [
        f"{t.get('nombre')} - {t.get('categoria')} - {t.get('servicio')} - {t.get('fecha')} - {t.get('hora')}"
        for t in resultados
    ]

def exportar_csv():
    """Exporta los turnos a un archivo CSV."""
    clientes = cargar_clientes()
    with open("turnos.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Nombre", "Categoría", "Servicio", "Fecha", "Hora"])
        for turno in clientes:
            writer.writerow([
                turno.get("id", "Sin ID"),
                turno.get("nombre", "Desconocido"),
                turno.get("categoria", "Sin categoría"),
                turno.get("servicio", "Sin servicio"),
                turno.get("fecha", "Sin fecha"),
                turno.get("hora", "Sin hora")
            ])
    return "Exportación completada"

def obtener_estadisticas():
    """Genera estadísticas sobre los turnos registrados."""
    clientes = cargar_clientes()
    total_turnos = len(clientes)
    turnos_por_categoria = {}

    for turno in clientes:
        categoria = turno.get("categoria", "Sin categoría")
        turnos_por_categoria[categoria] = turnos_por_categoria.get(categoria, 0) + 1

    return {
        "total_turnos": total_turnos,
        "turnos_por_categoria": turnos_por_categoria
    }