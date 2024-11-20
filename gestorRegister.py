from flet import SnackBar, Text, AlertDialog, dropdown
from controlador.conexion import db
from controlador.mensajes import mensaje, validaciones
from controlador.rutas import rutas
from modelo.consultas import consulta
from modelo.modelPrincipal import lider


class gestionRegister:
    #VALIDA LA 1 SECCION DEL FORMULARIO EN EL QUE PIDE LOS DATOS PERSONALES
    def formulario1(page, nombre, apellido, cedula, numTelefono, correo, ubicacion, nivelUser, tipoCorreo, codigoTelefono, tipoCedula, formulario, contenedor1, contenedor2, encabezado):
        global nuevoUsuario

        listaCondicion = {
            "nombre" : {"min":3},
            "apellido" : {"min":4},
            "cedula" : {"min":7, "query":consulta.verficarCedula, "param":[f"{tipoCedula.value}-{cedula.value}",], "msj":"Esta cedula ya esta ligada a un usuario"},
            "numTelefono" : {"min":7, "query":consulta.verficarNumero, "param":[f"{codigoTelefono.value}-{numTelefono.value}",], "msj":"Este numero de telefono ya esta asignado a un usuario"},
            "correo" : {"min":3, "query":consulta.verificarCorreo, "param":[f"{correo.value}{tipoCorreo.value}",], "msj":"Este correo ya esta en uso"},
            "ubicacion" : {"min":3, "query":consulta.verficarUbicacion, "param":[ubicacion.value,], "msj":"Esta ubicacion ya esta en uso"},
            "nivelUser" : {"min":4},
            "tipoCorreo" : {"min":4},
            "codigoTelefono" : {"min":4}
        }
        todoValido = True

        for nombreCampo, config in listaCondicion.items():
            if not (eval(nombreCampo).value) or (len(eval(nombreCampo).value) < config["min"]):
                validaciones.validarCampos(page, eval(nombreCampo), config["min"])
                todoValido = False
            if "query" in config:
                if bool(validaciones.validarConsultas(page, config["query"], config["param"], config["msj"]) == False):
                    todoValido = False

        if todoValido:
            nuevoUsuario = lider(f"{tipoCedula.value}-{cedula.value}", nombre.value, apellido.value, f"{codigoTelefono.value}-{numTelefono.value}", f"{correo.value}{tipoCorreo.value}", ubicacion.value, True, True, nivelUser.value, True, True, True)
            encabezado.cambiarColor(encabezado.punto2, encabezado.punto1, encabezado.punto3)
            rutas.animar(formulario, contenedor1, contenedor2, page)


    #VALIDA LA 2 SECCION DEL FORMULARIO LA CUAL PIDE LA CONTRASENA Y EL USUARIO
    def formulario2(page, usuario, contrasena, confirmarContrasena, formulario, contenedor1, contenedor2, encabezado):
        
        listaCondicion = {
            "usuario" : {"min":5, "query":consulta.verificarNombreUsuario, "param":[usuario.value,], "msj":"Nombre de Usuario ya existente"},
            "contrasena" : {"min":6},
            "confirmarContrasena" : {"min":6}
        }
        todoValido = True

        for nombreCampo, config in listaCondicion.items():
            if not (eval(nombreCampo).value) or (len(eval(nombreCampo).value) < config["min"]):
                validaciones.validarCampos(page, eval(nombreCampo), config["min"])
                todoValido = False
            if "query" in config:
                if bool(validaciones.validarConsultas(page, config["query"], config["param"], config["msj"]) == False):
                    todoValido = False

        if todoValido:
            if contrasena.value == confirmarContrasena.value:
                nuevoUsuario.seccionUsuario(usuario.value, contrasena.value, 1)
                encabezado.cambiarColor(encabezado.punto3, encabezado.punto1, encabezado.punto2)
                rutas.animar(formulario, contenedor1, contenedor2, page)

            else:    
                page.snack_bar = SnackBar(content=Text("La contraseña no coinciden"))
                page.snack_bar.open = True
                page.update()

    #VALIDA LA ULTIMA SECCION DEL FORMULARIO EN LA CUAL VALIDA EL METODO DE SEGURIDAD
    def formulario3(page, pregunta, respuesta):
        textGuardar = AlertDialog(title=Text("Usuario registrado correctamente"))

        listaCondicion = {
            "pregunta" : {"min":1},
            "respuesta" : {"min":3},
        }
        todoValido = True

        for nombreCampo, config in listaCondicion.items():
            if not (eval(nombreCampo).value) or (len(eval(nombreCampo).value) < config["min"]):
                validaciones.validarCampos(page, eval(nombreCampo), config["min"])
                todoValido = False
            if "query" in config:
                if bool(validaciones.validarConsultas(page, config["query"], config["param"], config["msj"]) == False):
                    todoValido = False

        if todoValido:
            nuevoUsuario.seccionPregunta(respuesta.value, pregunta.value)
            gestionRegister.guardarUsuario(page, textGuardar)

    def guardarUsuario(page, mensaje):
        nivelUsuario = 2
        #OBTENER ID PREGUNTA
        idPregunta = db.consultaConRetorno(consulta.obtenerIdPregunta, [nuevoUsuario.pregunta,])

        #GUARDAR LA RESPUESTA
        db.consultaSinRetorno(consulta.guardarRespuesta, [nuevoUsuario.respuesta, idPregunta[0][0]])

        #OBTENER ID RESPUESTA
        idRespuesta = db.consultaConRetorno(consulta.obtenerIdRespuesta, [idPregunta[0][0], nuevoUsuario.respuesta])

        #GUARDAR DATOS DEL LIDER
        db.consultaSinRetorno(consulta.guardarLider, [nuevoUsuario.nombre, nuevoUsuario.apellido, nuevoUsuario.cedula, nuevoUsuario.telefono, nuevoUsuario.correo, nuevoUsuario.ubicacion])

        #OBTENER ID LIDER
        idLider = db.consultaConRetorno(consulta.obtenerIdLider, [nuevoUsuario.cedula])

        #SACAR DATO NIVEL USUARIO
        if nuevoUsuario.get_nivel() == "Lider Politico":
            nivelUsuario = 1

        #INSERTAR DATOS USUARIO
        db.consultaSinRetorno(consulta.guardarUsuario, [nuevoUsuario.get_usuario(), nuevoUsuario.get_contrasena(), idRespuesta[0][0], idLider[0][0], nivelUsuario])

        rutas.enrutamiento(page, rutas.routeLogin)

        page.dialog = mensaje
        mensaje.open = True
        page.update()

    def regresarF1(page,formulario, contenedor1, contenedor2):
        rutas.animar(formulario, contenedor1, contenedor2, page)

    def regresarF2(page,formulario, contenedor1, contenedor2):
        rutas.animar(formulario, contenedor1, contenedor2, page)

    def llenarPreguntas(widget):
        resultadoPreguntas = db.consultaConRetorno(consulta.llenarPreguntas)
        for mostrarPreguntas in resultadoPreguntas:
            widget.options.append(dropdown.Option(mostrarPreguntas[0]))