from flet import ScrollMode, Container, Text, SnackBar, Dropdown, dropdown, alignment, border_radius, border, TextCapitalization, TextField, CrossAxisAlignment, MainAxisAlignment, Column, FontWeight, TextButton, AlertDialog, padding, TextThemeStyle, DataRow, DataCell, Row, icons, IconButton, ElevatedButton
from controlador.conexion import db
from controlador.rutas import rutas
from controlador.mensajes import mensaje, validaciones
from modelo.modelPrincipal import lider, jefeFamiliar
from modelo.consultas import consulta
from modelo.modelVista import seccionesEditar, seccionesEditarCompleja

import modelo.reporte
from modelo.reporte import *
from modelo.modelPrincipal import lider

import os
import pathlib
import shutil

from datetime import datetime
from time import sleep

#USADA PARA OBTNER LOS ELEMENTOS QUE NECESITAN LAS OTRAS CLASES
class gestionPrincipal:

    cartas = []
    contenido = []
    bitacoraLista = []
    his = []

    formulario = None
    nombre = None
    apellido = None
    cedula = None
    estatus = None
    contrasena = None 
    usuario = None
    pregunta = None
    respuesta = None
    ubicacion = None
    telefono = None
    correo = None
    columnaCards = None

    contenedorInicio = None
    contenedorHistorial = None
    formularioBitacora = None
    formularioLiderCalle = None 
    contenedorBombonas = None
    formularioBitacora = None
    contenedorPerfil = None
    listaBitacora = None
    nombreLi = None
    apellidoLi = None
    cedulaLi = None
    ubicacionLi = None
    telefonoLi = None
    correoLi = None
    preguntaP = None
    respuestaP = None
    usuarioP = None
    contrasenaP = None
    tablaLlenarHistorial = None
    tablaSeleccionarHistorial = None

    check = None
    btnCandado = None
    btnCandadoP = None
    appbar = None


    def obtenerWidget(formulario, nombre, apellido, cedula, estatus, contrasena, usuario, pregunta, respuesta, ubicacion, telefono, correo, 
    columnaCards, contenedorInicio, contenedorHistorial ,formularioBitacora, formularioLiderCalle, 
    contenedorBombonas, contenedorPerfil, listaBitacora, nombreLi, apellidoLi, cedulaLi, ubicacionLi, telefonoLi, correoLi, 
    preguntaP, respuestaP, usuarioP, contrasenaP, tablaLlenarHistorial, tablaSeleccionarHistorial, check, btnCandado, btnCandadoP, appbar):

        gestionPrincipal.formulario = formulario
        gestionPrincipal.nombre = nombre
        gestionPrincipal.apellido = apellido
        gestionPrincipal.cedula = cedula
        gestionPrincipal.estatus = estatus
        gestionPrincipal.contrasena = contrasena
        gestionPrincipal.usuario = usuario
        gestionPrincipal.pregunta = pregunta
        gestionPrincipal.respuesta = respuesta
        gestionPrincipal.ubicacion = ubicacion
        gestionPrincipal.telefono = telefono
        gestionPrincipal.correo = correo
        gestionPrincipal.columnaCards = columnaCards

        gestionPrincipal.contenedorInicio = contenedorInicio
        gestionPrincipal.contenedorHistorial = contenedorHistorial
        gestionPrincipal.formularioBitacora = formularioBitacora
        gestionPrincipal.formularioLiderCalle = formularioLiderCalle
        gestionPrincipal.contenedorBombonas = contenedorBombonas
        gestionPrincipal.formularioBitacora = formularioBitacora
        gestionPrincipal.contenedorPerfil = contenedorPerfil
        gestionPrincipal.listaBitacora = listaBitacora
        gestionPrincipal.nombreLi = nombreLi
        gestionPrincipal.apellidoLi = apellidoLi
        gestionPrincipal.cedulaLi = cedulaLi
        gestionPrincipal.ubicacionLi = ubicacionLi
        gestionPrincipal.telefonoLi = telefonoLi
        gestionPrincipal.correoLi = correoLi
        gestionPrincipal.preguntaP = preguntaP
        gestionPrincipal.respuestaP = respuestaP
        gestionPrincipal.usuarioP = usuarioP
        gestionPrincipal.contrasenaP = contrasenaP
        gestionPrincipal.tablaLlenarHistorial = tablaLlenarHistorial
        gestionPrincipal.tablaSeleccionarHistorial = tablaSeleccionarHistorial
        gestionPrincipal.check = check
        gestionPrincipal.btnCandado = btnCandado
        gestionPrincipal.btnCandadoP = btnCandadoP
        gestionPrincipal.appbar = appbar

