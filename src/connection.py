import mysql.connector as mysql

# Establecer la conexión con la base de datos
def connect_to_database():
    try:
        connection = mysql.connect(
            host="localhost",
            user="root",
            password="password1234",
            database="dataset",
            port="3306"
        )
        print("Conexión exitosa a la base de datos")
        return connection
    except mysql.Error as error:
        print("Error al conectar a la base de datos:", error)

# Ejemplo de uso
connection = connect_to_database()

# Cerrar la conexión
#if connection.is_connected():
#    connection.close()
#    print("Conexión cerrada")