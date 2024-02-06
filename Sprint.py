'''
# MÓDULO 2: OBTENCIÓN Y PREPARACIÓN DE DATOS

- Nombre alumno: Sebastián Menares Arriaza


'''


import pandas as pd
import os
from datetime import datetime
import csv



# Función para cargar los datos previamente guardados
def cargar_datos():
    try:
        df_productos = pd.read_csv("productos.csv")
    except FileNotFoundError:
        df_productos = pd.DataFrame(columns=["Nombre", "Precio"])

    try:
        df_facturas = pd.read_csv("facturas.csv")
    except FileNotFoundError:
        df_facturas = pd.DataFrame(columns=["Producto", "Cantidad", "Precio_Unitario", "Total", "Nombre_Cliente", "Fecha_Hora"])

    return df_productos, df_facturas

# Función para guardar los datos en archivos CSV
def guardar_datos(productos, facturas):
    productos.to_csv("productos.csv", index=False)
    facturas.to_csv("facturas.csv", index=False)


# Función para ingresar un nuevo producto
def ingresar_producto(df_productos):
    nombre = input("Ingrese el nombre del producto: ")
    precio = float(input("Ingrese el precio del producto: "))
    df_productos = df_productos.append({"Nombre": nombre, "Precio": precio}, ignore_index=True)
    print("Producto ingresado correctamente.")
    return df_productos

# Función para mostrar el submenú de gestión de productos
def submenu_ingresar_producto(df_productos, df_facturas):
    while True:
        print("\n--- Submenú Ingresar Producto ---")
        print("1. Nuevo producto")
        print("2. Guardar producto")
        print("3. Volver")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            df_productos = ingresar_producto(df_productos)
        elif opcion == "2":
            guardar_datos(df_productos, df_facturas)
            print("Productos guardados correctamente.")
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")
# Función para guardar los datos de productos
def guardar_producto(df_productos):
    df_productos.to_csv("productos.csv", index=False)
    print("Productos guardados correctamente.")

def ingresar_factura(df_productos, df_facturas, cliente):
    # Crear un DataFrame vacío para los productos de la factura
    df_productos_factura = pd.DataFrame(columns=["Producto", "Cantidad", "Precio_Unitario", "Total", "Nombre_Cliente", "Fecha_Hora"])

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    productos_factura = []

    while True:
        nombre_producto = input("Ingrese el nombre del producto (o 'fin' para terminar): ")
        if nombre_producto.lower() == "fin":
            break
        if nombre_producto in df_productos["Nombre"].values:
            cantidad = int(input("Ingrese la cantidad: "))
            precio_unitario = df_productos.loc[df_productos["Nombre"] == nombre_producto, "Precio"].values[0]
            total_producto = precio_unitario * cantidad
            productos_factura.append((nombre_producto, cantidad, precio_unitario, total_producto))
        else:
            print("El producto no existe en el inventario.")

    # Agregar los productos a la factura
    for producto, cantidad, precio_unitario, total_producto in productos_factura:
        df_productos_factura = df_productos_factura.append({"Producto": producto, "Cantidad": cantidad,
                                                            "Precio_Unitario": precio_unitario, "Total": total_producto,
                                                            "Nombre_Cliente": cliente, "Fecha_Hora": fecha_hora}, ignore_index=True)

    print("Factura ingresada correctamente.")
    return df_productos_factura




# Función para mostrar el submenú de ingreso de factura
def submenu_ingresar_factura(df_productos, df_facturas):
    cliente = input("Ingrese el nombre del cliente: ")
    while True:
        print("\n--- Submenú Ingresar Factura ---")
        print("1. Ingresar producto")
        print("2. Guardar factura")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            df_facturas = ingresar_factura(df_productos, df_facturas, cliente)
        elif opcion == "2":
            guardar_datos(df_productos, df_facturas)
            print("Facturas guardadas correctamente.")
            break
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")

# Función para ver el resumen de ventas
def ver_resumen(facturas):
    cantidad_ventas = len(facturas)
    monto_total_vendido = facturas["Total"].sum()
    print(f"Cantidad de ventas: {cantidad_ventas}")
    print(f"Monto total vendido: {monto_total_vendido}")

