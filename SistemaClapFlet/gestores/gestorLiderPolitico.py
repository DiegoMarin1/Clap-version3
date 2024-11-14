from flet import ScrollMode, Container, Text, SnackBar, Dropdown, dropdown, alignment, border_radius, border, TextCapitalization, TextField, CrossAxisAlignment, MainAxisAlignment, Column, FontWeight, TextButton, AlertDialog, padding, TextThemeStyle, DataRow, DataCell, Row, icons, IconButton, ElevatedButton
from controlador.conexion import db
from controlador.rutas import rutas
from controlador.mensajes import mensaje
from modelo.modelPrincipal import *
import modelo.reporte
from modelo.reporte import *
from modelo.modelLiderPolitico import UsuarioSistema

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

    titulo = None
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
    textoSlider = None
    tablaLlenarHistorial = None
    tablaSeleccionarHistorial = None

    check = None
    btnCandado = None
    btnCandadoP = None

    entryEmpresa = None
    entryPico = None

    def obtenerWidget(formulario, nombre, apellido, cedula, estatus, contrasena, usuario, pregunta, respuesta, ubicacion, telefono, correo, 
    columnaCards, titulo, contenedorInicio, contenedorHistorial ,formularioBitacora, formularioLiderCalle, 
    contenedorBombonas, contenedorPerfil, listaBitacora, nombreLi, apellidoLi, cedulaLi, ubicacionLi, telefonoLi, correoLi, 
    preguntaP, respuestaP, usuarioP, contrasenaP, textoSlider, tablaLlenarHistorial, tablaSeleccionarHistorial, check, btnCandado, btnCandadoP, 
    entryEmpresa, entryPico):

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

        gestionPrincipal.titulo = titulo
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
        gestionPrincipal.textoSlider = textoSlider
        gestionPrincipal.tablaLlenarHistorial = tablaLlenarHistorial
        gestionPrincipal.tablaSeleccionarHistorial = tablaSeleccionarHistorial
        gestionPrincipal.check = check
        gestionPrincipal.btnCandado = btnCandado
        gestionPrincipal.btnCandadoP = btnCandadoP
        gestionPrincipal.entryEmpresa = entryEmpresa
        gestionPrincipal.entryPico = entryPico

    def volverLogin(page, indicator):
        gestionPrincipal.columnaCards.controls.clear()
        gestionPrincipal.tablaSeleccionarHistorial.rows.clear()
        mensaje.salir(page, indicator)

#GENERA LAS FICHAS DE LOS JEFES DE FAMILIA MOSTRADOS EN LA VIEW
class generarCartas:
    #LIMPIA EL CONTEDOR DE LAS CARTAS
    def volverGenerarCartas(page):
        gestionPrincipal.columnaCards.controls.clear()
        gestionPrincipal.columnaCards.controls = generarCartas.generarCards(page)

        page.update()

    def generarCards(page):
        resultado = db.obtenerTodosUsuarios()

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
        global datosUsuarioLiderCalle
        resultadoUsuario = db.obtenerDatosUsuarioLideresCalle(ids)
        datosUsuarioLiderCalle = UsuarioSistema(resultadoUsuario[0][0], resultadoUsuario[0][1], resultadoUsuario[0][2], resultadoUsuario[0][3], resultadoUsuario[0][4], resultadoUsuario[0][5], resultadoUsuario[0][6], resultadoUsuario[0][7], resultadoUsuario[0][8], resultadoUsuario[0][9])

        gestionPrincipal.nombre.value = f"{resultadoUsuario[0][0]}"
        gestionPrincipal.apellido.value = f"{resultadoUsuario[0][1]}"
        gestionPrincipal.cedula.value = f"{resultadoUsuario[0][2]}"
        gestionPrincipal.ubicacion.value = f"{resultadoUsuario[0][3]}"
        gestionPrincipal.pregunta.value = f"{resultadoUsuario[0][4]}"
        gestionPrincipal.respuesta.value = f"{resultadoUsuario[0][5]}"
        gestionPrincipal.usuario.value = f"{resultadoUsuario[0][6]}"
        gestionPrincipal.contrasena.value = f"{resultadoUsuario[0][7]}"
        gestionPrincipal.telefono.value = f"{resultadoUsuario[0][8]}"
        gestionPrincipal.correo.value = f"{resultadoUsuario[0][9]}"
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
            db.actualizarEstatusUsuario(2, gestionPrincipal.usuario.value)
        else:
            gestionPrincipal.check.value = False
            gestionPrincipal.estatus.value = "Habilitado"
            db.actualizarEstatusUsuario(1, gestionPrincipal.usuario.value)

        page.update()

