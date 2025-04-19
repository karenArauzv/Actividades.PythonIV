#Parcial 1  PDCIV

import json

ArchivoPresupuesto = 'presupuesto.json'

def cargarDatos():
    try:
        with open(ArchivoPresupuesto, 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []


def guardarDatos(datos):
    with open(ArchivoPresupuesto, 'w') as archivo:
        json.dump(datos, archivo)


def registrarArt():
    datos = cargarDatos()
    nombreArt = input("Nombre del articulo: ")
    precio = float(input("Precio del articulo: "))
    datos.append({"nombre": nombreArt, "precio": precio})
    guardarDatos(datos)
    print("Articulo registrado correctamente")


def buscarArt():
    datos = cargarDatos()
    articulo = input("ingrese Articulos que desea buscar: ")
    resultado = [art for art in datos if articulo.lower() in art['nombre'].lower()]
    if resultado:
        print("resultado de la busqueda: ")
        for i, art in enumerate(resultado):
            print(f"{i + 1}. {art['nombre']} - ${art['precio']:.2f}")
        else:
            print("No se encontraron artículos.")

def editarArt():
    datos = cargarDatos()
    buscarArt()
    art = input("ingrese Articulo que desea editar: ")
    if 0 < art < len(datos):
        print("Deje el este espacio vacio")
        nuevoNombre = input("Nombre del articulo que desea editar: ")
        nuevoPrecio = input("Precio del articulo que desea editar: ")
        if nuevoNombre:
            datos[art]['nombre'] = nuevoNombre
        if nuevoPrecio:
            datos[art]['precio'] = float(nuevoPrecio)
        guardarDatos(datos)
        print("Articulo editando correctamente")
    else:
        print("Articulo invalido")


def eliminarArt():
    datos = cargarDatos()
    buscarArt()
    art = int(input("ingrese Articulo que desea eliminar: "))
    if 0 < art < len(datos):
        datos.pop(art)
        guardarDatos(datos)
        print("Articulo eliminado correctamente")
    else:
        print("Articulo invalido")

def menu():
    while True:
        print("Presupuesto")
        print("Menú de Articulo")
        print("1. Registrar Articulo")
        print("2. Buscar Articulo")
        print("3. Editar Articulo")
        print("4. Eliminar Articulo")
        print("5. Salir ")
        choose = input("Seleccione una opción: ")

        if choose == "1":
            registrarArt()
        elif choose == "2":
            buscarArt()
        elif choose == "3":
            editarArt()
        elif choose == "4":
            eliminarArt()
        elif choose == "5":
            print("Salir")
            break
        else:
            print("Opcion no valida")

menu()





