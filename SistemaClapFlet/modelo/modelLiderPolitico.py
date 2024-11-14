class UsuarioSistema:
    #CONTRUCTOR
    def __init__(self, nombre, apellido, cedula,  ubicacion, pregunta, respuesta, usuario, contrasena, telefono, correo,):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.ubicacion = ubicacion
        self.pregunta = pregunta
        self.respuesta = respuesta
        self.usuario = usuario
        self.contrasena = contrasena
        self.telefono = telefono
        self.correo = correo

    #RETORNAR DATOS
    def datos(self):
        return self.nombre, self.apellido, self.cedula, self.ubicacion, self.pregunta, self.respuesta, self.usuario, self.contrasena, self.telefono, self.correo