#PARA AGREGAR NUEVAS EMPRESAS O TIPOS DE PICOS A LOS CILINDROS
class caracteristicasCilindro:
    def nuevaEmpresa(page):
        alertNuevaEmpresa = AlertDialog(
            content=Container(
                alignment=alignment.center,
                height=150,
                width=300,
                bgcolor="white",
                content=Column(
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        Text("Añade una nueva empresa"),
                        gestionPrincipal.entryEmpresa,
                    ]
                )
            ),
            actions=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        ElevatedButton("Guardar", on_click=lambda _:caracteristicasCilindro.ValidarEmpresa(page, alertNuevaEmpresa)),
                        ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(page, alertNuevaEmpresa))
                    ]
                )
            ]
        )

        page.dialog = alertNuevaEmpresa
        alertNuevaEmpresa.open = True

        page.update()
    
    def ValidarEmpresa(page, alertNuevaEmpresa):

        if (gestionPrincipal.entryEmpresa.value == "") or (len(gestionPrincipal.entryEmpresa.value) in range(1, 3)):
            if gestionPrincipal.entryEmpresa.value == "":
                gestionPrincipal.entryEmpresa.error_text = mensaje.campoFaltante
                page.update()
            if len(gestionPrincipal.entryEmpresa.value) in range(1, 3):
                gestionPrincipal.entryEmpresa.error_text = mensaje.minimoCaracteres(3)
                page.update()
        elif db.verificarEmpresa(gestionPrincipal.entryEmpresa.value):
            page.snack_bar = SnackBar(content=Text("Esta Empresa ya esta registrada"))
            page.snack_bar.open = True
            page.update()
        else:
            db.guardarEmpresaNueva(gestionPrincipal.entryEmpresa.value)
            mensaje.cerrarAlert(page, alertNuevaEmpresa)
            gestionPrincipal.entryEmpresa.value = ""
            page.snack_bar = SnackBar(bgcolor="GREEN", content=Text("La empresa se guardo correctamente"))
            page.snack_bar.open = True
            page.update()

    def nuevoPico(page):

        alertNuevaPico = AlertDialog(
            content=Container(
                alignment=alignment.center,
                height=150,
                width=300,
                bgcolor="white",
                content=Column(
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        Text("Añade un nuevo tipo de pico"),
                        gestionPrincipal.entryPico,
                    ]
                )
            ),
            actions=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        ElevatedButton("Guardar", on_click=lambda _:caracteristicasCilindro.ValidarPico(page, alertNuevaPico)),
                        ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(page, alertNuevaPico))
                    ]
                )
            ]
        )

        page.dialog = alertNuevaPico
        alertNuevaPico.open = True

        page.update()

    def ValidarPico(page, alertNuevaPico):

        if (gestionPrincipal.entryPico.value == "") or (len(gestionPrincipal.entryPico.value) in range(1, 3)):
            if gestionPrincipal.entryPico.value == "":
                gestionPrincipal.entryPico.error_text = mensaje.campoFaltante
                page.update()
            if len(gestionPrincipal.entryPico.value) in range(1, 3):
                gestionPrincipal.entryPico.error_text = mensaje.minimoCaracteres(3)
                page.update()
        elif db.verificarPico(gestionPrincipal.entryPico.value):
            page.snack_bar = SnackBar(content=Text("Esta Tamaño ya esta registrada"))
            page.snack_bar.open = True
            page.update()
        else:
            db.guardarPicoNuevo(gestionPrincipal.entryPico.value)
            mensaje.cerrarAlert(page, alertNuevaPico)
            gestionPrincipal.entryPico.value = ""
            page.snack_bar = SnackBar(bgcolor="GREEN", content=Text("El nuevo tipo de pico se guardo correctamente"))
            page.snack_bar.open = True
            page.update()

