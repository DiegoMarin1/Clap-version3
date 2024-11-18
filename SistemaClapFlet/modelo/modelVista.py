from flet import *
from flet import Container, border_radius, Column, CrossAxisAlignment, Stack, FontWeight, Page
from controlador.conexion import db
from datetime import datetime
from controlador.mensajes import mensaje
from modelo.consultas import consulta

"""class slider:
    def __init__(self, page):
        self.page = page

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
#                                               Text(mensaje.bienvenida, weight=FontWeight.W_500, color="WHITE"),
                                                self.textoSlider,
                                            ]
                                        )
                                    ),

                                    Container(
                                        margin=margin.only(top=50),
                                        padding=padding.only(left=35),
                                        data=0,
 #                                       on_click=lambda e: [rutas.animar(self.formulario, self.contenedorInicio, self.contenedorInicio, page), mensaje.cambiarPagina(self.indicator, 5.5), mensaje.cambiarTitulo(page, self.titulo, "Mi Comunidad")],
                                        content=Row(
                                            controls=[
                                                Icon(name=icons.HOME),
#                                                Text(mensaje.inicio)
                                            ]
                                        )
                                    ),

                                    Container(
                                        margin=margin.only(top=20),
                                        padding=padding.only(left=35),
                                        data=0,
#                                        on_click=lambda e: [rutas.animar(self.formulario, self.contenedorReporte, self.contenedorReporte, page), mensaje.cambiarPagina(self.indicator, 6.8), reporteJornada.volverGenerarJornada(page, self.iDLiderCalle), mensaje.cambiarTitulo(page, self.titulo, "Administrador de Jornada")],
                                        content=Row(
                                            controls=[
                                                Icon(name=icons.EDIT_NOTE),
#                                                Text(mensaje.reporte)
                                            ]
                                        )
                                    ),
                                    Container(
                                        margin=margin.only(top=20),
                                        padding=padding.only(left=35),
                                        data=0,
 #                                       on_click=lambda e: [rutas.animar(self.formulario, self.contenedorHistorial, self.contenedorHistorial, page), mensaje.cambiarPagina(self.indicator, 8.2), archivoPdf.volverGenerarArchivos(page), mensaje.cambiarTitulo(page, self.titulo, "Historial de jornadas")],
                                        content=Row(
                                            controls=[
                                                Icon(name=icons.EVENT_NOTE),
#                                                Text(mensaje.historial)
                                            ]
                                        )
                                    ),
                                    Container(
                                        margin=margin.only(top=20),
                                        padding=padding.only(left=35),
                                        data=0,
 #                                       on_click=lambda e: [rutas.animar(self.formulario, self.contenedorPerfilLider, self.contenedorPerfilLider, page), editarDatosLiderCalle.cargarDatosLider(page), mensaje.cambiarPagina(self.indicator, 9.5), mensaje.cambiarTitulo(page, self.titulo, "Mis datos")],
                                        content=Row(
                                            controls=[
                                                Icon(name=icons.PEOPLE),
  #                                              Text(mensaje.perfil)
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
"""
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

class cartas:
    def __init__(self, page, iDLiderCalle, tablaPedido, tablaCilindros, funcion, consulta, lista):
        self.page = page
        self.iDLiderCalle = iDLiderCalle
        self.tablaPedido = tablaPedido
        self.tablaCilindros = tablaCilindros
        self.funcion = funcion
        self.consulta = consulta
        self.lista = lista

    def generarCards(self):
        for ids, nom, ape, ci in db.consultaConRetorno(self.consulta, [self.iDLiderCalle,]):
            self.lista.append(
                Container(
                    bgcolor="RED",
                    height=150,
                    width=250,
                    padding=padding.all(7),
                    border_radius=border_radius.all(20),
                    on_click=lambda _, ids=ids, nom=nom: self.funcion(ids, self.page, nom, self.tablaCilindros, self.tablaPedido), 
                    content=Column(
                        controls=[
                            Text(f"{nom} {ape}", style=TextThemeStyle.TITLE_LARGE, color="WHITE"),
                            Text(f"{ci}", style=TextThemeStyle.TITLE_MEDIUM, color="WHITE"),
                        ]
                    )
                )
            )
            self.page.update()
        return self.lista