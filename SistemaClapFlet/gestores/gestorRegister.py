from flet import SnackBar, Text, AlertDialog, dropdown
from controlador.conexion import db
from controlador.mensajes import mensaje
from controlador.rutas import rutas
from modelo.modelRegister import Usuario, Lideres, Respuesta

class gestionRegister:
    #VALIDA LA 1 SECCION DEL FORMULARIO EN EL QUE PIDE LOS DATOS PERSONALES
    def formulario1(page, nombre, apellido, cedula, numTelefono, correo, ubicacion, nivelUser, tipoCorreo, codigoTelefono, tipoCedula, formulario, contenedor1, contenedor2):
        #ARREGLOS
        arregloCedula = f"{tipoCedula.value}-{cedula.value}"
        arregloCorreo = f"{correo.value}{tipoCorreo.value}"
        arregloTelefono = f"{codigoTelefono.value}-{numTelefono.value}"
        global nuevoLider

        if (nombre.value == "") or (apellido.value == "") or (cedula.value == "") or (numTelefono.value == "") or (correo.value == "") or (ubicacion.value == "") or (nivelUser.value == None) or (tipoCorreo.value == None) or (codigoTelefono.value == None) or (len(nombre.value) in range(1, 3)) or (len(apellido.value) in range(1, 4)) or (len(cedula.value) in range(1, 7)) or (len(numTelefono.value) in range(1, 7)) or (len(ubicacion.value) in range(1, 3)):
            #VALIDA TODOS LOS CAMPOS VACIOS, MEJORA IMPLEMENTADA
            for control in (nombre, apellido, cedula, numTelefono, correo, ubicacion):
                if not control.value:
                    control.error_text = mensaje.campoFaltante
                    page.update()

            if len(nombre.value) in range(1, 3):
                nombre.error_text = "Minimo de caracteres 3"
                page.update()

            if len(apellido.value) in range(1, 4):
                apellido.error_text = "Minimo de caracteres 4"
                page.update()
            
            if len(cedula.value) in range(1, 7):
                cedula.error_text = "Minimo de caracteres 7"
                page.update()
            
            if len(numTelefono.value) in range(1, 7):
                numTelefono.error_text = "Numero de telefono no valido"
                page.update()

            if len(ubicacion.value) in range(1, 3):
                ubicacion.error_text = "Minimo de caracteres 3"
                page.update()
            
        elif db.verificarUbicacion(ubicacion.value):
            page.snack_bar = SnackBar(content=Text("Esta ubicacion ya esta en uso"))
            page.snack_bar.open = True
            page.update()

        elif db.verificarCedula(arregloCedula):
            page.snack_bar = SnackBar(content=Text("Esta cedula ya esta ligada a un usuario"))
            page.snack_bar.open = True
            page.update()

        elif db.verificarTelefono(arregloTelefono):
            page.snack_bar = SnackBar(content=Text("Este numero de telefono ya esta asignado a un usuario"))
            page.snack_bar.open = True
            page.update()

        elif db.verificarCorreo(arregloCorreo):
            page.snack_bar = SnackBar(content=Text("Este correo ya esta en uso"))
            page.snack_bar.open = True
            page.update()

        else:
            nuevoLider = Lideres(nombre.value, apellido.value, arregloCedula, arregloTelefono, arregloCorreo, ubicacion.value, nivelUser.value)
            rutas.animar(formulario, contenedor1, contenedor2, page)

    #VALIDA LA 2 SECCION DEL FORMULARIO LA CUAL PIDE LA CONTRASENA Y EL USUARIO
    def formulario2(page, usuario, contrasena, confirmarContrasena, formulario, contenedor1, contenedor2, nivelUser):
        global nuevoUsuario
        if (usuario.value == "") or (contrasena.value == "") or (confirmarContrasena.value == "") or (len(usuario.value) in range(1, 5)) or (len(contrasena.value) in range(1, 6)):

            for control in (usuario, contrasena, confirmarContrasena):
                if not control.value:
                    control.error_text = mensaje.campoFaltante
                    page.update()
            
            if len(usuario.value) in range(1, 5):
                usuario.error_text = "Minimo de caracteres 5"
                page.update()

            if len(contrasena.value) in range(1, 6):
                contrasena.error_text = "Minimo de caracteres 6"
                page.update()
        
        elif db.verificarNombreUsuario(usuario.value):
            page.snack_bar = SnackBar(content=Text("Nombre de Usuario ya existente"))
            page.snack_bar.open = True
            page.update()

        elif contrasena.value == confirmarContrasena.value:
            nuevoUsuario = Usuario(usuario.value, contrasena.value, nivelUser.value, 1)
            rutas.animar(formulario, contenedor1, contenedor2, page)

        else:    
            page.snack_bar = SnackBar(content=Text("La contraseña no coinciden"))
            page.snack_bar.open = True
            page.update()

    #VALIDA LA ULTIMA SECCION DEL FORMULARIO EN LA CUAL VALIDA EL METODO DE SEGURIDAD
    def formulario3(page, pregunta, respuesta):
        global nuevaRespuesta
        textGuardar = AlertDialog(title=Text("Usuario registrado correctamente"))

        if (pregunta.value == None) or (respuesta.value == "") or (len(respuesta.value) in range (1, 3)):          
            if respuesta.value == "":
                respuesta.error_text = mensaje.campoFaltante
                page.update()

            if pregunta.value == None:
                pregunta.error_text = mensaje.campoFaltante
                page.update()

            if len(respuesta.value) in range (1, 3):
                respuesta.error_text = "Minimo de caracteres 3"
                page.update()

            else:
                return

        else:
            nuevaRespuesta = Respuesta(respuesta.value, pregunta.value)
            gestionRegister.guardarUsuario(page, textGuardar)
            
    def guardarUsuario(page, mensaje):
        nivelUsuario = 2
        #OBTENER ID PREGUNTA
        idPregunta = db.obtenerIdPregunta(nuevaRespuesta.datos()[1])

        #GUARDAR LA RESPUESTA
        db.guardarRespuesta(nuevaRespuesta.datos()[0], idPregunta[0][0])

        #OBTENER ID RESPUESTA
        idRespuesta = db.obtenerIdRespuesta(idPregunta[0][0], nuevaRespuesta.datos()[0])

        #GUARDAR DATOS DEL LIDER
        db.guardarLider(nuevoLider.datos()[0], nuevoLider.datos()[1], nuevoLider.datos()[2], nuevoLider.datos()[3], nuevoLider.datos()[4], nuevoLider.datos()[5])

        #OBTENER ID LIDER
        idLider = db.obtenerIdLider(nuevoLider.datos()[2])

        #SACAR DATO NIVEL USUARIO
        if nuevoUsuario.datos()[2] == "Lider Politico":
            nivelUsuario = 1

        #INSERTAR DATOS USUARIO
        db.guardarUsuario(nuevoUsuario.datos()[0], nuevoUsuario.datos()[1], idRespuesta[0][0], idLider[0][0], nivelUsuario)

        rutas.enrutamiento(page, rutas.routeLogin)

        page.dialog = mensaje
        mensaje.open = True
        page.update()

    def regresarF1(page,formulario, contenedor1, contenedor2):
        rutas.animar(formulario, contenedor1, contenedor2, page)

    def regresarF2(page,formulario, contenedor1, contenedor2):
        rutas.animar(formulario, contenedor1, contenedor2, page)

    def llenarPreguntas(widget):
        resultadoPreguntas = db.llenarPreguntas()
        for mostrarPreguntas in resultadoPreguntas:
            widget.options.append(dropdown.Option(mostrarPreguntas[0]))