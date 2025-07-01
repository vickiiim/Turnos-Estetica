import tkinter as tk
from collections import Counter
import math
from tkinter import messagebox
import tkinter.font as tkFont

COLORES = ["#66b3ff", "#99ff99", "#ffcc99", "#ff9999", "#c2c2f0", "#ffb3e6", "#d9f2d9"]

def mostrar_estadisticas_completas(clientes):
    if not clientes:
        messagebox.showinfo("Información", "No hay datos para mostrar.")
        return

    nombres = [c.get("nombre", "Desconocido") for c in clientes]
    contador_nombres = Counter(nombres)
    ranking_5 = contador_nombres.most_common(5)

    franjas = {
        "Mañana (10:00-15:00)": 0,
        "Tarde (15:30-18:00)": 0,
        "Otro horario": 0
    }
    for c in clientes:
        hora = c.get("hora", "")
        try:
            h, m = map(int, hora.split(":"))
            total_min = h * 60 + m
            if 10*60 <= total_min <= 15*60:
                franjas["Mañana (10:00-15:00)"] += 1
            elif 15*60 + 30 <= total_min <= 18*60:
                franjas["Tarde (15:30-18:00)"] += 1
            else:
                franjas["Otro horario"] += 1
        except:
            franjas["Otro horario"] += 1

    categorias = [c.get("categoria", "Desconocido") for c in clientes]
    contador_cat = Counter(categorias)

    # Ventana principal con scroll
    ventana = tk.Toplevel()
    ventana.title("Estadísticas de Turnos")
    ventana.geometry("800x800")
    ventana.configure(bg="white")

    canvas = tk.Canvas(ventana, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    frame_scroll = tk.Frame(canvas, bg="white")

    frame_scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Ranking de usuarios
    tk.Label(frame_scroll, text="Ranking: Top 5 Usuarios con más turnos", font=("Arial", 14, "bold"), bg="white").pack(pady=(10, 5), anchor="w", padx=10)
    for i, (nombre, cant) in enumerate(ranking_5, 1):
        tk.Label(frame_scroll, text=f"{i}. {nombre} - {cant} turno{'s' if cant > 1 else ''}", font=("Arial", 12), bg="white").pack(anchor="w", padx=30)

    tk.Label(frame_scroll, text="", bg="white").pack(pady=10)

    # Categorías
    tk.Label(frame_scroll, text="Cantidad de turnos por categoría", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=10)
    max_cant = max(contador_cat.values()) if contador_cat else 1
    barra_max = 30

    for i, (cat, cant) in enumerate(contador_cat.items()):
        barra = "█" * int((cant / max_cant) * barra_max)
        color = COLORES[i % len(COLORES)]

        frame = tk.Frame(frame_scroll, bg="white")
        frame.pack(anchor="w", padx=30, pady=2)

        tk.Label(frame, text=f"{cat:<15}", font=("Courier", 12), bg="white").pack(side="left")
        tk.Label(frame, text=barra, font=("Courier", 12), fg=color, bg="white").pack(side="left")
        tk.Label(frame, text=f" ({cant})", font=("Courier", 12), bg="white").pack(side="left")

    tk.Label(frame_scroll, text="", bg="white").pack(pady=10)

    # Gráfico de torta
    tk.Label(frame_scroll, text="Distribución de franjas horarias", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=10)

    canvas_torta = tk.Canvas(frame_scroll, width=800, height=600, bg="white", highlightthickness=1, highlightbackground="gray")
    canvas_torta.pack(pady=10, padx=10)

    franjas_filtradas = {k: v for k, v in franjas.items() if v > 0}
    total_franjas = sum(franjas_filtradas.values())
    if total_franjas == 0:
        total_franjas = 1

    inicio = 0
    cx, cy, r = 350, 250, 180
    colores_torta = ["#ff9999", "#66b3ff", "#99ff99"]
    font_etiqueta = tkFont.Font(family="Arial", size=9, weight="bold")

    for i, (franja, valor) in enumerate(franjas_filtradas.items()):
        angulo = (valor / total_franjas) * 360
        fin = inicio + angulo

        canvas_torta.create_arc(cx - r, cy - r, cx + r, cy + r,
                                start=inicio, extent=angulo,
                                fill=colores_torta[i % len(colores_torta)], outline="black")

        porcentaje = f"{(valor / total_franjas) * 100:.1f}%"
        texto_etiqueta = f"{franja}\n{porcentaje}"

        if franja == "Mañana (10:00-15:00)":
            angulo_salida = math.radians(fin)
            x_line = cx + r * math.cos(angulo_salida)
            y_line = cy - r * math.sin(angulo_salida)

            x_text = cx + r + 100
            y_text = cy - r
            anchor = "w"
        else:
            angulo_med = math.radians(inicio + angulo / 2)
            x_line = cx + r * math.cos(angulo_med)
            y_line = cy - r * math.sin(angulo_med)

            x_text = cx + (r + 80) * math.cos(angulo_med)
            y_text = cy - (r + 80) * math.sin(angulo_med)
            anchor = "w" if x_text >= cx else "e"

        canvas_torta.create_line(x_line, y_line, x_text, y_text, width=2)

        temp_text = canvas_torta.create_text(x_text, y_text, text=texto_etiqueta, font=font_etiqueta, fill="black", anchor=anchor)
        bbox_coords = canvas_torta.bbox(temp_text)
        canvas_torta.delete(temp_text)

        pad = 4
        canvas_torta.create_rectangle(
            bbox_coords[0] - pad, bbox_coords[1] - pad,
            bbox_coords[2] + pad, bbox_coords[3] + pad,
            fill="white", outline=""
        )
        canvas_torta.create_text(x_text, y_text, text=texto_etiqueta, font=font_etiqueta, fill="black", anchor=anchor)

        inicio = fin