class bitacora:
    def volverGenerarBitacora(page, ci):
        resultadoBitacora = db.extraerBitacora(ci.value)

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

        PrecioPequeña = TextField(label="Pequeña", hint_text="Ingresar precio", border_radius=30, border_color="#820000", width=150, height=60, on_change=lambda _:[mensaje.quitarError(page, PrecioPequeña), mensaje.validarNumeros(PrecioPequeña, page)])
        PrecioMediana = TextField(label="Mediana", hint_text="Ingresar precio", border_radius=30, border_color="#820000", width=150, height=60, on_change=lambda _:[mensaje.quitarError(page, PrecioMediana), mensaje.validarNumeros(PrecioMediana, page)])
        PrecioRegular = TextField(label="Regular", hint_text="Ingresar precio", border_radius=30, border_color="#820000", width=150, height=60, on_change=lambda _:[mensaje.quitarError(page, PrecioRegular), mensaje.validarNumeros(PrecioRegular, page)])
        PrecioGrande = TextField(label="Grande", hint_text="Ingresar precio", border_radius=30, border_color="#820000", width=150, height=60, on_change=lambda _:[mensaje.quitarError(page, PrecioGrande), mensaje.validarNumeros(PrecioGrande, page)])

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
            db.actualizarPrecios(PrecioPequeña.value, 1)
            db.actualizarPrecios(PrecioMediana.value, 2)
            db.actualizarPrecios(PrecioRegular.value, 3)
            db.actualizarPrecios(PrecioGrande.value, 4)
            mensaje.cerrarAlert(page, alertJornada)
            page.snack_bar = SnackBar(content=Text("Precios Actualizados Correctamente"), bgcolor="GREEN")
            page.snack_bar.open = True
            page.update()

