from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk  # Importar ttk desde tkinter

# Conectarse a la base de datos
client = MongoClient('mongodb://localhost:27017/')
db = client['ARZA']

# Crear la ventana
ventana = tk.Tk()
ventana.title("Consulta de Stock")
ventana.geometry("600x400")

# Obtener las colecciones disponibles
colecciones = db.list_collection_names()

# Variables para almacenar las selecciones del usuario
coleccion_var = tk.StringVar(ventana)
coleccion_var.set("Seleccione una colección")

categoria_var = tk.StringVar(ventana)
categoria_var.set("Seleccione una categoría")

producto_var = tk.StringVar(ventana)
producto_var.set("Seleccione un producto")

color_var = tk.StringVar(ventana)
color_var.set("Seleccione un color")

talla_var = tk.StringVar(ventana)
talla_var.set("Seleccione una talla")

# Función para actualizar las opciones cuando se selecciona una colección o categoría
def actualizar_opciones(*args):
    # Obtener la colección seleccionada
    coleccion_seleccionada = coleccion_var.get()

    # Obtener las categorías disponibles para la colección seleccionada
    categorias = db[coleccion_seleccionada].distinct("categoria")

    # Limpiar y actualizar la lista de categorías
    categoria_var.set("Seleccione una categoría")
    categoria_combobox['values'] = categorias
    categoria_combobox.set("Seleccione una categoría")

    # Limpiar las opciones de producto, color y talla
    producto_var.set("Seleccione un producto")
    producto_combobox.set("Seleccione un producto")
    color_var.set("Seleccione un color")
    color_combobox.set("Seleccione un color")
    talla_var.set("Seleccione una talla")
    talla_combobox.set("Seleccione una talla")

# Función para actualizar las opciones cuando se selecciona una categoría o producto
def actualizar_opciones_producto(*args):
    # Obtener la colección y categoría seleccionadas
    coleccion_seleccionada = coleccion_var.get()
    categoria_seleccionada = categoria_var.get()

    # Obtener los productos disponibles para la colección y categoría seleccionadas
    productos = db[coleccion_seleccionada].distinct("nombre", {"categoria": categoria_seleccionada})

    # Limpiar y actualizar la lista de productos
    producto_var.set("Seleccione un producto")
    producto_combobox['values'] = productos
    producto_combobox.set("Seleccione un producto")

    # Limpiar las opciones de color y talla
    color_var.set("Seleccione un color")
    color_combobox.set("Seleccione un color")
    talla_var.set("Seleccione una talla")
    talla_combobox.set("Seleccione una talla")

# Función para actualizar las opciones cuando se selecciona un producto o color
def actualizar_opciones_color(*args):
    # Obtener la colección, categoría y producto seleccionados
    coleccion_seleccionada = coleccion_var.get()
    categoria_seleccionada = categoria_var.get()
    producto_seleccionado = producto_var.get()

    # Obtener los colores disponibles para la colección, categoría y producto seleccionados
    colores = db[coleccion_seleccionada].find_one({"categoria": categoria_seleccionada, "nombre": producto_seleccionado})

    # Verificar si se encontraron colores
    if colores and 'colores' in colores:
        colores = colores['colores']

        # Limpiar y actualizar la lista de colores
        color_var.set("Seleccione un color")
        color_combobox['values'] = [color['color'] for color in colores]
        color_combobox.set("Seleccione un color")

    # Limpiar la opción de talla
    talla_var.set("Seleccione una talla")
    talla_combobox.set("Seleccione una talla")

# Función para actualizar las opciones cuando se selecciona un color o talla
def actualizar_opciones_talla(*args):
    # Obtener la colección, categoría, producto y color seleccionados
    coleccion_seleccionada = coleccion_var.get()
    categoria_seleccionada = categoria_var.get()
    producto_seleccionado = producto_var.get()
    color_seleccionado = color_var.get()

    # Obtener las tallas disponibles para la colección, categoría, producto y color seleccionados
    tallas = db[coleccion_seleccionada].distinct("colores.tallas.talla", {"categoria": categoria_seleccionada, "nombre": producto_seleccionado, "colores.color": color_seleccionado})

    # Limpiar y actualizar la lista de tallas
    talla_var.set("Seleccione una talla")
    talla_combobox['values'] = tallas
    talla_combobox.set("Seleccione una talla")

