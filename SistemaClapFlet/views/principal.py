from flet import *
from flet import View, AnimatedSwitcher, AnimatedSwitcherTransition, ScrollMode, margin, DataColumn, DataTable, PopupMenuButton, PopupMenuItem, Stack, CircleAvatar, Icon, Image, AnimationCurve, animation, transform, Container, Text, SnackBar, Dropdown, dropdown, alignment, border_radius, border, TextCapitalization, TextField, CrossAxisAlignment, MainAxisAlignment, Column, FontWeight, TextButton, AlertDialog, padding, TextThemeStyle, DataRow, DataCell, Row, icons, IconButton, ElevatedButton

from flet_route import Params, Basket
from datetime import datetime
from time import sleep

import os
import pathlib
import shutil

import modelo.reporte

from controlador.mensajes import mensaje
from controlador.rutas import rutas
from gestores.gestorPincipal import *
from gestores.gestorPincipal import regresarAtras, reporteJornada, archivoPdf, editarDatosLiderCalle, editarDatosJefeFamilia, gestionPrincipal, cartasJefesFamilia, registrarJefeFamiliaCilindros, crudCilindros

class principal:
    def __init__(self):
        self.logo = Image(src=rf"{rutas.rutaActualArreglada}\img\clap.png", height=80)        
        self.indicator = Container(bgcolor='WHITE', width=140, height=40, border_radius=border_radius.only(top_left=15, bottom_left=15), offset=transform.Offset(0.075,5.5), animate_offset=animation.Animation(500, AnimationCurve.DECELERATE))

    def view(self, page:Page, params:Params, basket:Basket):
        #DATOS DEL JEFE DE FAMILIA
        self.nombreJ = Text("")
        self.apellidoJ = Text("")
        self.cedulaJ = Text("")
        self.ubicacionJ = Text("")
        self.telefonoJ = Text("")
        self.correoJ = Text("")

        #DATOS DEL LIDER DE CALLE
        self.nombreLi = Text("")
        self.apellidoLi = Text("")
        self.cedulaLi = Text("")
        self.ubicacionLi = Text("")
        self.telefonoLi = Text("")
        self.correoLi = Text("")

        #DATOS BASICOS DEL INCIO DE SECCION
        self.iDLiderCalle = mensaje.datosUsuarioLista[0][0]
        self.nombreLiderCalle = mensaje.datosUsuarioLista[0][1]
        self.ApellidoLiderCalle = mensaje.datosUsuarioLista[0][2]
        self.UbicacionLiderCalle = mensaje.datosUsuarioLista[0][3]
        self.idUsuario = mensaje.datosUsuarioLista[0][4]
        self.fechaEntradaUser = mensaje.datosUsuarioLista[0][5]

        self.textoSlider = Text(f"{self.nombreLiderCalle}", weight=FontWeight.W_500, color="WHITE")

        #CARACTERISTICAS DE LA  VENTANA
        page.title = "CLAP"
        page.window_resizable = False
        page.window_height = "800"
        page.window_width = "1000"
        page.window_center()
        page.window_maximizable = False

        #WIDGET PARA TITULOS
        self.titulo = Text(mensaje.tituloComunidad, style=TextThemeStyle.TITLE_LARGE, color="white")
        self.tituloCilindroPropietario = Text("", style=TextThemeStyle.TITLE_LARGE)
        self.tituloCilindroSeleccionado = Text("", style=TextThemeStyle.TITLE_LARGE)
        self.tituloAgregarJefes = Text(mensaje.mensajeSinJefesFamilia, style=TextThemeStyle.TITLE_LARGE)

        #TEXTFIELDS REGISTRO
        self.nombre = TextField(label=mensaje.nombre, hint_text=mensaje.minimoCaracteres(3), max_length=12, capitalization=TextCapitalization.SENTENCES, border_radius=30, border_color="#820000", width=300, height=60, on_change=lambda _:[mensaje.quitarError(page, self.nombre), mensaje.validarNombres(self.nombre, page)])
        self.apellido = TextField(label=mensaje.apellido, hint_text=mensaje.minimoCaracteres(4), max_length=12, capitalization=TextCapitalization.SENTENCES, border_radius=30, border_color="#820000", width=300, height=60, on_change=lambda _:[mensaje.quitarError(page, self.apellido), mensaje.validarNombres(self.apellido, page)])
        self.tipoCedula = Dropdown(label=mensaje.tipo, color="black",border_color="#820000", border_radius=20, width=100, height=60, on_change=lambda _: mensaje.quitarError(page, self.tipoCedula), options=[
                dropdown.Option("V"), dropdown.Option("E")])
        self.tipoCedula.value = "V"
        self.cedula = TextField(label=mensaje.cedula, hint_text=mensaje.minimoCaracteres(7), border_color="#820000", border_radius=20, width=180, height=60, max_length=8, on_change=lambda _: [mensaje.quitarError(page, self.cedula), mensaje.validarNumeros(self.cedula, page)])
        self.cantidadCi = Dropdown(label=mensaje.cantidadCilindros, border_radius=30, border_color="#820000", width=300, height=60, value=0, on_change=lambda _: [self.generarCasillasCilindro(page), mensaje.quitarError(page, self.cantidadCi)], options=[
                dropdown.Option("1"), dropdown.Option("2"), dropdown.Option("3"),
                dropdown.Option("4"), dropdown.Option("5"), dropdown.Option("6"),
                dropdown.Option("7"), dropdown.Option("8"), dropdown.Option("9"),
            ]
        )

        self.codigoTelefono = Dropdown(hint_text=mensaje.codigoTelefono, color="black",border_color="#820000", border_radius=20, width=100, height=60, on_change=lambda _: mensaje.quitarError(page, self.codigoTelefono), options=[
                dropdown.Option("0412"), dropdown.Option("0414"), dropdown.Option("0416"), dropdown.Option("0424"), dropdown.Option("0238")])
        self.numeroTelefono = TextField(label=mensaje.nTelefono, hint_text="0000000", border_color="#820000", border_radius=20, width=180, height=60, max_length=7, on_change=lambda _: [mensaje.quitarError(page, self.numeroTelefono), mensaje.validarNumeros(self.numeroTelefono, page)])
        self.correo = TextField(label=mensaje.correo, hint_text="ej: clapcamoruco", border_color="#820000", border_radius=20, width=180, height=60, on_change=lambda _:[mensaje.quitarError(page, self.correo), mensaje.validarCorreo(self.correo, page)])
        self.tipoCorreo = Dropdown(hint_text=mensaje.tipoCorreo, color="black",border_color="#820000", border_radius=20, width=120, height=60, on_change=lambda _: mensaje.quitarError(page, self.tipoCorreo), options=[
                dropdown.Option("@gmail.com"), dropdown.Option("@hotmail.com"), dropdown.Option("@outlook.com")])

        #CONTENEDORES EN COLUMNAS
        self.columnaContenedor = Row(
            vertical_alignment=MainAxisAlignment.CENTER,
            alignment=alignment.center,
            wrap=True,
        )

        self.columnaCards = Row(
            wrap=True,
        )

        self.tablaCilindros = DataTable(
            bgcolor="#C5283D",
            columns=[
                DataColumn(Text(mensaje.idColumnas, color="WHITE")),
                DataColumn(Text(mensaje.empresa, color="WHITE")),
                DataColumn(Text(mensaje.tamano, color="WHITE")),
                DataColumn(Text(mensaje.pico, color="WHITE")),
                DataColumn(Text("Fecha Registrado", color="WHITE")),
                DataColumn(Text(mensaje.acciones, color="WHITE"))
            ],
            rows=[

            ]
        )

        self.tablaPedido = DataTable(
            bgcolor="#C5283D",
            columns=[
                DataColumn(Text(mensaje.idColumnas, color="WHITE")),
                DataColumn(Text(mensaje.empresa, color="WHITE")),
                DataColumn(Text(mensaje.tamano, color="WHITE")),
                DataColumn(Text(mensaje.pico, color="WHITE")),
                DataColumn(Text(mensaje.acciones, color="WHITE"))
            ],
            rows=[

            ]
        )

        self.tablaJornadaPrincipal = DataTable(
            bgcolor="#C5283D",
            column_spacing=30,
            columns=[
                DataColumn(Text("Ci", color="WHITE")),
                DataColumn(Text(mensaje.nombre, color="WHITE")),
                DataColumn(Text(mensaje.apellido, color="WHITE")),
                DataColumn(Text(mensaje.empresa, color="WHITE")),
                DataColumn(Text(mensaje.tamano, color="WHITE")),
                DataColumn(Text(mensaje.pico, color="WHITE")),
                DataColumn(Text("Agregado", color="WHITE")),
                DataColumn(Text(mensaje.acciones, color="WHITE"))
            ],
            rows=[

            ]
        )

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
                DataColumn(Text("Ci", color="WHITE")),
                DataColumn(Text(mensaje.nombre, color="WHITE")),
                DataColumn(Text(mensaje.apellido, color="WHITE")),
                DataColumn(Text(mensaje.empresa, color="WHITE")),
                DataColumn(Text(mensaje.tamano, color="WHITE")),
                DataColumn(Text(mensaje.pico, color="WHITE")),
                DataColumn(Text("Agregado", color="WHITE"))
            ],
            rows=[

            ]
        )

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
                    PopupMenuButton(items=[PopupMenuItem(text=mensaje.cerrarSeccion, on_click=lambda _: regresarAtras.volverLogin(page, self.indicator))])
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
                                                Text(mensaje.bienvenida, weight=FontWeight.W_500, color="WHITE"),
                                                self.textoSlider,
                                            ]
                                        )
                                    ),

                                    Container(
                                        margin=margin.only(top=50),
                                        padding=padding.only(left=35),
                                        data=0,
                                        on_click=lambda e: [rutas.animar(self.formulario, self.contenedorInicio, self.contenedorInicio, page), mensaje.cambiarPagina(self.indicator, 5.5), mensaje.cambiarTitulo(page, self.titulo, "Mi Comunidad")],
                                        content=Row(
                                            controls=[
                                                Icon(name=icons.HOME),
                                                Text(mensaje.inicio)
                                            ]
                                        )
                                    ),

                                    Container(
                                        margin=margin.only(top=20),
                                        padding=padding.only(left=35),
                                        data=0,
                                        on_click=lambda e: [rutas.animar(self.formulario, self.contenedorReporte, self.contenedorReporte, page), mensaje.cambiarPagina(self.indicator, 6.8), reporteJornada.volverGenerarJornada(page, self.iDLiderCalle), mensaje.cambiarTitulo(page, self.titulo, "Administrador de Jornada")],
                                        content=Row(
                                            controls=[
                                                Icon(name=icons.EDIT_NOTE),
                                                Text(mensaje.reporte)
                                            ]
                                        )
                                    ),

                                    Container(
                                        margin=margin.only(top=20),
                                        padding=padding.only(left=35),
                                        data=0,
                                        on_click=lambda e: [rutas.animar(self.formulario, self.contenedorHistorial, self.contenedorHistorial, page), mensaje.cambiarPagina(self.indicator, 8.2), archivoPdf.volverGenerarArchivos(page), mensaje.cambiarTitulo(page, self.titulo, "Historial de jornadas")],
                                        content=Row(
                                            controls=[
                                                Icon(name=icons.EVENT_NOTE),
                                                Text(mensaje.historial)
                                            ]
                                        )
                                    ),
                                    Container(
                                        margin=margin.only(top=20),
                                        padding=padding.only(left=35),
                                        data=0,
                                        on_click=lambda e: [rutas.animar(self.formulario, self.contenedorPerfilLider, self.contenedorPerfilLider, page), editarDatosLiderCalle.cargarDatosLider(page), mensaje.cambiarPagina(self.indicator, 9.5), mensaje.cambiarTitulo(page, self.titulo, "Mis datos")],
                                        content=Row(
                                            controls=[
                                                Icon(name=icons.PEOPLE),
                                                Text(mensaje.perfil)
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
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Row(
                        height=50,
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Text(""),
                            ElevatedButton("Agregar", bgcolor="GREEN", color="WHITE",on_click= lambda _: [rutas.animar(self.formulario, self.formularioJefe, self.formularioJefe, page), mensaje.cambiarTitulo(page, self.titulo, "Datos Personales del Jefe de Familia")])
                        ]
                    ),

                    Container(
                        height=550,
                        border_radius=border_radius.all(7),  
                        content=Column(
                            expand=True,
                            height=550,
                            scroll=ScrollMode.ALWAYS,
                            controls=[
                                self.columnaCards,
                                self.tituloAgregarJefes
                            ]
                        )
                    )
                ]
            )
        )

        self.contenedorReporte = Container(
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
                                self.tablaJornadaPrincipal,
                            ]
                        )
                    ),

                    Row(
                        controls=[
                            ElevatedButton(mensaje.regresarBtn, bgcolor="#cb3234", color="#ffffff", on_click=lambda _:[rutas.animar(self.formulario, self.contenedorInicio, self.contenedorInicio, page), mensaje.cambiarPagina(self.indicator, 5.5), mensaje.cambiarTitulo(page, self.titulo, "Mi Comunidad")]),
                            ElevatedButton("Generar Reporte",bgcolor="GREEN", color="WHITE", on_click=lambda _:reporteJornada.confirmarReporte(page, self.indicator))
                        ]
                    ),
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
                            ElevatedButton(mensaje.regresarBtn, bgcolor="#cb3234", color="#ffffff", on_click=lambda _:[rutas.animar(self.formulario, self.contenedorInicio, self.contenedorInicio, page), mensaje.cambiarPagina(self.indicator, 5.5), mensaje.cambiarTitulo(page, self.titulo, "Mi Comunidad")])
                        ]
                    ),
                ]
            )
        )

        #CONTENEDOR CON LOS DATOS PERSONALES DEL JEFE DE FAMILIA DONDE SE PUEDE EDITAR
        self.contenedorPerfilJefe = Container(
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
                        padding=padding.only(top=60),
                        border_radius=border_radius.all(40),
                        alignment=alignment.center,
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    controls=[
                                        Text("Nombre:"),
                                        self.nombreJ,
                                        IconButton(icon=icons.EDIT, tooltip="Editar Nombre", on_click=lambda _: editarDatosJefeFamilia.editNombre(page, self.iDLiderCalle, self.tablaPedido, self.tablaCilindros))
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    controls=[
                                        Text("Apellido:"),
                                        self.apellidoJ,

                                        IconButton(icon=icons.EDIT, tooltip="Editar Apellido", on_click=lambda _: editarDatosJefeFamilia.editApellido(page, self.iDLiderCalle, self.tablaPedido, self.tablaCilindros))
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    controls=[
                                        Text("Cedula:"),
                                        self.cedulaJ,
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    controls=[
                                        Text("Ubicacion:"),
                                        self.ubicacionJ,
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    controls=[
                                        Text("Telefono:"),
                                        self.telefonoJ,
                                        IconButton(icon=icons.EDIT, tooltip="Editar Telefono", on_click=lambda _: editarDatosJefeFamilia.editTelefono(page, self.iDLiderCalle, self.tablaPedido, self.tablaCilindros))
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    controls=[
                                        Text("Correo:"),
                                        self.correoJ,
                                        IconButton(icon=icons.EDIT, tooltip="Editar Correo", on_click=lambda _: editarDatosJefeFamilia.editCorreo(page, self.iDLiderCalle, self.tablaPedido, self.tablaCilindros))
                                    ]
                                ),
                                ElevatedButton("Regresar a inicio", bgcolor="#cb3234", color="#ffffff", on_click=lambda _:[ rutas.animar(self.formulario, self.contenedorInicio, self.contenedorInicio, page), mensaje.cambiarPagina(self.indicator, 5.5), mensaje.cambiarTitulo(page, self.titulo, "Mi Comunidad")]),
                            ]
                        )
                    )
                ]
            )
        )

        #CONTENEDOR CON LOS DATOS PERSONALES DEL LIDER DE CALLE DONDE SE PUEDE EDITAR
        self.contenedorPerfilLider = Container(
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
                        padding=padding.only(top=60),
                        border_radius=border_radius.all(40),
                        alignment=alignment.center,
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    controls=[
                                        Text("Nombre:"),
                                        self.nombreLi,
                                        IconButton(icon=icons.EDIT, tooltip="Editar Nombre", on_click=lambda _: editarDatosLiderCalle.editNombreLi(page, self.textoSlider))
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    controls=[
                                        Text("Apellido:"),
                                        self.apellidoLi,
                                        IconButton(icon=icons.EDIT, tooltip="Editar Apellido", on_click=lambda _: editarDatosLiderCalle.editApellidoLi(page, self.textoSlider))
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    controls=[
                                        Text("Cedula:"),
                                        self.cedulaLi,
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
                                        Text("Telefono:"),
                                        self.telefonoLi,
                                        IconButton(icon=icons.EDIT, tooltip="Editar Telefono", on_click=lambda _: editarDatosLiderCalle.editTelefonoLi(page))
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    controls=[
                                        Text("Correo:"),
                                        self.correoLi,
                                        IconButton(icon=icons.EDIT, tooltip="Editar Correo", on_click=lambda _: editarDatosLiderCalle.editCorreoLi(page))
                                    ]
                                ),
                                ElevatedButton("Regresar a inicio", bgcolor="#cb3234", color="#ffffff", on_click=lambda _:[ rutas.animar(self.formulario, self.contenedorInicio, self.contenedorInicio, page), mensaje.cambiarPagina(self.indicator, 5.5), mensaje.cambiarTitulo(page, self.titulo, "Mi Comunidad")]),
                            ]
                        )
                    )
                ]
            )
        )

        #FORMULARIO REGISTRO JEFE
        self.formularioJefe = Container(
            height=635,
            width=815,
            expand=True,
            bgcolor="WHITE",
            border=border.all(2, "#C5283D"),
            padding=padding.only(top=30),
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
                            spacing=10,
                            controls=[
                                Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        self.nombre,
                                        self.apellido,
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                self.tipoCedula,
                                                self.cedula,
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                self.codigoTelefono,
                                                self.numeroTelefono
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                self.correo,
                                                self.tipoCorreo
                                            ]
                                        ),
                                        self.cantidadCi,
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    controls=[
                                        ElevatedButton(mensaje.regresarBtn, bgcolor="#cb3234", color="#ffffff", on_click=lambda _:[ self.regresarJefesFamiliaInicio(page), mensaje.cambiarTitulo(page, self.titulo, "Mi Comunidad")]),
                                        ElevatedButton("Seguir",bgcolor="GREEN", color="WHITE", on_click=lambda _: self.accionBtnFormularioJefeFamilia(page))
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )

        self.formularioCilindro = Container(
            height=635,
            width=815,
            expand=True,
            padding=10,
            bgcolor="WHITE",
            border=border.all(2, "#C5283D"),
            border_radius=border_radius.all(15),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    self.columnaContenedor,
                    ElevatedButton("Guardar", bgcolor="GREEN", color="#ffffff",  on_click=lambda _:self.accionBtnFormularioCilindros(page)),
                    ElevatedButton(mensaje.regresarBtn, bgcolor="#cb3234", color="#ffffff", on_click=lambda _:[self.regresarJefesFamiliaCilindro(page), mensaje.cambiarTitulo(page, self.titulo, "Datos Personales del Jefe de Familia")])
                ]
            )
        )

        #VISTA DE CILINDROS DE JEFES DE FAMILIA
        self.contenedorJefeFamilia = Container(
            height=635,
            width=815,
            padding=3,
            expand=True,
            bgcolor="WHITE",
            border=border.all(2, "#C5283D"),
            border_radius=border_radius.all(15),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Row(
                        vertical_alignment=MainAxisAlignment.CENTER,
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ElevatedButton(mensaje.regresarBtn, bgcolor="#cb3234", color="#ffffff", on_click=lambda _:[rutas.animar(self.formulario, self.contenedorInicio, self.contenedorInicio, page), mensaje.cambiarTitulo(page, self.titulo, "Mi Comunidad")]),
                            self.tituloCilindroPropietario,
                            Row(
                                vertical_alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    ElevatedButton("Ver informacion", on_click=lambda _: self.accionBtnFormularioJefeFamiliaVerInfo(page)),
                                    ElevatedButton("Anadir Cilindro", bgcolor="GREEN", color="#ffffff", on_click=lambda _: self.accionBtnFromularioCilindroAnadir(page))
                                ]
                            ),
                        ]
                    ),
                    Container(
                        height=260,
                        bgcolor="WHITE",
                        content=Column(
                            scroll=ScrollMode.ALWAYS,
                            expand=True,
                            controls=[
                               self.tablaCilindros 
                            ]
                        )
                    ),
                    self.tituloCilindroSeleccionado,
                    Container(
                        height=260,
                        bgcolor="WHITE",
                        content=Column(
                            scroll=ScrollMode.ALWAYS,
                            expand=True,
                            controls=[
                               self.tablaPedido
                            ]
                        )
                    ),
                ]
            )
        )

        #CONTENEDOR CENTRAL
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
        self.iniciarGenerarCartas(page)

        return View(
            rutas.routePrincipal,
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
        gestionPrincipal.obtenerWidget(self.formulario, self.nombreJ, self.apellidoJ, self.cedulaJ, self.ubicacionJ, self.telefonoJ, 
        self.correoJ, self.columnaCards, self.tituloAgregarJefes, self.tituloCilindroSeleccionado, self.tituloCilindroPropietario, 
        self.titulo, self.contenedorInicio, self.contenedorReporte, self.contenedorHistorial, self.contenedorPerfilJefe, 
        self.contenedorPerfilLider, self.formularioJefe, self.formularioCilindro, self.contenedorJefeFamilia, self.tablaJornadaPrincipal,
        self.nombreLi, self.apellidoLi, self.cedulaLi, self.ubicacionLi, self.telefonoLi, self.correoLi, self.textoSlider, 
        self.tablaLlenarHistorial, self.tablaSeleccionarHistorial)

    def iniciarGenerarCartas(self, pagee):
        pagee = pagee
        cartasJefesFamilia.volverGenerarCartas(pagee, self.iDLiderCalle, self.tablaPedido, self.tablaCilindros)

    def regresarJefesFamiliaInicio(self, pagee):
        pagee = pagee
        regresarAtras.regresarInicio(pagee, self.nombre, self.apellido, self.cedula, self.cantidadCi, self.numeroTelefono, self.codigoTelefono, self.correo, self.tipoCorreo, self.tipoCedula)

    def regresarJefesFamiliaCilindro(self, pagee):
        pagee = pagee
        regresarAtras.regresarFormularioJefe(pagee, self.cantidadCi)

    def accionBtnFormularioJefeFamilia(self, pagee):
        pagee = pagee
        registrarJefeFamiliaCilindros.validarFormularioJefesFamilia(pagee, self.nombre, self.apellido, self.cedula, self.tipoCedula, self.numeroTelefono, self.correo, self.tipoCorreo, self.codigoTelefono, self.cantidadCi)
    
    def accionBtnFormularioCilindros(self, pagee):
        pagee = pagee
        registrarJefeFamiliaCilindros.abrirAlertConfirmarCilindros(pagee,  self.nombre, self.apellido, self.cedula, self.tipoCedula, self.correo, self.tipoCorreo, self.numeroTelefono, self.codigoTelefono, self.cantidadCi, self.iDLiderCalle, self.tablaPedido, self.tablaCilindros)

    def accionBtnFromularioCilindroAnadir(self, pagee):
        pagee = pagee
        crudCilindros.abrirAnadirCilindro(pagee, self.tablaCilindros, self.tablaPedido)

    def accionBtnFormularioJefeFamiliaVerInfo(self, pagee):
        pagee = pagee
        editarDatosJefeFamilia.cargarDatosJefe(pagee)

    def generarCasillasCilindro(self, pagee):
        pagee = pagee
        registrarJefeFamiliaCilindros.volverGenerarCilindros(pagee, self.columnaContenedor, self.cantidadCi)