#GENERA LAS FICHAS DE LOS JEFES DE FAMILIA MOSTRADOS EN LA VIEW
class generarCartas:
    #LIMPIA EL CONTEDOR DE LAS CARTAS
    def volverGenerarCartas(page):
        gestionPrincipal.cartas.clear()
        gestionPrincipal.columnaCards.controls.clear()
        gestionPrincipal.columnaCards.controls = generarCartas.generarCards(page)

        page.update()

    def generarCards(page):
        resultado = db.consultaConRetorno(consulta.obtenerTodosUsuarios)

        for nom, ape, ci, ids in resultado:
            gestionPrincipal.cartas.append(
                Container(
                    bgcolor="RED",
                    height=150,
                    width=250,
                    padding=padding.all(7),
                    border_radius=border_radius.all(20),
                    on_click=lambda _, ids=ids, nom=nom: [formularioUsuarioLiderCalle.generarJefe(ids, page), rutas.animar(gestionPrincipal.formulario, gestionPrincipal.formularioLiderCalle, gestionPrincipal.formularioLiderCalle, page)],
                    content=Column(
                        controls=[
                            Text(f"{nom} {ape}", style=TextThemeStyle.TITLE_LARGE, color="WHITE"),
                            Text(f"{ci}", style=TextThemeStyle.TITLE_MEDIUM, color="WHITE"),
                        ]
                    )
                )
            )
            page.update()

        return gestionPrincipal.cartas

#PARA CARGAR LOS DATOS DEL USUARIO QUE INCIO SECCION
class formularioUsuarioLiderCalle:
    def generarJefe(ids, page):
        
        resultadoUsuario = db.consultaConRetorno(consulta.obtenerDatosUsuarioLideresCalle, [ids,])
        datosUsuarioLiderCalle = lider(resultadoUsuario[0][2], resultadoUsuario[0][0], resultadoUsuario[0][1], resultadoUsuario[0][8], resultadoUsuario[0][9], resultadoUsuario[0][3], resultadoUsuario[0][6], resultadoUsuario[0][7], resultadoUsuario[0][10], resultadoUsuario[0][9], resultadoUsuario[0][4], resultadoUsuario[0][5])

        gestionPrincipal.nombre.value = f"{datosUsuarioLiderCalle.nombre}"
        gestionPrincipal.apellido.value = f"{datosUsuarioLiderCalle.apellido}"
        gestionPrincipal.cedula.value = f"{datosUsuarioLiderCalle.cedula}"
        gestionPrincipal.ubicacion.value = f"{datosUsuarioLiderCalle.ubicacion}"
        gestionPrincipal.pregunta.value = f"{datosUsuarioLiderCalle.pregunta}"
        gestionPrincipal.respuesta.value = f"{datosUsuarioLiderCalle.respuesta}"
        gestionPrincipal.usuario.value = f"{datosUsuarioLiderCalle.get_usuario()}"
        gestionPrincipal.contrasena.value = f"{datosUsuarioLiderCalle.get_contrasena()}"
        gestionPrincipal.telefono.value = f"{datosUsuarioLiderCalle.telefono}"
        gestionPrincipal.correo.value = f"{datosUsuarioLiderCalle.correo}"

        rutas.animar(gestionPrincipal.formulario, gestionPrincipal.formularioLiderCalle, gestionPrincipal.formularioLiderCalle, page)
        
        if resultadoUsuario[0][10] == 1:
            gestionPrincipal.estatus.value = "Habilitado"
            gestionPrincipal.check.value = False
        else:
            gestionPrincipal.estatus.value = "inhabilitado"
            gestionPrincipal.check.value = True

        page.update()

class revelarContrasena:
    def regresarPassFalse(page, widget):

        if widget.visible == True:
            widget.visible = False
            gestionPrincipal.btnCandado.icon = icons.LOCK_OUTLINE
            page.update()
        else:
            pass

    def revelarPass(page, widget):

        if widget.visible == False:
            gestionPrincipal.btnCandado.icon = icons.LOCK_OPEN
            widget.visible = True
            page.update()
        else:
            gestionPrincipal.btnCandado.icon = icons.LOCK_OUTLINE
            widget.visible = False
            page.update()

class bloqueoUsuario:
    def estatusUsuario(page):

        if gestionPrincipal.estatus.value == "Habilitado":
            gestionPrincipal.check.value = True
            gestionPrincipal.estatus.value = "Inhabilitado"
            db.consultaSinRetorno(consulta.actualizarEstatusUsuario, [2, gestionPrincipal.usuario.value])
        else:
            gestionPrincipal.check.value = False
            gestionPrincipal.estatus.value = "Habilitado"
            db.consultaSinRetorno(consulta.actualizarEstatusUsuario, [1, gestionPrincipal.usuario.value])

        page.update()

