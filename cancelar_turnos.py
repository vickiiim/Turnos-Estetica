import tkinter as tk
from tkinter import messagebox
import json
import os

RUTA_CLIENTES = "clientes.json"

def cargar_turnos():
    if not os.path.exists(RUTA_CLIENTES):
        return []
    with open(RUTA_CLIENTES, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def guardar_turnos(turnos):
    with open(RUTA_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(turnos, f, ensure_ascii=False, indent=2)

def ventana_cancelar_turno():
    turnos = cargar_turnos()
    if not turnos:
        messagebox.showinfo("Sin turnos", "No hay turnos para cancelar.")
        return

    ventana = tk.Toplevel()
    ventana.title("Selecciona turno a cancelar")

    lista = tk.Listbox(ventana, width=60)
    lista.pack(padx=10, pady=10)

    for turno in turnos:
        # Si es diccionario
        if isinstance(turno, dict):
            cliente = turno.get('cliente', '') or turno.get('nombre', '')
            fecha = turno.get('fecha', '')
            hora = turno.get('hora', '')
            servicio = turno.get('servicio', '')
        elif isinstance(turno, (tuple, list)):
            cliente = turno[0] if len(turno) > 0 else ''
            fecha = turno[1] if len(turno) > 1 else ''
            hora = turno[2] if len(turno) > 2 else ''
            servicio = turno[3] if len(turno) > 3 else ''
        else:
            cliente = fecha = hora = servicio = ''
        texto = f"{fecha} {hora} - {cliente} ({servicio})"
        lista.insert(tk.END, texto)

    def cancelar_turno():
        seleccion = lista.curselection()
        if seleccion:
            idx = seleccion[0]
            turno = turnos[idx]
            respuesta = messagebox.askyesno(
                "Confirmar",
                f"¿Cancelar turno?"
            )
            if respuesta:
                del turnos[idx]
                guardar_turnos(turnos)
                lista.delete(idx)
                messagebox.showinfo("Cancelado", "Turno cancelado.")
        else:
            messagebox.showwarning("Atención", "Selecciona un turno para cancelar.")

    btn_cancelar = tk.Button(ventana, text="Cancelar turno seleccionado", command=cancelar_turno)
    btn_cancelar.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    ventana_cancelar_turno()
    root.mainloop()