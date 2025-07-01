import json
from datetime import datetime

def cargar_feriados():
    """Carga la lista de feriados desde un archivo JSON."""
    try:
        with open("feriados.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
            return datos.get("feriados", [])  
    except FileNotFoundError:
        print("⚠ Error: No se encontró el archivo 'feriados.json'.")
        return []
    except json.JSONDecodeError:
        print("⚠ Error: Formato incorrecto en 'feriados.json'.")
        return []

FERIADOS_ARG = cargar_feriados()

def turno_disponible(clientes, fecha, hora):
    """Verifica si el horario ya está ocupado."""
    for turno in clientes:
        if "fecha" in turno and "hora" in turno:  # Previene KeyError
            if turno["fecha"] == fecha and turno["hora"] == hora:
                return False  # Turno ya ocupado
    return True  # Turno disponible


def horario_disponible(clientes, categoria, hora, fecha):
    """Verifica disponibilidad de horarios evitando feriados."""
    try:
        fecha_turno = datetime.strptime(fecha, "%Y-%m-%d")
        hora_turno = datetime.strptime(hora, "%H:%M")
    except ValueError:
        return False

    if fecha_turno.strftime("%Y-%m-%d") in FERIADOS_ARG:
        return False  

    for turno in clientes:
        if turno.get("categoria") == categoria and turno.get("fecha") == fecha:
            hora_existente = datetime.strptime(turno["hora"], "%H:%M")
            if abs((hora_turno - hora_existente).total_seconds()) / 3600 < 1:
                return False
    return True





