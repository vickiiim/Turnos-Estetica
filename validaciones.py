from datetime import datetime, timedelta
import re

HORARIOS_VALIDOS = [
    f"{h:02d}:{m:02d}"
    for h in range(10, 19)
    for m in (0, 30)
    if not (h == 18 and m == 30)
]

DIAS_VALIDOS = [0, 1, 2, 3, 4, 5]  #No se puede tomar turnos los domingos


def validar_nombre_completo(nombre):
    nombre = nombre.strip()
    if len(nombre) < 4:
        return False
    return bool(re.match(r"^[A-Za-zÁÉÍÓÚÑáéíóúñ ]+$", nombre))

def validar_fecha(fecha_str):
    """Valida formato YYYY-MM-DD y que no sea una fecha pasada."""
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        hoy = datetime.today().date()
        return fecha >= hoy
    except ValueError:
        return False

def validar_hora(hora_str):
    """
    Valida que la hora esté en formato HH:MM, 
    que sea entre 10:00 y 18:00, 
    y en punto o y media solamente.
    """
    if hora_str not in HORARIOS_VALIDOS:
        return False
    return True

def validar_no_vacios(campos):
    """Verifica que todos los campos estén completos (no vacíos)."""
    return all(campos)

def validar_dia_valido(fecha_str):
    """
    Valida que la fecha esté permitida según los días válidos (evita domingos u otros).
    """
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        return fecha.weekday() in DIAS_VALIDOS
    except ValueError:
        return False

def turno_duplicado(clientes, nuevo_turno):
    """Revisa si ya existe un turno con la misma fecha y hora para ese cliente."""
    for t in clientes:
        if (
            t.get("nombre") == nuevo_turno.get("nombre") and
            t.get("fecha") == nuevo_turno.get("fecha") and
            t.get("hora") == nuevo_turno.get("hora")
        ):
            return True
    return False

def validar_anticipacion(fecha_str, hora_str, anticipacion_minima_horas=2):
    """Valida que el turno se solicite con al menos X horas de anticipación."""
    try:
        fecha_turno = datetime.strptime(fecha_str, "%Y-%m-%d")
        hora_turno = datetime.strptime(hora_str, "%H:%M").time()
        turno_datetime = datetime.combine(fecha_turno, hora_turno)
        ahora = datetime.now()

        return turno_datetime >= ahora + timedelta(hours=anticipacion_minima_horas)
    except ValueError:
        return False

def validar_capacidad_categoria(clientes, categoria, fecha, hora):
    max_turnos = 2
    cantidad = sum(
    1 for t in clientes
    if t.get("categoria") == categoria and t.get("fecha") == fecha and t.get("hora") == hora
)
    if cantidad >= max_turnos:
        return False, "Ya hay 2 turnos registrados en esta categoría a esa hora."
    return True, ""

def validar_limite_4_meses(fecha_str):
    """
    Valida que la fecha no sea más allá de 4 meses desde hoy.
    """
    try:
        fecha_turno = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        fecha_limite = (datetime.today() + timedelta(days=120)).date()  # 4 meses aprox
        return fecha_turno <= fecha_limite
    except ValueError:
        return False