class editarDatosUsuario:
    def editNombreLi(page):
        entryNombre = TextField(label="Nombre", hint_text=mensaje.minimoCaracteres(3), max_length=12, capitalization=TextCapitalization.SENTENCES, border_radius=30, border_color="#820000", width=300, height=60, on_change=lambda _:[mensaje.quitarError(page, entryNombre), mensaje.validarNombres(entryNombre, page)])
        entryNombre.value = gestionPrincipal.nombreLi.value

        alertEditNombre = AlertDialog(
            content=Container(
                alignment=alignment.center,
                height=150,
                width=300,
                bgcolor="white",
                content=Row(
                    spacing=10,
                    controls=[
                        entryNombre,
                    ]
                )
            ),
            actions=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        ElevatedButton("Guardar Cambios", on_click=lambda _:editarDatosUsuario.validarNombreLi(page, entryNombre, alertEditNombre)),
                        ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(page, alertEditNombre))
                    ]
                )
            ]
        )

        page.dialog = alertEditNombre
        alertEditNombre.open = True

        page.update()

    def validarNombreLi(page, widget, alertEditNombre):
        if (widget.value == "") or (len(widget.value) in range(1, 3)):
            if widget.value == "":
                widget.error_text = mensaje.campofaltante
            if len(widget.value) in range(1, 3):
                widget.error_text = mensaje.minimoCaracteres(3)
                page.update()
        else:
            db.actualizarNombreLider(widget.value, mensaje.datosUsuarioLista[0][0])
            gestionPrincipal.textoSlider.value = f"{widget.value}"
            datosUsuario.volverCargarTusDatos(page)
            mensaje.cerrarAlert(page, alertEditNombre)
            page.snack_bar = SnackBar(bgcolor="GREEN", content=Text("El nombre se modifico correctamente"))
            page.snack_bar.open = True
            page.update()

    def editApellidoLi(page):

        entryApellido = TextField(label="Apellido", hint_text="Minimo 4 caracteres", max_length=12, capitalization=TextCapitalization.SENTENCES, border_radius=30, border_color="#820000", width=300, height=60, on_change=lambda _:[mensaje.quitarError(page, entryApellido), mensaje.validarNombres(entryApellido, page)])
        entryApellido.value = gestionPrincipal.apellidoLi.value

        alertEditApellido = AlertDialog(
            content=Container(
                alignment=alignment.center,
                height=150,
                width=300,
                bgcolor="white",
                content=Row(
                    spacing=10,
                    controls=[
                        entryApellido,
                    ]
                )
            ),
            actions=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        ElevatedButton("Guardar Cambios", on_click=lambda _:editarDatosUsuario.validarApellidoLi(page, entryApellido, alertEditApellido)),
                        ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(page, alertEditApellido))
                    ]
                )
            ]
        )

        page.dialog = alertEditApellido
        alertEditApellido.open = True

        page.update()

    def validarApellidoLi(page, widget, alertEditApellido):
        if (widget.value == "") or (len(widget.value) in range(1, 4)):
            if widget.value == "":
                widget.error_text = mensaje.campoFaltante
                page.update()
            if len(widget.value) in range(1, 4):
                widget.error_text = "Minimo de caracteres 4"
                page.update()
        else:
            db.actualizarApellidoLider(widget.value, mensaje.datosUsuarioLista[0][0])
            datosUsuario.volverCargarTusDatos(page)
            mensaje.cerrarAlert(page, alertEditApellido)
            page.snack_bar = SnackBar(bgcolor="GREEN", content=Text("El apellido se modifico correctamente"))
            page.snack_bar.open = True
            page.update()

    def editTelefonoLi(page):
        codigo = gestionPrincipal.telefonoLi.value[:4]
        telefono = gestionPrincipal.telefonoLi.value[-7:]

        selectTipoTelefono = Dropdown(hint_text="Codigo", color="black",border_color="#820000", border_radius=20, width=100, height=60, on_change=lambda _: mensaje.quitarError(page, selectTipoTelefono), options=[
                dropdown.Option("0412"), dropdown.Option("0414"), dropdown.Option("0416"), dropdown.Option("0424"), dropdown.Option("0238")])
        selectTipoTelefono.value = codigo
        entryTelefono = TextField(label="N telefono", hint_text="0000000", border_color="#820000", border_radius=20, width=180, height=60, max_length=7, on_change=lambda _: [mensaje.quitarError(page, entryTelefono), mensaje.validarNumeros(entryTelefono, page)])
        entryTelefono.value = telefono

        alertEditTelefono = AlertDialog(
            content=Container(
                alignment=alignment.center,
                height=150,
                width=300,
                bgcolor="white",
                content=Row(
                    spacing=2,
                    controls=[
                        selectTipoTelefono,
                        entryTelefono,
                    ]
                )
            ),
            actions=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        ElevatedButton("Guardar Cambios", on_click=lambda _:editarDatosUsuario.validarTelefonoLi(page, selectTipoTelefono, entryTelefono, alertEditTelefono)),
                        ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(page, alertEditTelefono))
                    ]
                )
            ]
        )

        page.dialog = alertEditTelefono
        alertEditTelefono.open = True

        page.update()

    def validarTelefonoLi(page, codigo, telefono, alertEditTelefono):

        arregloTelefono = f"{codigo.value}-{telefono.value}"

        if (telefono.value == "") or (len(telefono.value) in range(1, 7)):
            if telefono.value == "":
                telefono.error_text = mensaje.campoFaltante
                page.update()

            if len(telefono.value) in range(1, 7):
                telefono.error_text = "numero de telefono invalido"
                page.update()

        elif db.verificarTelefonoLider(arregloTelefono):
            page.snack_bar = SnackBar(content=Text("Esta numero de telefono ya esta registrada"))
            page.snack_bar.open = True
            page.update()
        
        else:
            db.actualizarTelefonoLider(arregloTelefono, mensaje.datosUsuarioLista[0][0])
            datosUsuario.volverCargarTusDatos(page)
            mensaje.cerrarAlert(page, alertEditTelefono)
            page.snack_bar = SnackBar(bgcolor="GREEN", content=Text("El numero de telefono se modifico correctamente"))
            page.snack_bar.open = True
            page.update()

    #SECCION CORREO
    def editCorreoLi(page):
        direccion = ""
        tipo = ""

        if gestionPrincipal.correoLi.value[-10:] == "@gmail.com":
            direccion = gestionPrincipal.correoLi.value[:-10]
            tipo = gestionPrincipal.correoLi.value[-10:]
        else:
            direccion = gestionPrincipal.correoLi.value[:-12]
            tipo = gestionPrincipal.correoLi.value[-12:]

        entryCorreo = TextField(label="Direccion", hint_text="ej: clapcamoruco", border_color="#820000", border_radius=20, width=180, height=60, on_change=lambda _:[mensaje.quitarError(page, entryCorreo), mensaje.validarCorreo(entryCorreo, page)])
        entryCorreo.value = direccion
        selectTipoCorreo = Dropdown(hint_text="Correo", color="black",border_color="#820000", border_radius=20, width=120, height=60, on_change=lambda _: mensaje.quitarError(page, selectTipoCorreo), options=[
                dropdown.Option("@gmail.com"), dropdown.Option("@hotmail.com")])
        selectTipoCorreo.value = tipo

        alertEditCorreo = AlertDialog(
            content=Container(
                alignment=alignment.center,
                height=150,
                width=300,
                bgcolor="white",
                content=Row(
                    spacing=2,
                    controls=[
                        entryCorreo,
                        selectTipoCorreo,
                    ]
                )
            ),
            actions=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        ElevatedButton("Guardar Cambios", on_click=lambda _:editarDatosUsuario.validarCorreoLi(page, selectTipoCorreo, entryCorreo, alertEditCorreo)),
                        ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(page, alertEditCorreo))
                    ]
                )
            ]
        )

        page.dialog = alertEditCorreo
        alertEditCorreo.open = True

        page.update()

    def validarCorreoLi(page, tipo, correo, alertEditCorreo):

        arregloCorreo = f"{correo.value}{tipo.value}"

        if (correo.value == ""):
            if correo.value == "":
                correo.error_text = mensaje.campoFaltante
                page.update()

        elif db.verificarCorreoLider(arregloCorreo):
            page.snack_bar = SnackBar(content=Text("Esta correo ya esta registrado"))
            page.snack_bar.open = True
            page.update()

        else:
            db.actualizarCorreoLider(arregloCorreo, mensaje.datosUsuarioLista[0][0])
            datosUsuario.volverCargarTusDatos(page)
            mensaje.cerrarAlert(page, alertEditCorreo)
            page.snack_bar = SnackBar(bgcolor="GREEN", content=Text("El correo se modifico correctamente"))
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
        resultado = db.obtenerHistorial(ids)

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
    def volverGenerarArchivos(page):
        gestionPrincipal.bitacoraLista.clear()
        gestionPrincipal.tablaSeleccionarHistorial.rows.clear()

        gestionPrincipal.tablaSeleccionarHistorial.rows = archivos.generarArchivos(page)

        page.update()

    def generarArchivos(page):
        coun = 1

        resultadoId = db.obtenerArchivosId(gestionPrincipal.cedula.value)

        for idss in resultadoId:

            datos = db.obtenerFechasJornadas(idss[0])

            gestionPrincipal.bitacoraLista.append([datos[0][0], datos[0][1]])

        for fecha, ids in gestionPrincipal.bitacoraLista:
            gestionPrincipal.his.append(DataRow(
                color="WHITE",
                cells=[
                    DataCell(Text(f"Jornada {coun}")),
                    DataCell(Text(f"{fecha}")),
                ],
                on_select_changed=lambda _, fecha = fecha, ids = ids: [historial.abrirHistorial(page, fecha, ids)]
            ),
            )
            coun = coun + 1

            page.update()

        return gestionPrincipal.his

    def descargarArchivo(page, alertt, ids):

        origen = db.origenRutaArchivo(ids)
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

        resultadoUsuario = db.obtenerDatosLiderPolitico(mensaje.datosUsuarioLista[0][0])

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