class bitacora:
    def volverGenerarBitacora(page, ci):
        resultadoBitacora = db.consultaConRetorno(consulta.extraerBitacora, [ci.value,])

        for entrada, salida in resultadoBitacora:
            gestionPrincipal.listaBitacora.controls.append(Text(f"Entrada: {entrada}     Salida : {salida}"))
            page.update()

    def regresarViewFalse(page):
        gestionPrincipal.listaBitacora.controls.clear()
        page.update()

        if gestionPrincipal.contrasena.visible == True:
            gestionPrincipal.contrasena.visible = False
            gestionPrincipal.btnCandado.icon = icons.LOCK_OUTLINE
            page.update()
        else:
            pass

class preciosCilindros:
    def menuPrecios(page):

        PrecioPequeña = TextField(label="Pequeña", hint_text="Ingresar precio", border_radius=30, border_color="#820000", width=150, height=60, on_change=lambda _:[mensaje.quitarError(page, PrecioPequeña), validaciones.validarCamposNot(PrecioPequeña, page, True, validaciones.condicionNumeros)])
        PrecioMediana = TextField(label="Mediana", hint_text="Ingresar precio", border_radius=30, border_color="#820000", width=150, height=60, on_change=lambda _:[mensaje.quitarError(page, PrecioMediana), validaciones.validarCamposNot(PrecioMediana, page, True, validaciones.condicionNumeros)])
        PrecioRegular = TextField(label="Regular", hint_text="Ingresar precio", border_radius=30, border_color="#820000", width=150, height=60, on_change=lambda _:[mensaje.quitarError(page, PrecioRegular), validaciones.validarCamposNot(PrecioRegular, page, True, validaciones.condicionNumeros)])
        PrecioGrande = TextField(label="Grande", hint_text="Ingresar precio", border_radius=30, border_color="#820000", width=150, height=60, on_change=lambda _:[mensaje.quitarError(page, PrecioGrande), validaciones.validarCamposNot(PrecioGrande, page, True, validaciones.condicionNumeros)])

        alertJornada = AlertDialog(
            modal=True,
            content=Column(
            height=400,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Text("Ingrese los nuevos precios de los cilindros en los siguientes campos"),
                Column(
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        PrecioPequeña,
                        PrecioMediana,
                        PrecioRegular,
                        PrecioGrande
                    ]
                )
            ]
            ),
            actions=[TextButton("Guardar", on_click=lambda _: preciosCilindros.validarPrecios(page, alertJornada, PrecioPequeña, PrecioMediana, PrecioRegular, PrecioGrande)), TextButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(page, alertJornada))]
            )

        page.dialog = alertJornada
        alertJornada.open = True

        page.update()

    def validarPrecios(page, alertJornada, PrecioPequeña, PrecioMediana, PrecioRegular, PrecioGrande):

        if (PrecioPequeña.value == "") or (PrecioMediana.value == "") or (PrecioRegular.value == "") or (PrecioGrande.value == ""):
            for control in (PrecioPequeña, PrecioMediana, PrecioRegular, PrecioGrande):
                if not control.value:
                    control.error_text = mensaje.campoFaltante
                    page.update()
            else:
                return
        else:
            contador = 0
            for precio in (PrecioPequeña, PrecioMediana, PrecioRegular, PrecioGrande):
                contador = contador + 1
                db.consultaSinRetorno(consulta.actualizarPrecios, [precio.value, contador])

            mensaje.cerrarAlert(page, alertJornada)
            page.snack_bar = SnackBar(content=Text("Precios Actualizados Correctamente"), bgcolor="GREEN")
            page.snack_bar.open = True
            page.update()

