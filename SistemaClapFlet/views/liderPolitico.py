from flet import *
from flet import View, Image, Icon, margin, Offset, ScrollMode, AnimatedSwitcher, DataTable, DataColumn, ListView, PopupMenuButton, PopupMenuItem, Stack, CircleAvatar, Checkbox, AnimatedSwitcherTransition, AnimationCurve, animation, transform, Container, Text, SnackBar, Dropdown, dropdown, alignment, border_radius, border, TextCapitalization, TextField, CrossAxisAlignment, MainAxisAlignment, Column, FontWeight, TextButton, AlertDialog, padding, TextThemeStyle, DataRow, DataCell, Row, icons, IconButton, ElevatedButton
from flet_route import Params, Basket
from datetime import datetime
from time import sleep

import os
import pathlib
import shutil

import modelo.reporte

from controlador.mensajes import mensaje, validaciones
from controlador.rutas import rutas
from modelo.consultas import consulta
from gestores.gestorLiderPolitico import *
from gestores.gestorLiderPolitico import bloqueoUsuario, revelarContrasena, gestionPrincipal, preciosCilindros, editarDatosUsuario, bitacora, archivos, caracteristicasCilindro, datosUsuario, generarCartas, historial

class liderPolitico:
    def __init__(self):       
        self.logo = Image(src=rf"{rutas.rutaActualArreglada}\img\clap.png", height=80)
        self.indicator = Container(bgcolor='WHITE', width=140, height=40, border_radius=border_radius.only(top_left=15, bottom_left=15), offset=transform.Offset(0.075,5.5), animate_offset=animation.Animation(500, AnimationCurve.DECELERATE))

    def view(self, page:Page, params:Params, basket:Basket):

        self.bitacoraLista = []

        self.iDLiderCalle = mensaje.datosUsuarioLista[0][0]
        self.nombreLiderCalle = mensaje.datosUsuarioLista[0][1]
        self.ApellidoLiderCalle = mensaje.datosUsuarioLista[0][2]
        self.UbicacionLiderCalle = mensaje.datosUsuarioLista[0][3]
        self.idUsuario = mensaje.datosUsuarioLista[0][4]
        self.fechaEntradaUser = mensaje.datosUsuarioLista[0][5]

        self.check = Checkbox(on_change=lambda _:bloqueoUsuario.estatusUsuario(page))

        self.entryEmpresa = TextField(label=mensaje.empresa, hint_text=mensaje.minimoCaracteres(3), max_length=12, capitalization=TextCapitalization.SENTENCES, border_radius=30, border_color="#820000", width=300, height=60, on_change=lambda _:[mensaje.quitarError(page, self.entryEmpresa), validaciones.validarCamposNot(self.entryEmpresa, page, True, validaciones.condicionAlfanumericos)])
        self.entryTamano = TextField(label=mensaje.tamano, hint_text=mensaje.minimoCaracteres(3), max_length=12, capitalization=TextCapitalization.SENTENCES, border_radius=30, border_color="#820000", width=300, height=60, on_change=lambda _:[mensaje.quitarError(page, self.entryTamano), validaciones.validarCamposNot(self.entryTamano, page, False, validaciones.condicionNombres)])
        self.entryPico = TextField(label=mensaje.pico, hint_text=mensaje.minimoCaracteres(3), max_length=12, capitalization=TextCapitalization.SENTENCES, border_radius=30, border_color="#820000", width=300, height=60, on_change=lambda _:[mensaje.quitarError(page, self.entryPico), validaciones.validarCamposNot(self.entryPico, page, False, validaciones.condicionNombres)])

        self.entryComunidad = TextField(label="Comunidad", hint_text="Minimo 4 caracteres", max_length=30, capitalization=TextCapitalization.SENTENCES, border_radius=30, border_color="#820000", width=300, height=60, on_change=lambda _:[mensaje.quitarError(page, self.entryComunidad), validaciones.validarCamposNot(self.entryComunidad, page, True, validaciones.condicionAlfanumericos)])

        page.title = "CLAP"
        page.window_maximizable = False
        page.window_resizable = False
        page.window_height = "800"
        page.window_width = "1000"
        page.window_center()

        self.titulo = Text("Lideres de Calle", style=TextThemeStyle.TITLE_LARGE, color="white")
        self.textoSlider = Text(f"{self.nombreLiderCalle}", weight=FontWeight.W_500, color="WHITE")

        self.nombreLi = Text("")
        self.apellidoLi = Text("")
        self.cedulaLi = Text("")
        self.ubicacionLi = Text("")
        self.telefonoLi = Text("")
        self.correoLi = Text("")
        self.preguntaP = Text("")
        self.respuestaP = Text("")
        self.usuarioP = Text("")
        self.contrasenaP = Text("", visible=False)

        
        self.codigoTelefono = Dropdown(hint_text="Codigo", visible=False, color="black",border_color="#820000", border_radius=20, width=100, height=60, on_change=lambda _: mensaje.quitarError(page, self.codigoTelefono), options=[
                dropdown.Option("0412"), dropdown.Option("0414"), dropdown.Option("0416"), dropdown.Option("0424"), dropdown.Option("0238")])
        self.numeroTelefono = TextField(label="N telefono", visible=False, hint_text="0000000", border_color="#820000", border_radius=20, width=180, height=60, max_length=7, on_change=lambda _: [mensaje.quitarError(page, self.numeroTelefono), validaciones.validarCamposNot(self.numeroTelefono, page, True, validaciones.condicionNumeros)])
        self.correoCambiar = TextField(label="Direccion", visible=False, hint_text="ej: clapcamoruco", max_length=50, border_color="#820000", border_radius=20, width=180, height=60, on_change=lambda _: mensaje.quitarError(page, self.correo))
        self.tipoCorreo = Dropdown(hint_text="Correo", visible=False, color="black",border_color="#820000", border_radius=20, width=120, height=60, on_change=lambda _: mensaje.quitarError(page, self.tipoCorreo), options=[
                dropdown.Option("@gmail.com"), dropdown.Option("@hotmail.com"), dropdown.Option("@outlook.com")])


        self.nombre = Text("")
        self.apellido = Text("")
        self.cedula = Text("")
        self.ubicacion = Text("")
        self.pregunta = Text("")
        self.respuesta = Text("")
        self.usuario = Text("")
        self.contrasena = Text("", visible=False)
        self.telefono = Text("")
        self.correo = Text("")
        self.estatus = Text("")

        self.btnCandado = IconButton(icon=icons.LOCK_OUTLINE, on_click=lambda _:revelarContrasena.revelarPass(page, self.contrasena))
        self.btnCandadoP = IconButton(icon=icons.LOCK_OUTLINE, on_click=lambda _:revelarContrasena.revelarPass(page, self.contrasenaP))

        self.tablaSeleccionarHistorial = DataTable(
            bgcolor="#C5283D",
            columns=[
                DataColumn(Text("Jornada", color="WHITE")),
                DataColumn(Text("Fecha", color="WHITE")),
            ],
            rows=[

            ]
        )

        self.tablaLlenarHistorial = DataTable(
            bgcolor="#C5283D",
            columns=[
                #DataColumn(Text("id")),
                DataColumn(Text("Ci", color="WHITE")),
                DataColumn(Text("Nombre", color="WHITE")),
                DataColumn(Text("Apellido", color="WHITE")),
                DataColumn(Text(mensaje.empresa, color="WHITE")),
                DataColumn(Text(mensaje.tamano, color="WHITE")),
                DataColumn(Text(mensaje.pico, color="WHITE")),
                DataColumn(Text("Agregado", color="WHITE"))
            ],
            rows=[

            ]
        )

        self.columnaCards = Row(
            wrap=True,
        )
        
        self.listaBitacora = ListView(width=400, height=550, spacing=20)

        #APP BAR
        self.appbar = Container(
            bgcolor="#C5283D",
            border_radius=border_radius.all(15),
            height=100,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Container(padding=padding.only(left=10) ,content=self.logo),
                    self.titulo,
                    PopupMenuButton(items=[PopupMenuItem(text="Cerrar seccion", on_click=lambda _: gestionPrincipal.volverLogin(page, self.indicator))])
                ]
            )
        )

        #SLIDER
        self.slider = Container(
            height=635,
            width=150,
            bgcolor="#C5283D",
            border_radius=border_radius.all(15),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=10,
                height=630,
                width=150,
                expand=True,
                controls=[
                    Stack(
                        controls=[
                            Column(
                                height=630,
                                controls=[
                                    self.indicator
                                ]
                            ),

                            Column(
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=10,
                                controls=[
                                    Container(
                                        padding=padding.only(top=25),
                                        content=Column(
                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                            controls=[
                                                CircleAvatar(
                                                    content=Icon(icons.PEOPLE),
                                                    width=80,
                                                    height=80,
                                                ),
                                                Text("Bienvenido", weight=FontWeight.W_500, color="WHITE"),
                                                self.textoSlider,
                                            ]
                                        )
                                    ),

                                    Container(
                                        
                                        margin=margin.only(top=50),
                                        padding=padding.only(left=35),
                                        offset=Offset(x=None, y=None),
                                        data=0,
                                        on_click=lambda e: [rutas.animar(self.formulario, self.contenedorInicio, self.contenedorInicio, page), mensaje.cambiarPagina(self.indicator, 5.5), mensaje.cambiarTitulo(page, self.titulo, "Lideres de Calle")],
                                        content=Row(
                                            controls=[
                                                Icon(name=icons.HOME),
                                                Text("Inicio")
                                            ]
                                        )
                                    ),

                                    Container(
                                        margin=margin.only(top=20),
                                        padding=padding.only(left=35),
                                        data=0,
                                        on_click=lambda e: [rutas.animar(self.formulario, self.contenedorBombonas, self.contenedorBombonas, page), mensaje.cambiarPagina(self.indicator, 6.8), mensaje.cambiarTitulo(page, self.titulo, "Gestion de Bombonas")],
                                        content=Row(
                                            controls=[
                                                Icon(name=icons.EVENT_NOTE),
                                                Text("Bombonas")
                                            ]
                                        )
                                    ),

                                    Container(
                                        margin=margin.only(top=20),
                                        padding=padding.only(left=35),
                                        offset=Offset(x=None, y=None),
                                        data=0,
                                        on_click=lambda e: [rutas.animar(self.formulario, self.contenedorPerfil, self.contenedorPerfil, page), mensaje.cambiarPagina(self.indicator, 8.2), mensaje.cambiarTitulo(page, self.titulo, "Tu Perfil"), revelarContrasena.regresarPassFalse(page, self.contrasena)],
                                        content=Row(
                                            controls=[
                                                Icon(name=icons.PEOPLE),
                                                Text("Tu Perfil")
                                            ]
                                        )
                                    ),
                                ]
                            )
                        ]
                    )
                ]
            )
        )


        #CONTENEDORES PRINCIPALES
        self.contenedorInicio = Container(
            height=635,
            width=815,
            padding=15,
            expand=True,
            bgcolor="WHITE",
            border=border.all(2, "#C5283D"),
            border_radius=border_radius.all(15),
            alignment=alignment.center,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Row(
                        height=50,
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Text(""),
                            ElevatedButton("Actualizar Precios", bgcolor="Yellow", color="Black", on_click=lambda _: preciosCilindros.menuPrecios(page))
                        ]
                    ),
                    self.columnaCards
                ]    
            )
        )

        self.contenedorPerfil = Container(
            height=635,
            width=815,
            expand=True,
            bgcolor="WHITE",
            border=border.all(2, "#C5283D"),
            padding=padding.only(top=10),
            alignment=alignment.center,
            border_radius=border_radius.all(15),
            content=Column(
                spacing=20,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        bgcolor="white",
                        height=500,
                        width=800,
                        padding=padding.only(top=40),
                        border_radius=border_radius.all(40),
                        alignment=alignment.center,
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                Column(
                                    controls=[
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Nombre:"),
                                                self.nombreLi,
                                                IconButton(icon=icons.EDIT, tooltip="Editar Nombre", on_click=lambda _: editarDatosUsuario.editNombreLi(page, self.textoSlider))
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Apellido:"),
                                                self.apellidoLi,
                                                IconButton(icon=icons.EDIT, tooltip="Editar Apellido", on_click=lambda _: editarDatosUsuario.editApellidoLi(page, self.slider))
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Cedula:"),
                                                self.cedulaLi
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Telefono:"),
                                                self.telefonoLi,
                                                IconButton(icon=icons.EDIT, tooltip="Editar Telefono", on_click=lambda _: editarDatosUsuario.editTelefonoLi(page))
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Correo:"),
                                                self.correoLi,
                                                IconButton(icon=icons.EDIT, tooltip="Editar Correo", on_click=lambda _: editarDatosUsuario.editCorreoLi(page))
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Ubicacion:"),
                                                self.ubicacionLi,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Pregunta:"),
                                                self.preguntaP,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Respuesta:"),
                                                self.respuestaP,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Usuario:"),
                                                self.usuarioP,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Contraseña:"),
                                                self.contrasenaP,
                                                self.btnCandadoP
                                            ]
                                        ),
                                    ]
                                ),
                                Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                ElevatedButton("Regresar", bgcolor="#cb3234", color="#ffffff", on_click=lambda _:[ rutas.animar(self.formulario, self.contenedorInicio, self.contenedorInicio, page), mensaje.cambiarPagina(self.indicator, 5.5), mensaje.cambiarTitulo(page, self.titulo, "Lideres de Calle"), revelarContrasena.regresarPassFalse(page, self.contrasenaP)]),
                                                ElevatedButton("Ver tu bitacora", on_click=lambda _: [rutas.animar(self.formulario, self.formularioBitacora, self.formularioBitacora, page), mensaje.cambiarTitulo(page, self.titulo, "Historial de Inicios de sesion"), bitacora.volverGenerarBitacora(page, self.cedulaLi)])
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )

        self.contenedorHistorial = Container(
            height=635,
            width=815,
            expand=True,
            bgcolor="WHITE",
            padding=15,
            border=border.all(2, "#C5283D"),
            alignment=alignment.center,
            border_radius=border_radius.all(15),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        bgcolor="white",
                        height=550,
                        border_radius=border_radius.all(7),  
                        content=Column(
                            expand=True,
                            height=550,
                            scroll=ScrollMode.ALWAYS,
                            controls=[
                                self.tablaSeleccionarHistorial,
                            ]
                        )
                    ),

                    Row(
                        controls=[
                            ElevatedButton("Regresar", bgcolor="#cb3234", color="#ffffff", on_click=lambda _:[rutas.animar(self.formulario, self.contenedorInicio, self.contenedorInicio, page), mensaje.cambiarPagina(self.indicator, 5.5), mensaje.cambiarTitulo(page, self.titulo, "Mi Comunidad")])
                        ]
                    ),
                ]
            )
        )

        self.formularioLiderCalle = Container(
            height=635,
            width=815,
            expand=True,
            bgcolor="WHITE",
            border=border.all(2, "#C5283D"),
            padding=padding.only(top=10),
            alignment=alignment.center,
            border_radius=border_radius.all(15),
            content=Column(
                spacing=20,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        bgcolor="white",
                        height=500,
                        width=350,
                        padding=padding.only(top=40),
                        border_radius=border_radius.all(40),
                        alignment=alignment.center,
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Column(
                                    controls=[
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Nombre:"),
                                                self.nombre,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Apellido:"),
                                                self.apellido,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Cedula:"),
                                                self.cedula,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Ubicacion:"),
                                                self.ubicacion,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Telefono:"),
                                                self.telefono,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Correo:"),
                                                self.correo,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Pregunta:"),
                                                self.pregunta,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Respuesta:"),
                                                self.respuesta,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Usuario:"),
                                                self.usuario,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Contraseña:"),
                                                self.contrasena,
                                                self.btnCandado
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                Text("Estatus:"),
                                                self.estatus,
                                                self.check
                                            ]
                                        ),
                                    ]
                                ),
                                Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            spacing=20,
                                            controls=[
                                                ElevatedButton("Regresar", bgcolor="#cb3234", color="#ffffff", on_click=lambda _:[ rutas.animar(self.formulario, self.contenedorInicio, self.contenedorInicio, page), mensaje.cambiarTitulo(page, self.titulo, "Lideres de Calle"), revelarContrasena.regresarPassFalse(page, self.contrasena)]),
                                                ElevatedButton("Ver Jornadas", bgcolor="Green", color="#ffffff", on_click=lambda _:[ rutas.animar(self.formulario, self.contenedorHistorial, self.contenedorHistorial, page), mensaje.cambiarTitulo(page, self.titulo, "Administrador de jornadas"), archivos.volverGenerarArchivos(page, consulta.obtenerArchivosId, self.cedula.value, self.tablaSeleccionarHistorial, historial.abrirHistorial)])
                                            ]
                                        ),
                                        ElevatedButton("Ver bitacora", on_click=lambda _: [rutas.animar(self.formulario, self.formularioBitacora, self.formularioBitacora, page), mensaje.cambiarTitulo(page, self.titulo, "Historial de Inicios de sesion"), bitacora.volverGenerarBitacora(page, self.cedula)])
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )

        self.formularioBitacora = Container(
            height=635,
            width=815,
            expand=True,
            bgcolor="WHITE",
            border=border.all(2, "#C5283D"),
            padding=padding.only(top=10),
            alignment=alignment.center,
            border_radius=border_radius.all(15),
            content=Column(
                spacing=20,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    self.listaBitacora,
                    ElevatedButton("Regresar", bgcolor="#cb3234", color="#ffffff", on_click=lambda _:[ rutas.animar(self.formulario, self.contenedorInicio, self.contenedorInicio, page), mensaje.cambiarTitulo(page, self.titulo, "Lideres de Calle"), mensaje.cambiarPagina(self.indicator, 5.5), bitacora.regresarViewFalse(page)]),
                ]
            )
        )

        self.contenedorBombonas = Container(
            height=635,
            width=815,
            padding=15,
            expand=True,
            bgcolor="WHITE",
            border=border.all(2, "#C5283D"),
            border_radius=border_radius.all(15),
            alignment=alignment.center,
            content=Column(
                spacing=30,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
#                    ElevatedButton("Agregar nueva Empresa", on_click=lambda _: caracteristicasCilindro.nuevaEmpresa(page)),
                    ElevatedButton("Agregar nueva Empresa", on_click=lambda _: caracteristicasCilindro.nuevaCaracteristica(page, mensaje.anadirNuevaEmpresa, self.entryEmpresa, caracteristicasCilindro.ValidarNuevaCaracteristica, consulta.verificarEmpresa, mensaje.empresaDuplicada, mensaje.anadidoEmpresa)),
                    ElevatedButton("Agregar nuevo Pico", on_click=lambda _: caracteristicasCilindro.nuevaCaracteristica(page, mensaje.anadirNuevoPico, self.entryPico, caracteristicasCilindro.ValidarNuevaCaracteristica, consulta.verificarPico, mensaje.picoDuplicado, mensaje.anadidoPico))            
                ]
            )
        )

        #SALTOS DE VISTAS
        #Contenedor del medio
        self.formulario = AnimatedSwitcher(
            self.contenedorInicio,
            expand=True, 
            transition=AnimatedSwitcherTransition.FADE,
            duration=500,
            reverse_duration=100,
            switch_in_curve=AnimationCurve.BOUNCE_OUT,
            switch_out_curve=AnimationCurve.BOUNCE_IN
        )

        self.pasarWidget()
        datosUsuario.volverCargarTusDatos(page)
        generarCartas.volverGenerarCartas(page)

        return View(
            "/liderPolitico",
            padding=5,
            controls=[
                self.appbar,

                Container(
                    padding=0,
                    margin=0,
                    content=Row(
                        alignment=CrossAxisAlignment.START,
                        controls=[
                            self.slider,
                            self.formulario
                        ]
                    )
                )
            ]
        )


    #ESTA FUNCION CUENTA CON UNA CANTIDAD ELEVADA DE PARAMETROS POR QUE DE DICHA MANERA SE MANEJA MEJOR LOS PARAMETROS DE LA LOGICA,
    #YA QUE QUEDAN ALMACENADOS EN UNA CLASE Y LAS FUNCIONES QUE REQUIERAN LOS WIDGET SIMPLEMENTE LE HACEN UN LLAMADO
    def pasarWidget(self):
        gestionPrincipal.obtenerWidget(self.formulario, self.nombre, self.apellido, self.cedula, self.estatus, self.contrasena, self.usuario, 
        self.pregunta, self.respuesta, self.ubicacion, self.telefono, self.correo, self.columnaCards, 
        self.titulo, self.contenedorInicio, self.contenedorHistorial, self.formularioBitacora, self.formularioLiderCalle, self.contenedorBombonas, 
        self.contenedorPerfil, self.listaBitacora, self.nombreLi, self.apellidoLi, self.cedulaLi, self.ubicacionLi, 
        self.telefonoLi, self.correoLi, self.preguntaP, self.respuestaP, self.usuarioP, self.contrasenaP, 
        self.tablaLlenarHistorial, self.tablaSeleccionarHistorial, self.check, self.btnCandado, self.btnCandadoP)