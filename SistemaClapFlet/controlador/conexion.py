import sqlite3
from modelo.consultas import consulta
import pathlib

class db:
    def conectar():
        try:
            rutaActual = pathlib.Path(__file__).parent.absolute()
            dbname = rutaBD = rf"{rutaActual}\dbclap.db"
            miConexion = sqlite3.connect(dbname)
            cursor = miConexion.cursor()
            return miConexion, cursor
        except:
            print("Ocurrio un error en la conexion con la base de datos")

    def consultaConRetorno(query, parametros=()):
        miConexion, cursor = db.conectar()
        cursor.execute(query, parametros)
        miConexion.commit()
        return cursor.fetchall()
    
    def consultaSinRetorno(query, parametros=()):
        miConexion, cursor = db.conectar()
        cursor.execute(query, parametros)
        miConexion.commit()