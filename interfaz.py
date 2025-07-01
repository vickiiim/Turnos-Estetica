import tkinter as tk
from tkinter import ttk, messagebox
from agregar_turno import agregar_turno, cancelar_turno, modificar_turno, exportar_csv, buscar_turno, cargar_clientes
from servicios import CATEGORIAS
from graficos import mostrar_estadisticas_completas
from validaciones import (
    validar_anticipacion, validar_fecha, validar_hora, validar_limite_4_meses, validar_nombre_completo,
    validar_no_vacios, validar_dia_valido, turno_duplicado, validar_capacidad_categoria,
    HORARIOS_VALIDOS, 
)
import subprocess

def actualizar_servicios(event):
    """Actualiza los servicios según la categoría seleccionada."""
    categoria = combo_categoria.get()
    combo_servicio["values"] = CATEGORIAS.get(categoria, [])

def registrar_turno_gui():
    """Registra turnos en la interfaz."""
    nombre = entry_nombre.get()
    categoria = combo_categoria.get()
    servicio = combo_servicio.get()
    fecha = entry_fecha.get()
    hora = combo_hora.get()

   
    if not validar_no_vacios([nombre, categoria, servicio, fecha, hora]):
        messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
        return

    if not validar_nombre_completo(nombre):
        messagebox.showwarning("Nombre inválido", "El nombre debe tener al menos 4 letras y solo contener letras y espacios.")
        return

    if not validar_fecha(fecha):
        messagebox.showwarning("Fecha inválida", "Ingrese una fecha válida en formato YYYY-MM-DD y que no sea pasada.")
        return

    if not validar_dia_valido(fecha):
        messagebox.showwarning("Día no disponible", "No se pueden registrar turnos los domingos.")
        return

    if not validar_hora(hora):
        messagebox.showwarning("Hora inválida", "Ingrese una hora válida en punto o y media entre 10:00 y 18:00.")
        return

    if not validar_anticipacion(fecha, hora):
        messagebox.showwarning(
            "Anticipación insuficiente",
            "Los turnos deben solicitarse con al menos 2 horas de anticipación."
        )
        return
    
    if not validar_limite_4_meses(fecha):
        messagebox.showwarning(
        "Fecha inválida", 
        "No se pueden crear o modificar turnos con más de 4 meses de anticipación."
    )
        return

    clientes = cargar_clientes()

    turno = {
        "nombre": nombre.strip(),
        "categoria": categoria,
        "servicio": servicio,
        "fecha": fecha,
        "hora": hora
    }

    
    if turno_duplicado(clientes, turno):
        messagebox.showerror("Duplicado", f"{nombre} ya tiene un turno registrado el {fecha} a las {hora}.")
        return

    
    disponible, mensaje = validar_capacidad_categoria(clientes, categoria, fecha, hora)
    if not disponible:
        messagebox.showerror("Capacidad", mensaje)
        return

    
    resultado = agregar_turno(turno)
    messagebox.showinfo("Resultado", resultado)


def cancelar_turno_gui():
    nombre = entry_nombre.get()
    resultado = cancelar_turno(nombre)
    messagebox.showinfo("Resultado", resultado)

def modificar_turno_gui():
    nombre = entry_nombre.get()
    nueva_fecha = entry_fecha.get()
    nueva_hora = combo_hora.get()

    if not validar_no_vacios([nombre, nueva_fecha, nueva_hora]):
        messagebox.showwarning("Campos vacíos", "Complete los datos para modificar el turno.")
        return

    if not validar_fecha(nueva_fecha):
        messagebox.showwarning("Fecha inválida", "Ingrese una fecha válida en formato YYYY-MM-DD y que no sea pasada.")
        return

    if not validar_dia_valido(nueva_fecha):
        messagebox.showwarning("Día no válido", "No se pueden registrar turnos los domingos.")
        return

    if not validar_hora(nueva_hora):
        messagebox.showwarning("Hora inválida", "Ingrese una hora válida en punto o y media entre 10:00 y 18:00.")
        return

    if not validar_anticipacion(nueva_fecha, nueva_hora):
        messagebox.showwarning("Anticipación insuficiente", "Los turnos deben modificarse con al menos 2 horas de anticipación.")
        return
    
    if not validar_limite_4_meses(nueva_fecha):
        messagebox.showwarning(
        "Fecha inválida", 
        "No se pueden crear o modificar turnos con más de 4 meses de anticipación."
    )
        return
    

    clientes = cargar_clientes()

    
    turno_actual = next((t for t in clientes if t.get("nombre") == nombre), None)
    if not turno_actual:
        messagebox.showerror("Error", "Turno no encontrado.")
        return

    
    clientes_sin_actual = [t for t in clientes if t != turno_actual]
    ok, mensaje = validar_capacidad_categoria(clientes_sin_actual, turno_actual["categoria"], nueva_fecha, nueva_hora)
    if not ok:
        messagebox.showerror("Capacidad", mensaje)
        return

    
    resultado = modificar_turno(nombre, nueva_fecha, nueva_hora)
    messagebox.showinfo("Resultado", resultado)

def exportar_turnos_gui():
    exportar_csv()
    messagebox.showinfo("Exportación", "Turnos exportados correctamente a turnos.csv.")

def buscar_turno_gui():
    nombre = entry_nombre.get()
    if not nombre:
        messagebox.showwarning("Campos vacíos", "Ingrese el nombre del cliente para buscar turnos.")
        return

    resultados = buscar_turno(nombre)
    messagebox.showinfo("Resultado", "\n".join(resultados))

def estadisticas_gui():
    clientes = cargar_clientes()
    if not clientes:
        messagebox.showinfo("Información", "No hay turnos registrados para mostrar estadísticas.")
        return
    mostrar_estadisticas_completas(clientes)

def abrir_cancelar_turnos():
    subprocess.Popen(["python", "cancelar_turnos.py"])

# Ventana principal
root = tk.Tk()
root.title("Sistema de Turnos Estética")
root.geometry("420x520")

tk.Label(root, text="Nombre del Cliente:").pack()
entry_nombre = tk.Entry(root)
entry_nombre.pack()

tk.Label(root, text="Categoría de Servicio:").pack()
combo_categoria = ttk.Combobox(root, values=list(CATEGORIAS.keys()), state="readonly")
combo_categoria.pack()
combo_categoria.bind("<<ComboboxSelected>>", actualizar_servicios)

tk.Label(root, text="Servicio:").pack()
combo_servicio = ttk.Combobox(root, state="readonly")
combo_servicio.pack()

tk.Label(root, text="Fecha (YYYY-MM-DD):").pack()
entry_fecha = tk.Entry(root)
entry_fecha.pack()

tk.Label(root, text="Hora:").pack()
combo_hora = ttk.Combobox(root, values=HORARIOS_VALIDOS, state="readonly")
combo_hora.pack()

tk.Button(root, text="Registrar Turno", command=registrar_turno_gui).pack(pady=3)
tk.Button(root, text="Cancelar Turno", command=abrir_cancelar_turnos).pack(pady=3)
tk.Button(root, text="Modificar Turno", command=modificar_turno_gui).pack(pady=3)
tk.Button(root, text="Exportar Turnos a CSV", command=exportar_turnos_gui).pack(pady=3)
tk.Button(root, text="Buscar Turno", command=buscar_turno_gui).pack(pady=3)
tk.Button(root, text="Ver Estadísticas", command=estadisticas_gui).pack(pady=3)

root.mainloop()