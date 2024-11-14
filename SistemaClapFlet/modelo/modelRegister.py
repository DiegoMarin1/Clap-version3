class Usuario:
    #CONTRUCTOR
    def __init__(self, user, contra, nivel, estatus):
        self.user = user
        self.contra = contra
        self.nivel = nivel
        self.estatus = estatus

    #RETORNAR DATOS
    def datos(self):
        return self.user, self.contra, self.nivel, self.estatus

class Lideres:
    #CONTRUCTOR
    def __init__(self, nombre, apellido, cedula, telefono, correo, ubicacion, nivelUser):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.telefono = telefono
        self.correo = correo
        self.ubicacion = ubicacion
        self.nivelUser = nivelUser

    #RETORNAR DATOS
    def datos(self):
        return self.nombre, self.apellido, self.cedula, self.telefono,self.correo, self.ubicacion, self.nivelUser

class Respuesta:
    #CONTRUCTOR
    def __init__(self, respuesta, pregunta):
        self.respuesta = respuesta
        self.pregunta = pregunta

    #RETORNAR DATOS
    def datos(self):
        return self.respuesta, self.pregunta