# Función para realizar la consulta de stock
def consultar_stock():
    # Obtener las selecciones del usuario
    coleccion_seleccionada = coleccion_var.get()
    categoria_seleccionada = categoria_var.get()
    producto_seleccionado = producto_var.get()
    color_seleccionado = color_var.get()
    talla_seleccionada = talla_var.get()

    # Validar que se hayan seleccionado todos los valores
    if (coleccion_seleccionada == "Seleccione una colección" or
        categoria_seleccionada == "Seleccione una categoría" or
        producto_seleccionado == "Seleccione un producto" or
        color_seleccionado == "Seleccione un color" or
        talla_seleccionada == "Seleccione una talla"):
        resultado_label.config(text="Por favor, seleccione todos los valores.")
        return

    # Realizar la consulta en la base de datos (aquí debes agregar tu lógica de consulta)
    # En este ejemplo, simplemente mostraremos un mensaje
    resultado_label.config(text=f"Quedan 10 {producto_seleccionado} de color {color_seleccionado} y talla {talla_seleccionada} en stock.")

    # Realizar la consulta en la base de datos
    consulta = {
        "categoria": categoria_seleccionada,
        "nombre": producto_seleccionado,
        "colores.color": color_seleccionado,
        "colores.tallas.talla": talla_seleccionada
    }

    # Obtener el stock desde la base de datos
    resultado = db[coleccion_seleccionada].find_one(consulta, {"_id": 0, "colores.$": 1})

    # Verificar si se encontró la información de stock
    if resultado and "colores" in resultado:
        color_info = resultado["colores"][0]
        cantidad_disponible = 0

        # Buscar la cantidad disponible para la talla seleccionada
        for talla_info in color_info["tallas"]:
            if talla_info["talla"] == talla_seleccionada:
                cantidad_disponible = talla_info["cantidad"]
                break

        resultado_label.config(text=f"Quedan {cantidad_disponible} unidades de {producto_seleccionado} en talla {talla_seleccionada}.")
    else:
        resultado_label.config(text="No se encontró información de stock para el producto seleccionado.")

# Crear y colocar los Combobox para colección, categoría, producto, color y talla
coleccion_combobox = ttk.Combobox(ventana, textvariable=coleccion_var, values=colecciones, state="readonly")
coleccion_combobox.pack(pady=30)

categoria_combobox = ttk.Combobox(ventana, textvariable=categoria_var, values=["Seleccione una categoría"], state="readonly")
categoria_combobox.pack(pady=10)

producto_combobox = ttk.Combobox(ventana, textvariable=producto_var, values=["Seleccione un producto"], state="readonly")
producto_combobox.pack(pady=10)

color_combobox = ttk.Combobox(ventana, textvariable=color_var, values=["Seleccione un color"], state="readonly")
color_combobox.pack(pady=10)

talla_combobox = ttk.Combobox(ventana, textvariable=talla_var, values=["Seleccione una talla"], state="readonly")
talla_combobox.pack(pady=10)

# Botón para consultar stock
consultar_boton = tk.Button(ventana, text="Consultar Stock", command=consultar_stock)
consultar_boton.pack(pady=30)

# Etiqueta para mostrar el resultado
resultado_label = tk.Label(ventana, text="")
resultado_label.pack()

# Asignar funciones de actualización a los Combobox
coleccion_combobox.bind("<<ComboboxSelected>>", actualizar_opciones)
categoria_combobox.bind("<<ComboboxSelected>>", actualizar_opciones_producto)
producto_combobox.bind("<<ComboboxSelected>>", actualizar_opciones_color)
color_combobox.bind("<<ComboboxSelected>>", actualizar_opciones_talla)

# Iniciar la interfaz gráfica
ventana.mainloop()