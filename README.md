# Sistema de Turnos para Estética

Aplicación de escritorio desarrollada en Python que permite gestionar turnos para un centro de estética. A través de una interfaz gráfica simple, los empleados pueden agendar, cancelar, modificar y visualizar turnos, además de generar estadísticas y exportaciones.

---

## Interfaz Gráfica

La aplicación utiliza `tkinter` para mostrar una ventana interactiva desde la cual se realizan todas las acciones.

---

## Funcionalidades principales

- Asignar turnos por categoría y servicio.
- Validaciones de fecha, hora, feriados y capacidad.
- Cancelación y modificación de turnos existentes.
- Búsqueda de turnos por nombre.
- Visualización de estadísticas básicas.
- Exportación de turnos a CSV.

---

## Estructura del proyecto
turnos_estetica/
├── agregar_turno.py # Lógica para agregar, modificar, cancelar turnos y exportar CSV
├── cancelar_turnos.py # Módulo específico para cancelación de turnos
├── clientes.json # Archivo donde se almacenan los turnos
├── menu_cmd.py # Menú CMD
├── feriados.json # Lista de feriados cargada en formato JSON
├── graficos.py # Generación de gráficos y estadísticas
├── horarios.py # Reglas de horarios y control de feriados
├── interfaz.py # (main) Ventana principal con la interfaz gráfica
├── servicios.py # Definición de categorías y servicios disponibles
├── turnos.csv # Archivo de exportación de turnos
├── validaciones.py # Validaciones de datos (fecha, hora, capacidad, anticipación)
├── README.md # Este archivo

---

## Autores

Este proyecto fue realizado por:

- **Solange Blanc** 
- **Sandra Chisté**
- **Victoria Belén Mamberti** 
- **Leandro Plaza Puga** 

Trabajo realizado para la materia Programación I, FCAD - Universidad Nacional de Entre Ríos, año 2025.

---

## Requisitos

- Python 3.x
- No se necesitan bibliotecas externas (todo está hecho con módulos estándar como `tkinter`, `datetime`, `json`, `csv`, etc.)

---

## Cómo ejecutar la aplicación

1. Asegurate de tener Python 3 instalado.
2. Descargá o cloná este repositorio.
3. Desde la terminal (cmd en Windows), navegá a la carpeta donde está el archivo `interfaz.py`.
4. Ejecutá el siguiente comando:

```bash
python interfaz.py

---


