# gestion_empleados_gui.py
import tkinter as tk
from tkinter import messagebox, ttk
# Importa las funciones CRUD desde la lógica
from gestion_empleados_logica import create_empleado, read_empleados, update_empleado, delete_empleado

# --- LÓGICA DE LA GUI ---

def cargar_empleados_en_tabla(tabla):
    # Limpia datos antiguos
    for item in tabla.get_children():
        tabla.delete(item)
    
    # Llama a la función de lectura de la BD
    empleados = read_empleados()
    
    if not empleados:
        return

    # Si es la primera carga, define las columnas
    if not tabla["columns"]:
        columnas = list(empleados[0].keys())
        tabla["columns"] = columnas
        tabla.heading("#0", text="", anchor="w") 
        for col in columnas:
            tabla.heading(col, text=col.upper())
            tabla.column(col, anchor="center", width=100)

    # Inserta las filas
    for emp in empleados:
        valores_fila = [emp[col] for col in tabla["columns"]]
        tabla.insert(parent='', index='end', iid=emp['id_empleado'], values=valores_fila)


def guardar_empleado(entry_id, entry_nombre, entry_puesto, entry_fecha, tabla_empleados):
    """Función que maneja el botón Crear."""
    try:
        id_empleado = int(entry_id.get())
        nombre = entry_nombre.get()
        puesto = entry_puesto.get()
        fecha_contratacion = entry_fecha.get() 

        if not nombre or not puesto or not fecha_contratacion:
            messagebox.showwarning("Validación", "Todos los campos son obligatorios.")
            return

        if create_empleado(id_empleado, nombre, puesto, fecha_contratacion):
            messagebox.showinfo("Éxito", f"Empleado ID {id_empleado} registrado correctamente.")
            
            # Limpiar campos y recargar la tabla para mostrar el nuevo registro
            entry_id.delete(0, tk.END)
            entry_nombre.delete(0, tk.END)
            entry_puesto.delete(0, tk.END)
            entry_fecha.delete(0, tk.END)
            cargar_empleados_en_tabla(tabla_empleados) # <--- ACTUALIZA LA TABLA
            
    except ValueError:
        messagebox.showerror("Error de Datos", "El ID debe ser un número entero.")


# --- CONFIGURACIÓN DE LA VENTANA PRINCIPAL ---
def main_app():
    root = tk.Tk()
    root.title("Gestión de Empleados - CRUD Completo")
    root.geometry("800x600") 

    # --- FRAME DE FORMULARIO (CREAR/ACTUALIZAR) ---
    frame_form = tk.LabelFrame(root, text="CREAR NUEVO EMPLEADO")
    frame_form.pack(pady=10, padx=10, fill="x")
    
    # Definiciones de Entry (ID, Nombre, Puesto, Fecha)
    # ... (Crea aquí los Labels y Entry como en el código original)
    entry_id = tk.Entry(frame_form, width=20); entry_id.grid(row=0, column=1)
    # ... (Crea los demás campos)
    entry_nombre = tk.Entry(frame_form, width=30); entry_nombre.grid(row=1, column=1)
    entry_puesto = tk.Entry(frame_form, width=30); entry_puesto.grid(row=2, column=1)
    entry_fecha = tk.Entry(frame_form, width=30); entry_fecha.grid(row=3, column=1)
    
    # Botón Crear
    btn_guardar = tk.Button(frame_form, text=" Crear Empleado", 
                            command=lambda: guardar_empleado(entry_id, entry_nombre, entry_puesto, entry_fecha, tabla_empleados))
    btn_guardar.grid(row=4, column=0, columnspan=2, pady=10)

    # --- FRAME DE TABLA (LEER) ---
    frame_tabla = tk.Frame(root)
    frame_tabla.pack(pady=10, padx=10, fill='both', expand=True)

    # Configuración de la tabla (Treeview)
    tabla_empleados = ttk.Treeview(frame_tabla, show='headings') 
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_empleados.yview)
    tabla_empleados.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla_empleados.pack(side="left", fill='both', expand=True)

    # Botón para Recargar Datos
    btn_recargar = tk.Button(root, text=" Recargar/Ver Todos", command=lambda: cargar_empleados_en_tabla(tabla_empleados))
    btn_recargar.pack(pady=5)
    
    # Cargar los datos al iniciar la aplicación
    cargar_empleados_en_tabla(tabla_empleados)

    root.mainloop()

if __name__ == "__main__":
    main_app()