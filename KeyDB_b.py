import redis
import json

def conectar_biblioteca_bd():
    client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
    print("Conexión lista")
    return client

def agregar_libro(client, titulo, autor, genero, estado_lectura):
    while estado_lectura not in ["Leído", "No leído"]:
        estado_lectura = input("Estado lectura inválido. Ingrese 'Leído' o 'No leído': ")

    libro_id = f"libro:{titulo}" 
    libro = {"titulo": titulo, "autor": autor, "genero": genero, "estadoLectura": estado_lectura}
    client.set(libro_id, json.dumps(libro))
    print("El libro ha sido agregado.")

def actualizar_libro(client, libro_id, campo, nuevo_valor):
    libro = client.get(libro_id)
    if libro:
        libro_data = json.loads(libro)
        libro_data[campo] = nuevo_valor  
        client.set(libro_id, json.dumps(libro_data))
        print("El libro ha sido actualizado.")
    else:
        print("No se encontró el libro.")

def eliminar_libro(client, libro_id):
    resultado = client.delete(libro_id)
    if resultado:
        print("El libro ha sido eliminado.")
    else:
        print("No se encontró el libro.")

def lista_libros(client):
    keys = client.keys("libro:*")  
    for key in keys:
        libro = json.loads(client.get(key))
        print(f"ID: {key}, Título: {libro['titulo']}, Autor: {libro['autor']}, Género: {libro['genero']}, Estado: {libro['estadoLectura']}")

def buscar_libro(client, campo, valor):
    keys = client.keys("libro:*")
    for key in keys:
        libro = json.loads(client.get(key))
        if valor.lower() in libro[campo].lower():
            print(f"ID: {key}, Título: {libro['titulo']}, Autor: {libro['autor']}, Género: {libro['genero']}, Estado: {libro['estadoLectura']}")

def menu():
    client = conectar_biblioteca_bd()
    print("\nBiblioteca")
    while True:
        print("\nMenu de mi Biblioteca")
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
            agregar_libro(client, titulo, autor, genero, estado_lectura)

        elif opcion == "2":
            libro_id = input("ID del libro: ")
            campo = input("Campo a actualizar titulo, autor, genero, estado de Lectura: ")
            nuevo_valor = input(f"Nuevo valor para {campo}: ")
            actualizar_libro(client, libro_id, campo, nuevo_valor)

        elif opcion == "3":
            libro_id = input("ID del libro que desea eliminar: ")
            eliminar_libro(client, libro_id)

        elif opcion == "4":
            lista_libros(client)

        elif opcion == "5":
            campo = input("Buscar por titulo, autor, genero: ")
            valor = input("Valor de búsqueda: ")
            buscar_libro(client, campo, valor)

        elif opcion == "6":
            print("Saliendo de la Biblioteca.")
            client.close()  
            break

        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()