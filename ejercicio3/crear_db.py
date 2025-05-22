import sqlite3

def crear_db():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute("INSERT OR IGNORE INTO usuarios VALUES (?, ?)", ("admin", "1234"))

    conexion.commit()
    conexion.close()
    print("Base de datos creada con éxito.")

if __name__ == "__main__":
    crear_db()
