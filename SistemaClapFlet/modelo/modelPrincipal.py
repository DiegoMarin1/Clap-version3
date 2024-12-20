class persona:
    #CONTRUCTOR
    def __init__(self, cedula, nombre, apellido, telefono, correo, ubicacion):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.ubicacion = ubicacion

class lider(persona):
    def __init__(self, cedula, nombre, apellido, telefono, correo, ubicacion, usuario, contrasena, nivel, status, pregunta, respuesta):
        super().__init__(cedula, nombre, apellido, telefono, correo, ubicacion)
        self.__usuario = usuario
        self.__contrasena = contrasena
        self.__nivel = nivel
        self.__status = status
        self.pregunta = pregunta
        self.respuesta = respuesta

    def seccionUsuario(self, usuario, contrasena, status):
        self.__usuario = usuario
        self.__contrasena = contrasena
        self.__status = status
    
    def seccionPregunta(self, respuesta, pregunta):
        self.respuesta = respuesta
        self.pregunta = pregunta

    def set_contrasena(self, contrasena):
        self.__contrasena = contrasena

    def set_status(self, status):
        self.__status = status
    
    def get_nivel(self):
        return self.__nivel
    
    def get_usuario(self):
        return self.__usuario
    
    def get_contrasena(self):
        return self.__contrasena
    
class jefeFamiliar(persona):
    def __init__(self, cedula, nombre, apellido, telefono, correo, ubicacion, liderId, estatus):
        super().__init__(cedula, nombre, apellido, telefono, correo, ubicacion)
        self.__liderId = liderId
        self.__estatus = estatus
    
    def get_liderId(self):
        return self.__liderId
    
    def set_estatus(self, estatus):
        self.__estatus = estatus

class cilindro:
    def __init__(self, empresa, tamano, pico, precio):
        self.empresa = empresa
        self.tamano = tamano
        self.pico = pico
        self.precio = precio