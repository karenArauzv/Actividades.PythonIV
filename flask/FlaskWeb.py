from flask import Flask, render_template, request, redirect, url_for
import redis
import json

app = Flask(__name__)

client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

def serialize_book(book):
    return json.dumps(book)

def deserialize_book(book_string):
    return json.loads(book_string)

@app.route('/')
def lista_libros():
    keys = client.keys("libro:*")
    libros = [deserialize_book(client.get(key)) for key in keys]
    return render_template('home.html', libros=libros)

@app.route('/agregar_libro', methods=['GET', 'POST'])
def agregar_libro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        genero = request.form['genero']
        estado_lectura = request.form['estadoLectura']
        libro_id = f"libro:{titulo}" 
        libro = {
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "estadoLectura": estado_lectura
        }
        client.set(libro_id, serialize_book(libro))
        return redirect(url_for('lista_libros'))
    return render_template('agregar_libro.html')

@app.route('/actuali_libro/<book_id>', methods=['GET', 'POST'])
def actualizar_libro(book_id):
    libro = deserialize_book(client.get(book_id))
    if request.method == 'POST':
        libro['titulo'] = request.form['titulo']
        libro['autor'] = request.form['autor']
        libro['genero'] = request.form['genero']
        libro['estadoLectura'] = request.form['estadoLectura']
        client.set(book_id, serialize_book(libro))
        return redirect(url_for('lista_libros'))
    return render_template('actuali_libro.html', libro=libro)

@app.route('/eliminar_libro/<book_id>')
def eliminar_libro(book_id):
    client.delete(book_id)
    return redirect(url_for('lista_libros'))

@app.route('/buscar_libros', methods=['GET', 'POST'])
def buscar_libros():
    if request.method == 'POST':
        query = request.form['query']
        campo = request.form['campo']
        keys = client.keys("libro:*")
        resultados = [
            deserialize_book(client.get(key))
            for key in keys
            if query.lower() in deserialize_book(client.get(key))[campo].lower()
        ]
        return render_template('buscar_resultados.html', libros=resultados)
    return render_template('buscar_libros.html')

if __name__ == '__main__':
    app.run(debug=True)