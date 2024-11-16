from flet import SnackBar, Text, AlertDialog, dropdown
from controlador.conexion import db
from controlador.mensajes import mensaje
from modelo.consultas import consulta
from controlador.rutas import rutas

class gestionRecuperar:
    #VALIDA LA SECCION 1 DE LA SECCION RECUPERAR DONDE SE PIDE LA CEDULA
    def formulario1(page, tipoCedula, cedula, widgetPregunta, formulario, contenedor1, contenedor2):
        arregloCedula = f"{tipoCedula.value}-{cedula.value}"
        
        pregunta = db.consultaConRetorno(consulta.verificarCedulaRecuperar, [arregloCedula,])

        if (cedula.value == "") or (len(cedula.value) in range (1,7)):
            if cedula.value == "":
                cedula.error_text = mensaje.campoFaltante
                page.update()
            
            elif len(cedula.value) in range (1,7):
                cedula.error_text = mensaje.minimoCaracteres(7)
                page.update()

        elif pregunta:
            gestionRecuperar.mostrarPregunta(page, widgetPregunta, pregunta)
            rutas.animar(formulario, contenedor1, contenedor2, page)

        else:
            page.snack_bar = SnackBar(content=Text("La cedula no coincide con ningun usuario registrado"))
            page.snack_bar.open = True
            page.update()

    #VALIDA LA SECCION 2 DE LA SECCION RECUPERAR DONDE SE PIDE LA RESPUESTA
    def formulario2(page, tipoCedula, cedula, respuesta, formulario, contenedor1, contenedor2):
        arregloCedulaa = f"{tipoCedula.value}-{cedula.value}"
        resultadoRespuesta =  db.consultaConRetorno(consulta.verificarRespuesta, [arregloCedulaa,])

        if respuesta.value == "":
            respuesta.error_text = mensaje.campoFaltante
            page.update()

        elif resultadoRespuesta[0][0] == respuesta.value:
            rutas.animar(formulario, contenedor1, contenedor2, page)

        else:
            page.snack_bar = SnackBar(content=Text("Su respuesta es incorrecta"))
            page.snack_bar.open = True
            page.update()

    #VALIDA LA SECCION 3 DE LA SECCION RECUPERAR DONDE SE VALIDA LA NUEVA CONTRASENA
    def formulario3(page, tipoCedula, cedula, contrasena, confirmar):
        textGuardar = AlertDialog(title=Text("Contraseña cambiada correctamente"))

        arregloCedula = f"{tipoCedula.value}-{cedula.value}"

        if (contrasena.value == "") or (confirmar.value == "") or (len(contrasena.value) in range (1,6)):
            if contrasena.value == "":
                contrasena.error_text = mensaje.campoFaltante
                page.update()

            if confirmar.value == "":
                confirmar.error_text = mensaje.campoFaltante
                page.update()

            if len(contrasena.value) in range (1,6):
                contrasena.error_text = mensaje.minimoCaracteres(6)
                page.update()
            
            else:
                return

        elif contrasena.value == confirmar.value:
            idUsuario = db.consultaConRetorno(consulta.obtenerIdCedulaRecuperar, [arregloCedula,])
            
            db.consultaSinRetorno(consulta.guardarCambiosContrasena, [contrasena.value, idUsuario[0][0]])

            rutas.enrutamiento(page, rutas.routeLogin)

            page.dialog = textGuardar
            textGuardar.open = True
            page.update()


        else:
            page.snack_bar = SnackBar(content=Text("Las contraseñas no coinciden"))
            page.snack_bar.open = True
            page.update()

    #PARA MOSTRAR LA PREGUNTA DEL USUARIO EN LA BD
    def mostrarPregunta(page, widgetPregunta, pregunta):
        widgetPregunta.value = f"{pregunta[0][0]}"

        page.update()

    #VOLVER ATRAS
    def regresarF1(page,formulario, contenedor1, contenedor2):
        rutas.animar(formulario, contenedor1, contenedor2, page)

    def regresarF2(page,formulario, contenedor1, contenedor2):
        rutas.animar(formulario, contenedor1, contenedor2, page)