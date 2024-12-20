from flet import *
from flet import AlertDialog,  MainAxisAlignment, Alignment, TextTheme, PopupMenuButton, PopupMenuItem, MainAxisAlignment, AlertDialog, alignment, TextThemeStyle, PopupMenuButton, PopupMenuItem, CircleAvatar, Icon, icons, margin, Text, Offset, Row, UserControl, padding, Container, border_radius, Column, CrossAxisAlignment, Stack, FontWeight, Page
from controlador.conexion import db
from datetime import datetime
from controlador.mensajes import mensaje
from modelo.consultas import consulta
from controlador.rutas import rutas

class encabezado(UserControl):
    def __init__(self, page:Page):
        super().__init__()
        self.page = page
        self.punto1 = Container(
                                                        height=20,
                                                        width=20,
                                                        border_radius=border_radius.all(50),
                                                        bgcolor="blue"
                                                    )
        self.punto2 = Container(
                                                        height=20,
                                                        width=20,
                                                        border_radius=border_radius.all(50),
                                                        bgcolor="white"
                                                    )
        self.punto3 = Container(
                                                        height=20,
                                                        width=20,
                                                        border_radius=border_radius.all(50),
                                                        bgcolor="white"
                                                    )
        self.encabezado = Container(
                        height=150,
                        alignment=alignment.center,
                        content=Row(
                            alignment=MainAxisAlignment.CENTER,
                            spacing=0,
                            controls=[
                                Stack(
                                    controls=[
                                        Container(
                                            width=50, 
                                            height=50, 
                                            bgcolor="white", 
                                            border_radius=border_radius.all(50),
                                            content=Column(
                                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                                alignment=MainAxisAlignment.CENTER,
                                                controls=[
                                                    self.punto1,
                                                ]
                                            )
                                        )
                                    ]
                                ),
                                Container(width=70, height=8, bgcolor="white"),
                                Stack(
                                    controls=[
                                        Container(
                                            width=50, 
                                            height=50, 
                                            bgcolor="white", 
                                            border_radius=border_radius.all(50),
                                            content=Column(
                                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                                alignment=MainAxisAlignment.CENTER,
                                                controls=[
                                                    self.punto2,
                                                ]
                                            )
                                        )
                                    ]
                                ),
                                Container(width=80, height=8, bgcolor="white"),
                                Stack(
                                    controls=[
                                        Container(
                                            width=50, 
                                            height=50, 
                                            bgcolor="white", 
                                            border_radius=border_radius.all(50),
                                            content=Column(
                                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                                alignment=MainAxisAlignment.CENTER,
                                                controls=[
                                                    self.punto3,
                                                ]
                                            )
                                        )
                                    ]
                                ),
                            ]
                        )
                    )

    def cambiarColor(self, azul, blanco, white):
        azul.bgcolor = "blue"
        blanco.bgcolor = "white"
        white.bgcolor = "white"

        self.update()


class seccionesEditar(UserControl):
    def __init__(self, page:Page, entry):
        super().__init__()
        self.page = page
        self.entry = entry
        self.listaBotones = []
        self.row = Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        self.listaBotones
                    ]
                )
        self.alert = AlertDialog(
            content=Container(
                alignment=alignment.center,
                height=150,
                width=300,
                bgcolor="white",
                content=Row(
                    spacing=10,
                    controls=[
                        self.entry,
                    ]
                )
            ),
            actions=[
                self.row
            ]
        )
    
    def pasarBoton(self, boton):
        self.row.controls = boton
        self.update()

class seccionesEditarCompleja(UserControl):
    def __init__(self, page:Page, entry, entry2):
        super().__init__()
        self.page = page
        self.entry = entry
        self.entry2 = entry2
        self.listaBotones = []
        self.row = Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        self.listaBotones
                    ]
                )
        self.alert = AlertDialog(
            content=Container(
                alignment=alignment.center,
                height=150,
                width=300,
                bgcolor="white",
                content=Row(
                    spacing=10,
                    controls=[
                        self.entry,
                        self.entry2
                    ]
                )
            ),
            actions=[
                self.row
            ]
        )
    
    def pasarBoton(self, boton):
        self.row.controls = boton
        self.update()

