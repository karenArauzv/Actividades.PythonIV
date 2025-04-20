from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from celery import Celery
import redis
import json


app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

app.config['MAIL_SERVER'] = 'smtp.example.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tu_correo@example.com'  
app.config['MAIL_PASSWORD'] = 'tu_contraseña'          
mail = Mail(app)


client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)


def serialize_book(book):
    return json.dumps(book)

def deserialize_book(book_string):
    return json.loads(book_string)

@celery.task
def enviar_correo(asunto, destinatario, cuerpo):
    """Función para enviar correos de manera asíncrona."""
    try:
        with app.app_context():
            msg = Message(asunto, recipients=[destinatario])
            msg.body = cuerpo
            mail.send(msg)
            print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


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

        
        enviar_correo.delay(
            asunto="Libro agregado exitosamente",
            destinatario="usuario@example.com",  
            cuerpo=f"El libro '{titulo}' ha sido agregado a tu biblioteca."
        )

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
    return render_template('actuali_libro.html', libro=libro, book_id=book_id)


@app.route('/eliminar_libro/<book_id>', methods=['POST'])
def eliminar_libro(book_id):
    libro = deserialize_book(client.get(book_id))
    client.delete(book_id)

    
    enviar_correo.delay(
        asunto="Libro eliminado",
        destinatario="usuario@example.com", 
        cuerpo=f"El libro '{libro['titulo']}' ha sido eliminado de tu biblioteca."
    )

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
        return render_template('buscar_libros.html', libros=resultados)
    return render_template('buscar_libros.html', libros=[])

if  __name__ == '__main__':
    app.run(debug=True)

