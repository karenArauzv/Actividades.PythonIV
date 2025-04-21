from flask import Flask, jsonify
import json

app = Flask(__name__)
with open('datosVacunacion.json', 'r') as archivo:
    datos = json.load(archivo)

@app.route('/')
def inicio():
    return jsonify({"mensaje:" : "🗺️👨‍⚕️👩‍⚕️Bienvenido a la API de vacunación en Panamá. Usa /api/vacunacion"})

@app.route('/api/vacunacion', methods=['GET'])
def obtener_todos_los_datos():
    return jsonify(datos)

@app.route('/api/vacunacion/<int:year>', methods=['GET'])
def obtener_datos_por_year(year):
    resultado = [d for d in datos if d['año'] == year]
    if resultado:
        return jsonify(resultado[0])
    else:
        return jsonify({"mensaje": "Datos no encontrados para el año especificado."}), 404

@app.route('/api/vacunacion/region/<region>', methods=['GET'])
def obtener_datos_por_region(region):
    return jsonify({
        "mensaje": f"No hay datos disponibles por región ('{region}') en este conjunto de datos."
    }), 501

@app.route('/api/vacunacion/edad/<int:edad_meses>', methods=['GET'])
def obtener_datos_por_edad_meses(edad_meses):
    resultado = [d for d in datos if d['edad_meses'] == edad_meses]
    if resultado:
        return jsonify(resultado)
    else:
        return jsonify({"mensaje": "No hay datos con esa edad."}), 404

if __name__ == '__main__':
    app.run(debug=True)