class sliderBase(UserControl):
    def __init__(self, page:Page, indicador, formulario):
        super().__init__()
        self.page = page
        self.indicador = indicador
        self.formulario = formulario
        self.textoSlider = Text("", weight=FontWeight.W_500, color="WHITE")
        self.columna = Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=10,
                        )

    def build(self):
        return Container(
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
                                    self.indicador
                                ]
                            ),
                            self.columna
                        ]
                    )
                ]
            )
        )    
    
    def cambiarNombreSlider(self, nombre):
        self.textoSlider.value = f"{nombre}"
        self.update()

    def contruirPrincipal(self, contenedorInicio, appbar, contenedorReporte, funcionReporte, iDLiderCalle, contenedorHistorial, funcionHistorial, contenedorPerfilLider, funcionPerfil, instancia):
        self.columna.controls = [
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
                                        on_click=lambda e: [rutas.animar(self.formulario, contenedorInicio, contenedorInicio, self.page), mensaje.cambiarPagina(self.indicador, 5.5), appbar.cambiarTitulo("Mi Comunidad")],
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
                                        on_click=lambda e: [rutas.animar(self.formulario, contenedorReporte, contenedorReporte, self.page), mensaje.cambiarPagina(self.indicador, 6.8), funcionReporte(self.page, iDLiderCalle), appbar.cambiarTitulo("Administrador de Jornada")],
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
                                        on_click=lambda e: [rutas.animar(self.formulario, contenedorHistorial, contenedorHistorial, self.page), mensaje.cambiarPagina(self.indicador, 8.2), funcionHistorial(instancia), appbar.cambiarTitulo("Historial de jornadas")],
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
                                        on_click=lambda e: [rutas.animar(self.formulario, contenedorPerfilLider, contenedorPerfilLider, self.page), funcionPerfil(self.page), mensaje.cambiarPagina(self.indicador, 9.5), appbar.cambiarTitulo("Mis datos")],
                                        content=Row(
                                            controls=[
                                                Icon(name=icons.PEOPLE),
                                                Text(mensaje.perfil)
                                            ]
                                        )
                                    ),
                                ]
        self.update()

    def contruirLiderCalle(self, contenedorInicio, contenedorBombonas, contenedorPerfil, appbar, funcionPerfil, contrasena):
        self.columna.controls = [Column(
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
                                        on_click=lambda e: [rutas.animar(self.formulario, contenedorInicio, contenedorInicio, self.page), mensaje.cambiarPagina(self.indicador, 5.5), appbar.cambiarTitulo("Lideres de Calle")],
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
                                        on_click=lambda e: [rutas.animar(self.formulario, contenedorBombonas, contenedorBombonas, self.page), mensaje.cambiarPagina(self.indicador, 6.8), appbar.cambiarTitulo("Gestion de Bombonas")],
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
                                        on_click=lambda e: [rutas.animar(self.formulario, contenedorPerfil, contenedorPerfil, self.page), mensaje.cambiarPagina(self.indicador, 8.2), appbar.cambiarTitulo("Tu Perfil"), funcionPerfil(self.page, contrasena)],
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
    
class appBar(UserControl):
    def __init__(self, page:Page, indicador, logo):
        super().__init__()
        self.page = page
        self.indicador = indicador
        self.logo = logo
        self.titulo = Text("", style=TextThemeStyle.TITLE_LARGE, color="white")

    def build(self):
        return Container(
            bgcolor="#C5283D",
            border_radius=border_radius.all(15),
            height=100,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Container(padding=padding.only(left=10), content=self.logo),
                    self.titulo,
                    PopupMenuButton(items=[PopupMenuItem(text="Cerrar Seccion", on_click=lambda _: self.salirVentana())])
                ]
            )
        )

    def cambiarTitulo(self, titulo):
        self.titulo.value = titulo
        self.update()

    def salirVentana(self):
        self.fechaS = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        db.consultaSinRetorno(consulta.guardarSalidaBitacora, [self.fechaS, mensaje.datosUsuarioLista[0][5], mensaje.datosUsuarioLista[0][4]])
        self.page.go("/")
        mensaje.cambiarPagina(self.indicador, 5.5)
        mensaje.datosUsuarioLista.clear()