# Función para desplegar ventas por usuario
def ventas_por_usuario(facturas):
    usuario = input("Ingrese el nombre de usuario: ")
    ventas_usuario = facturas[facturas["Nombre_Cliente"] == usuario]
    if not ventas_usuario.empty:
        print(ventas_usuario)
    else:
        print("No se encontraron ventas para el usuario:", usuario)

# Función para desplegar ventas por producto
def ventas_por_producto(facturas):
    producto = input("Ingrese el nombre del producto: ")
    ventas_producto = facturas[facturas["Producto"] == producto]
    if not ventas_producto.empty:
        print(ventas_producto)
    else:
        print("No se encontraron ventas para el producto:", producto)

# Función para desplegar ventas diarias
def ventas_diarias(facturas):
    fecha = input("Ingrese la fecha en formato DD/MM/AAAA: ")
    try:
        fecha_datetime = datetime.strptime(fecha, "%d/%m/%Y")
        ventas_fecha = facturas[facturas["Fecha"] == fecha_datetime.strftime("%Y-%m-%d")]
        if not ventas_fecha.empty:
            print(ventas_fecha)
        else:
            print("No se encontraron ventas para la fecha:", fecha)
    except ValueError:
        print("Formato de fecha incorrecto. Debe ser DD/MM/AAAA.")

# Función para guardar vista
def guardar_vista(facturas):
    nombre_archivo = input("Ingrese el nombre del archivo para guardar la vista: ")
    facturas.to_csv(nombre_archivo + ".csv", index=False)
    print("Vista guardada correctamente en", nombre_archivo + ".csv.")

# Función para ver detalle
def ver_detalle(facturas):
    while True:
        print("\n--- Submenú Ver Detalle ---")
        print("1. Ventas por usuario")
        print("2. Ventas por producto")
        print("3. Ventas diarias")
        print("4. Guardar vista")
        print("5. Volver")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            ventas_por_usuario(facturas)
        elif opcion == "2":
            ventas_por_producto(facturas)
        elif opcion == "3":
            ventas_diarias(facturas)
        elif opcion == "4":
            guardar_vista(facturas)
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")


# Función para borrar datos
def borrar_datos():
    while True:
        print("\n--- Submenú Borrar Datos ---")
        print("1. Eliminar productos")
        print("2. Eliminar facturas")
        print("3. Eliminar todo")
        print("4. Volver")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            if os.path.exists("productos.csv"):
                os.remove("productos.csv")
                print("Archivo 'productos.csv' eliminado.")
            else:
                print("No existe el archivo 'productos.csv'.")
        elif opcion == "2":
            if os.path.exists("facturas.csv"):
                os.remove("facturas.csv")
                print("Archivo 'facturas.csv' eliminado.")
            else:
                print("No existe el archivo 'facturas.csv'.")
        elif opcion == "3":
            if os.path.exists("productos.csv"):
                os.remove("productos.csv")
                print("Archivo 'productos.csv' eliminado.")
            else:
                print("No existe el archivo 'productos.csv'.")
            if os.path.exists("facturas.csv"):
                os.remove("facturas.csv")
                print("Archivo 'facturas.csv' eliminado.")
            else:
                print("No existe el archivo 'facturas.csv'.")
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

# Función principal
def main():
    productos, facturas = cargar_datos()
    while True:
        print("\n--- Menú Principal ---")
        print("1. Ingresar producto")
        print("2. Ingresar factura")
        print("3. Ver resumen")
        print("4. Ver detalle")
        print("5. Borrar datos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            submenu_ingresar_producto(productos, facturas)
        elif opcion == "2":
            submenu_ingresar_factura(productos, facturas)
        elif opcion == "3":
            ver_resumen(facturas)
        elif opcion == "4":
            ver_detalle(facturas)
        elif opcion == "5":
            borrar_datos()
        elif opcion == "6":
            #guardar_datos(productos, facturas)
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")

# Ejecutar el programa
if __name__ == "__main__":
    main()