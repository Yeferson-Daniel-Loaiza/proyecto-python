import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import sys
import shutil

def conexion_base_datos():
    """Crea la carpeta 'src/db' y la base de datos si no existen."""
    # Obtener la ruta actual del script y construir la ruta de 'src/db' 
    ruta_carpeta = os.path.join("db")
    ruta_base_datos = os.path.join(ruta_carpeta, "inventario.db")

    # Crear la carpeta 'db' si no existe
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        print(f"Carpeta creada en: {ruta_carpeta}")

    # Conectar a la base de datos (SQLite crea el archivo si no existe)
    conexion = sqlite3.connect(ruta_base_datos)
    return conexion

# Ejemplo de función para crear tabla si no existe
def crear_tabla_si_no_existe():
    conexion = conexion_base_datos()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            codigo INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()


crear_tabla_si_no_existe()

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario")
        self.root.geometry("1000x600")
        self.root.attributes("-fullscreen", True)
        def conexion_base_datos():
            """Crea la carpeta 'src/db' y la base de datos si no existen."""
            # Obtener la ruta actual del script y construir la ruta de 'src/db'
            ruta_src = os.path.dirname(__file__)  # Ruta de la carpeta 'src'
            ruta_carpeta = os.path.join(ruta_src, "db")
            ruta_base_datos = os.path.join(ruta_carpeta, "inventario.db")

            # Crear la carpeta 'db' si no existe
            if not os.path.exists(ruta_carpeta):
                os.makedirs(ruta_carpeta)
                print(f"Carpeta creada en: {ruta_carpeta}")

            # Conectar a la base de datos (SQLite crea el archivo si no existe)
            conexion = sqlite3.connect(ruta_base_datos)
            return conexion


        def crear_tabla_si_no_existe():
            conexion = conexion_base_datos()
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    codigo INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL
                )
            """)
            conexion.commit()
            conexion.close()


        crear_tabla_si_no_existe()



        pantalla_completa = False

        # Función para alternar pantalla completa


        def alternar_fullscreen(event=None):
            global pantalla_completa
            pantalla_completa = not pantalla_completa  # Cambia el estado
            # Habilitar pantalla completa
            self.root.attributes("-fullscreen", pantalla_completa)


        # Vincular F11 para alternar pantalla completa
        self.root.bind("<F11>", alternar_fullscreen)

        # Salir del modo pantalla completa con Escape


        def salir_fullscreen(event=None):
            global pantalla_completa
            pantalla_completa = False
            self.root.attributes("-fullscreen", False)  # desabilitar pantalla completa


        self.root.bind("<Escape>", salir_fullscreen)

        # Lista para almacenar los productos
        self.productos = []

        # Crear widgets
        self.crear_widgets()
        self.actualizar_tabla()

    def crear_widgets(self):
        # Etiquetas y entradas
        tk.Label(self.root, text="Código de barras:").grid(row=0, column=0, padx=10, pady=10)
        self.codigo_entry = tk.Entry(self.root)
        self.codigo_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Nombre del producto:").grid(row=0, column=2, padx=10, pady=10)
        self.nombre_entry = tk.Entry(self.root)
        self.nombre_entry.grid(row=0, column=3, padx=10, pady=10)

        tk.Label(self.root, text="Cantidad:").grid(row=0, column=4, padx=10, pady=10)
        self.cantidad_entry = tk.Entry(self.root)
        self.cantidad_entry.grid(row=0, column=5, padx=10, pady=10)

        tk.Label(self.root, text="Precio:").grid(row=0, column=6, padx=10, pady=10)
        self.precio_entry = tk.Entry(self.root)
        self.precio_entry.grid(row=0, column=7, padx=10, pady=10)

        # Botones
        tk.Button(self.root, text="Agregar", command=self.agregar_producto).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Editar", command=self.editar_producto).grid(row=1, column=1, columnspan=2, pady=10)
        tk.Button(self.root, text="Eliminar", command=self.eliminar_productos).grid(row=1, column=3, columnspan=2, pady=10)
        tk.Button(self.root, text="Buscar", command=self.buscar_producto).grid(row=1, column=5, columnspan=2, pady=10)
        tk.Button(self.root, text="Actualizar", command=self.actualizar_tabla).grid(row=1, column=7, columnspan=2, pady=10)

        # Tabla
        frame_tabla = tk.Frame(self.root)
        frame_tabla.grid(row=2, column=0, columnspan=8, padx=10, pady=10)

        self.scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical")
        self.scrollbar_x = ttk.Scrollbar(frame_tabla, orient="horizontal")

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=("Código", "Nombre", "Cantidad", "Precio"),
            show="headings",
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set
        )

        self.scrollbar_y.config(command=self.tabla.yview)
        self.scrollbar_y.pack(side="right", fill="y")

        self.scrollbar_x.config(command=self.tabla.xview)
        self.scrollbar_x.pack(side="bottom", fill="x")

        self.tabla.heading("Código", text="Código")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Precio", text="Precio")
        self.tabla.column("Código", width=150)
        self.tabla.column("Nombre", width=200)
        self.tabla.column("Cantidad", width=100)
        self.tabla.column("Precio", width=100)
        self.tabla.pack(side="left", fill="both", expand=True)

    def agregar_producto(self,):
        codigo = self.codigo_entry.get()
        nombre = self.nombre_entry.get()
        cantidad = self.cantidad_entry.get()
        precio = self.precio_entry.get()

        if not codigo or not nombre or not cantidad or not precio:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
            
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número entero y Precio un número decimal.")
            return
        def agregar_productos():
            try:
                conexion= conexion_base_datos()
            except Exception as ex:
                print(ex)
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO productos (codigo, nombre, cantidad, precio) VALUES (?,?,?,?)",
                           (codigo, nombre, cantidad, precio))
            print("producto agregado")
            conexion.commit()
            conexion.close()
        agregar_productos()
        self.actualizar_tabla()
        self.limpiar_campos()

    def editar_producto(self):
        try:
            conexion = conexion_base_datos()  # Intentar establecer la conexión
        except Exception as ex:
            print(ex)
            return  # Salir de la función si no se pudo establecer la conexión

        def obtener_producto_por_codigo(codigo):
            conexion = conexion_base_datos()  # Abrir la conexión si es necesario
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
            producto = cursor.fetchone()
            conexion.close()
            return producto

        cursor = conexion.cursor()

        # Pedir al usuario el código del producto
        id_producto = self.codigo_entry.get().strip()
        producto = obtener_producto_por_codigo(id_producto)

        if producto:
            # nombre
            nuevo_valor_nombre = self.nombre_entry.get().strip()
            if nuevo_valor_nombre:
                cursor.execute("UPDATE productos SET nombre = ? WHERE codigo = ?", (nuevo_valor_nombre, id_producto))

            # cantidad
            nuevo_valor_cantidad = self.cantidad_entry.get().strip()
            if nuevo_valor_cantidad.isdigit():
                cursor.execute("UPDATE productos SET cantidad = ? WHERE codigo = ?", (nuevo_valor_cantidad, id_producto))

            # precio
            nuevo_valor_precio = self.precio_entry.get().strip()
            if nuevo_valor_precio.replace('.', '', 1).isdigit():  # Verificar si es un número válido
                cursor.execute("UPDATE productos SET precio = ? WHERE codigo = ?", (nuevo_valor_precio, id_producto))

            conexion.commit()
            messagebox.showinfo("Información", "Producto modificado correctamente")
        else:
            messagebox.showerror("Error",f"Producto con ese codigo no existe")

        if conexion:
            conexion.close()
        self.limpiar_campos()
    
    def eliminar_productos(self):
        def obtener_producto_por_codigo(codigo):
            conexion = conexion_base_datos()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
            producto = cursor.fetchone()
            conexion.close()
            return producto
        try:
            conexion = conexion_base_datos()
        except Exception as ex:
            print(ex)
        # pedir al ususario el codigo del producto
        id_producto = self.codigo_entry.get()

        producto = obtener_producto_por_codigo(id_producto)

        if producto:
            respuesta = messagebox.askquestion("Pregunta", f"¿Está seguro De eliminar:  {producto[1]}?")
            if respuesta == 'yes':
                try:
                    conexion = conexion_base_datos()
                    cursor = conexion.cursor()
                    cursor.execute(
                        "DELETE FROM productos WHERE codigo = ?", (id_producto,))
                    conexion.commit()
                    self.actualizar_tabla()
                except sqlite3.Error as ex:
                    print(f"Error al eliminar el producto: {ex}")
                finally:
                    if conexion:
                        conexion.close()
                        
        else:
            messagebox.showerror("Error",f"Producto con el codigo no encotrado")
            return
        self.limpiar_campos()
    def buscar_producto(self):
        codigo_de_barra = self.codigo_entry.get()
        def obtener_producto_por_codigo(codigo):
            conexion = conexion_base_datos()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
            producto = cursor.fetchone()
            conexion.close()
            return producto
        
        producto=obtener_producto_por_codigo(codigo_de_barra)
        precio_formateado = f"{producto[3]:,.2f}".replace(",", ".") 
        messagebox.showinfo(
            "Información", 
                f"Se encontró este producto:\n\n"
                f"Código de barras: {producto[0]}\n"
                f"Nombre del producto: {producto[1]}\n"
                f"Cantidad en stock: {producto[2]}\n"
                f"Precio del producto: {precio_formateado}")

    def actualizar_tabla(self,event=None):
        try:
            conexion = conexion_base_datos()
        except Exception as ex:
            print(ex)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        resultados = cursor.fetchall()
        
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for producto in resultados:
            precio_formateado = f"{producto[3]:,.0f}".replace(",", ".")
            self.tabla.insert("", "end", values=(producto[0], producto[1], producto[2], precio_formateado))
        conexion.close()
    def limpiar_campos(self):
        self.codigo_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)

# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()
