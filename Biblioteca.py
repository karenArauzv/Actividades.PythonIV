import sqlite3

def conectar_biblioteca_bd():
    conexion = sqlite3.connect('biblioteca.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        genero TEXT NOT NULL,
        estadoLectura TEXT NOT NULL CHECK(estadoLectura IN('Leído', 'No leído'))
        )
    ''')
    conexion.commit()
    return conexion

def agregar_libro(conexion, titulo, autor, genero, estadoLectura):
    while estadoLectura not in ["Leído", "No leído"]:
        estadoLectura = input("Estado lectura inválido. Ingrese 'Leído' o 'No leído': ")

    cursor = conexion.cursor()
    cursor.execute("INSERT INTO libros (titulo, autor, genero, estadoLectura) VALUES (?, ?, ?, ?)",
                   (titulo, autor, genero, estadoLectura))
    conexion.commit()
    print("El libro ha sido agregado")

def actualizar_libro(conexion, id_libro, estado_new):
    while estado_new not in ["Leído", "No leído"]:
        estado_new = input("Estado de lectura inválido. Ingrese 'Leído' o 'No leído': ")

    cursor = conexion.cursor()
    cursor.execute("UPDATE libros SET estadoLectura = ? WHERE id = ?", (estado_new, id_libro))
    conexion.commit()
    print("El estado del libro ha sido actualizado")

def eliminar_libro(conexion, id_libro):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
    conexion.commit()
    print("El libro ha sido eliminado")

def lista_libro(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT id, titulo, autor, genero, estadoLectura FROM libros")
    libros = cursor.fetchall()
    for libro in libros:
        print(f"id: {libro[0]}, Titulo: {libro[1]}, Autor: {libro[2]}, Genero: {libro[3]}, Estado de lectura: {libro[4]}")

def buscar_libro(conexion, nombre, valor):
    cursor = conexion.cursor()
    query = f"SELECT id, titulo, autor, genero, estadoLectura FROM libros WHERE {nombre} LIKE ?"
    cursor.execute(query, (f"%{valor}%",))
    libros = cursor.fetchall()
    for libro in libros:
        print(f"Id: {libro[0]}, Titulo: {libro[1]}, Autor: {libro[2]}, Genero: {libro[3]}, Estado de Lectura: {libro[4]}")

def menu():
    conexion = conectar_biblioteca_bd()
    print("\nBiblioteca")
    while True:
        print("\nMenú de mi Biblioteca")
        print("1. Agregar libro")
        print("2. Actualizar libro")
        print("3. Eliminar libro")
        print("4. Listar libros")
        print("5. Buscar libro")
        print("6. Salir")
        option = input("Seleccione una de las opciones: ")

        if option == "1":
            titulo = input("Titulo: ")
            autor = input("Autor: ")
            genero = input("Genero: ")
            estadoLectura = input("Estado lectura (Leído/No leído): ")
            agregar_libro(conexion, titulo, autor, genero, estadoLectura)

        elif option == "2":
            id_libro = int(input("ID de libro: "))
            estado_new = input("Estado de lectura nuevo (Leído/No leído): ")
            actualizar_libro(conexion, id_libro, estado_new)

        elif option == "3":
            id_libro = int(input("ID de libro que desea eliminar: "))
            eliminar_libro(conexion, id_libro)

        elif option == "4":
            lista_libro(conexion)

        elif option == "5":
            nombre = input("Buscar por (titulo, autor, genero): ")
            valor = input("Valor de búsqueda: ")
            buscar_libro(conexion, nombre, valor)

        elif option == "6":
            conexion.close()
            print("Saliendo de la Biblioteca")
            break

        else:
            print("La opción no existe. Intenta nuevamente.")

if __name__ == "__main__":
    menu()

