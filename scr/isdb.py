import sqlite3

class TablaValidacion():
    def crearBD(self):
        conn = sqlite3.connect('Notas.db') #crea la Bd
        conn.commit() #Guarda CAmbios
        conn.close()

    def crearTabla(self):
        conn = sqlite3.connect('Notas.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        cursor.execute(
            """create table if not exists descargas (
            id int,
            campana text,
            reporte text,
            descarga int
            )
        """)
        conn.commit() 
        conn.close()

    def agregarDatos(self, id, campana, reporte, descarga):
        conn = sqlite3.connect('Notas.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        cursor.execute(f"insert into descargas values('{id}', {campana},'{reporte}', '{descarga}')")
        conn.commit() 
        conn.close() 

    def agregarVariosDatos(self, lista):
        conn = sqlite3.connect('Notas.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        consulta = f"insert into descargas values(?, ?, ?, ?)"
        cursor.executemany(consulta, lista)
        conn.commit() 
        conn.close() 

    def truncateTable(self):
        conn = sqlite3.connect('Notas.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        cursor.execute(f"delete from descargas")
        conn.commit() 
        conn.close()

    def deleteTable(self, id):
        conn = sqlite3.connect('Notas.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        cursor.execute(f"delete from descargas where id = '{id}'")
        conn.commit() 
        conn.close()

    def leerDatos(self):
        conn = sqlite3.connect('Notas.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        consulta = f"SELECT * FROM descargas ORDER BY id DESC LIMIT 1"
        cursor.execute(consulta)
        data = cursor.fetchall() #selecciona todos los datos (fetch all = buscar todo)
        conn.commit() 
        conn.close()
        return data

    def dropTable(self):
        conn = sqlite3.connect('Notas.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        cursor.execute(f"drop table descargas")
        conn.commit() 
        conn.close()
