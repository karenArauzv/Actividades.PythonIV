from pymongo import MongoClient

def conectar_biblioteca_bd():
   
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client["biblioteca"]
    coleccion = db["libros"]
    
    print("Conexion lista") 
    return coleccion

def agregar_libro(coleccion, titulo, autor, genero, estado_lectura):
    while estado_lectura not in ["Leído", "No leído"]:
        estado_lectura = input("Estado lectura inválido. Ingrese 'Leído' o 'No leído': ")

    libro = {"titulo": titulo, "autor": autor, "genero": genero, "estadoLectura": estado_lectura}
    coleccion.insert_one(libro)
    print("El libro ha sido agregado.")

def actualizar_libro(coleccion, libro_id, campo, nuevo_valor):
    resultado = coleccion.update_one({"_id": libro_id}, {"$set": {campo: nuevo_valor}})
    if resultado.modified_count:
        print("El libro ha sido actualizado.")
    else:
        print("No se encontro el libro.")

def eliminar_libro(coleccion, libro_id):
    resultado = coleccion.delete_one({"_id": libro_id})
    if resultado.deleted_count:
        print("El libro ha sido eliminado.")
    else:
        print("No se encontro el libro.")

def lista_libros(coleccion):
    libros = coleccion.find()
    for libro in libros:
        print(f"ID: {libro['_id']}, Título: {libro['titulo']}, Autor: {libro['autor']}, Género: {libro['genero']}, Estado: {libro['estadoLectura']}")

def buscar_libro(coleccion, campo, valor):
    libros = coleccion.find({campo: {"$regex": valor, "$options": "i"}})
    for libro in libros:
        print(f"ID: {libro['_id']}, Titulo: {libro['titulo']}, Autor: {libro['autor']}, Género: {libro['genero']}, Estado: {libro['estadoLectura']}")

def menu():
    coleccion = conectar_biblioteca_bd()
    print("\nBiblioteca")
    while True:
        print("\nMenú de mi Biblioteca")
        print("1. Agregar libro")
        print("2. Actualizar libro")
        print("3. Eliminar libro")
        print("4. Listar libros")
        print("5. Buscar libros")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            titulo = input("Titulo: ")
            autor = input("Autor: ")
            genero = input("Género: ")
            estado_lectura = input("Estado de lectura (Leído/No leído): ")
            agregar_libro(coleccion, titulo, autor, genero, estado_lectura)

        elif opcion == "2":
            libro_id = input("ID del libro : ")
            campo = input("Campo a actualizar (titulo, autor, genero, estadoLectura): ")
            nuevo_valor = input(f"Nuevo valor para {campo}: ")
            actualizar_libro(coleccion, libro_id, campo, nuevo_valor)

        elif opcion == "3":
            libro_id = input("ID del libro que desea eliminar: ")
            eliminar_libro(coleccion, libro_id)

        elif opcion == "4":
            lista_libros(coleccion)

        elif opcion == "5":
            campo = input("Buscar por titulo, autor, genero: ")
            valor = input("Valor de búsqueda: ")
            buscar_libro(coleccion, campo, valor)

        elif opcion == "6":
            print("Saliendo de la Biblioteca.")
            break

        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()