#PARA VER EL HISTORIAL DE JORNADAS QUE A REALIZADO UN USUARIO LIDER DE CALLE
class historial:
    #CARGAR LOS DATOS DE LAS JORNADAS
    def abrirHistorial(page, fechaa, idss):
        gestionPrincipal.tablaLlenarHistorial.rows.clear()
        gestionPrincipal.tablaLlenarHistorial.rows = historial.llenarHistroial(page, idss)

        alertHistorial = AlertDialog(
            modal=True,
            content=Column(
                controls=[
                    Text(f"Jornada realizada el {fechaa}"),
                    Container(
                        bgcolor="white",
                        height=550,
                        border_radius=border_radius.all(7),  
                        content=Column(
                            expand=True,
                            height=550,
                            scroll=ScrollMode.ALWAYS,
                            controls=[
                                gestionPrincipal.tablaLlenarHistorial,
                            ]
                        )
                    ),
                ]
            ),
            actions=[ElevatedButton("Descargar Pdf", on_click=lambda _:archivos.descargarArchivo(page, alertHistorial, idss)), ElevatedButton("Regresar", on_click=lambda _:mensaje.cerrarAlert(page, alertHistorial))]
        )

        page.dialog = alertHistorial
        alertHistorial.open = True

        page.update()

    #EXTRAER DE DATOS EL CONTENEDOR DEL HISTORIAL
    def llenarHistroial(page, ids):
        resultado = db.consultaConRetorno(consulta.obtenerHistorial, [ids,])

        for idss, cii, nom, ape, empresa, tamano, pico , fecha in resultado:
            gestionPrincipal.contenido.append(DataRow(
                color="WHITE",
                cells=[
                    DataCell(Text(f"{cii}")),
                    DataCell(Text(f"{nom}")),
                    DataCell(Text(f"{ape}")),
                    DataCell(Text(f"{empresa}")),
                    DataCell(Text(f"{tamano}")),
                    DataCell(Text(f"{pico}")),
                    DataCell(Text(f"{fecha}")),
                ],
            ),
            )

            page.update()

        return gestionPrincipal.contenido 

#GESTIONAR EL GUARDADO DE ARCHIVOS
class archivos:
    def volverGenerarArchivos(page, query, parametro, tabla, funcion):
        gestionPrincipal.bitacoraLista.clear()
        tabla.rows.clear()
        tabla.rows = archivos.generarArchivos(page, query, parametro, funcion)

        page.update()

    def generarArchivos(page, query, parametro, funcion):
        coun = 1
        resultadoId = db.consultaConRetorno(query, [parametro,])

        for idss in resultadoId:

            datos = db.consultaConRetorno(consulta.obtenerFechasJornadas, [idss[0],])

            gestionPrincipal.bitacoraLista.append([datos[0][0], datos[0][1]])

        for fecha, ids in gestionPrincipal.bitacoraLista:
            gestionPrincipal.his.append(DataRow(
                color="WHITE",
                cells=[
                    DataCell(Text(f"Jornada {coun}")),
                    DataCell(Text(f"{fecha}")),
                ],
                on_select_changed=lambda _, fecha = fecha, ids = ids: [funcion(page, fecha, ids)]
            ),
            )
            coun = coun + 1

            page.update()

        return gestionPrincipal.his

    def descargarArchivo(page, alertt, ids):

        origen = db.consultaConRetorno(consulta.origenRutaArchivo, [ids,])
        destino = os.path.join(os.path.join(os.environ['USERPROFILE']), rf'Desktop\Reportes')

        rutaEscritorio = os.path.join(os.path.join(os.environ['USERPROFILE']), rf'Desktop\Reportes')

        if os.path.exists(rutaEscritorio) == True:
            pass
        else:
            os.mkdir(rutaEscritorio)

        shutil.copy(origen[0][0], destino)

        mensaje.cerrarAlert(page, alertt)
        page.snack_bar = SnackBar(content=Text("El PDF se descargo correctamente, puede visualizarlo en la caperta Reportes ubicada en el escritorio"), bgcolor="GREEN")
        page.snack_bar.open = True
        page.update()

class datosUsuario:
    def volverCargarTusDatos(page):

        resultadoUsuario = db.consultaConRetorno(consulta.obtenerDatosLiderPolitico, [mensaje.datosUsuarioLista[0][0],])

        gestionPrincipal.nombreLi.value = f"{resultadoUsuario[0][0]}"
        gestionPrincipal.apellidoLi.value = f"{resultadoUsuario[0][1]}"
        gestionPrincipal.cedulaLi.value = f"{resultadoUsuario[0][2]}"
        gestionPrincipal.ubicacionLi.value = f"{resultadoUsuario[0][3]}"
        gestionPrincipal.preguntaP.value = f"{resultadoUsuario[0][4]}"
        gestionPrincipal.respuestaP.value = f"{resultadoUsuario[0][5]}"
        gestionPrincipal.usuarioP.value = f"{resultadoUsuario[0][6]}"
        gestionPrincipal.contrasenaP.value = f"{resultadoUsuario[0][7]}"
        gestionPrincipal.telefonoLi.value = f"{resultadoUsuario[0][8]}"
        gestionPrincipal.correoLi.value = f"{resultadoUsuario[0][9]}"

        page.update()