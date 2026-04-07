import config

def get_available_dogs():
    conn = config.get_db_connection()
    cur = conn.cursor()
    # Agregamos image_filename a la consulta (Son 5 cosas en total)
    cur.execute("SELECT id, name, age, breed, image_filename FROM Dog WHERE adopted = FALSE")
    dogs_data = cur.fetchall()
    conn.close()
    return dogs_data

def get_dog_by_id(dog_id):
    conn = config.get_db_connection()
    cur = conn.cursor()
    # Agregamos image_filename aquí también
    cur.execute("SELECT id, name, age, breed, image_filename FROM Dog WHERE id = ?", (dog_id,))
    dog_data = cur.fetchone()
    conn.close()
    return dog_data

def register_adoption_transactional(dog_id, adopter_name, adopter_lastname, address, id_card):
    conn = config.get_db_connection()
    if not conn: return False
    
    cur = conn.cursor()
    try:
        conn.autocommit = False 
        
        cur.execute("INSERT INTO Person (name, lastName, id_card) VALUES (?, ?, ?)", 
                   (adopter_name, adopter_lastname, id_card))
        person_id = cur.lastrowid
        
        cur.execute("INSERT INTO Adopter (person_id, address) VALUES (?, ?)", 
                   (person_id, address))
        
        cur.execute("INSERT INTO Adoption (adopter_id, dog_id) VALUES (?, ?)", 
                   (person_id, dog_id))
        
        cur.execute("UPDATE Dog SET adopted = TRUE WHERE id = ?", (dog_id,))
        
        conn.commit() 
        return True
        
    except Exception as e:
        conn.rollback() 
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def get_all_adoptions():
    conn = config.get_db_connection()
    cur = conn.cursor()
    # Unimos las tablas para saber el nombre del perro y del adoptante
    cur.execute("""
        SELECT Person.name, Person.lastName, Dog.name, Dog.breed 
        FROM Adoption
        JOIN Person ON Adoption.adopter_id = Person.id
        JOIN Dog ON Adoption.dog_id = Dog.id
    """)
    adoptions = cur.fetchall()
    conn.close()
    return adoptions

def get_all_adoptions():
    conn = config.get_db_connection()
    if not conn: return []
    
    cur = conn.cursor()
    try:
        # AGREGAMOS Dog.image_filename a la consulta SQL
        cur.execute("""
            SELECT Person.name, Person.lastName, Dog.name, Dog.breed, Dog.image_filename
            FROM Adoption
            JOIN Person ON Adoption.adopter_id = Person.id
            JOIN Dog ON Adoption.dog_id = Dog.id
        """)
        adoptions = cur.fetchall()
        return adoptions
    except Exception as e:
        print(f"Error al obtener adopciones: {e}")
        return []
    finally:
        conn.close()