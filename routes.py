from flask import Flask, render_template, request, redirect, url_for
import database
import models

app = Flask(__name__)

@app.route('/')
def index():
    dogs_data = database.get_available_dogs()
    available_dogs = []

    for row in dogs_data:
        # Verificamos si la fila tiene la columna de imagen (row[4])
        img = row[4] if len(row) >= 5 else 'default.jpg'
        
        # Creamos el objeto Dog pasando los 5 parámetros
        dog_obj = models.Dog(row[0], row[1], row[2], row[3], img)
        available_dogs.append(dog_obj)
    
    return render_template('catalogo.html', dogs=available_dogs)

@app.route('/adoptar/<int:dog_id>')
def form_adopcion(dog_id):
    dog = database.get_dog_by_id(dog_id)
    if not dog:
        return "Perrito no encontrado", 404
    
    # Aplicamos la misma lógica de seguridad aquí para la vista de confirmación
    img = dog[4] if len(dog) >= 5 else 'default.jpg'
    dog_obj = models.Dog(dog[0], dog[1], dog[2], dog[3], img)
    
    return render_template('confirmacion.html', dog=dog_obj)

@app.route('/confirmar_adopcion', methods=['POST'])
def procesar_adopcion():
    dog_id = request.form['dog_id']
    name = request.form['name']
    lastname = request.form['lastname']
    address = request.form['address']
    id_card = request.form['id_card']
    
    success = database.register_adoption_transactional(dog_id, name, lastname, address, id_card)
    
    if success:
        dog = database.get_dog_by_id(dog_id)
        # --- CAMBIAMOS ESTA LÍNEA PARA CARGAR LA PLANTILLA BONITA ---
        return render_template('gracias.html', dog_name=dog[1])
    else:
        return "Error al procesar la adopción (posible identificación duplicada). Por favor, inténtalo de nuevo. <a href='/'>Regresar</a>"

# --- Agregamos la nueva ruta de historial ---
@app.route('/historial-adopciones')
def historial_adopciones():
    from database import get_all_adoptions
    lista_adopciones = get_all_adoptions()
    return render_template('historial.html', adoptions=lista_adopciones)

# --- El arranque del servidor SIEMPRE debe ir al final absoluto ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)