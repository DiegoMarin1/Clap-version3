class jefeFamilia:
    #CONTRUCTOR
    def __init__(self, cedula, nombre, apellido, telefono, correo, ubicacion):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.ubicacion = ubicacion

    #RETORNAR DATOS
    def datos(self):
        return self.cedula, self.nombre, self.apellido, self.telefono, self.correo, self.ubicacion

class liderCalle:
    #CONTRUCTOR
    def __init__(self, cedula, nombre, apellido, telefono, correo, ubicacion):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.telefono = telefono
        self.correo = correo
        self.ubicacion = ubicacion

    #RETORNAR DATOS
    def datos(self):
        return self.cedula, self.nombre, self.apellido, self.telefono, self.correo, self.ubicacion