from flet import *
from flet import View,Image, colors, Container, Text, SnackBar, Dropdown, dropdown, alignment, border_radius, border, TextCapitalization, TextField, CrossAxisAlignment, MainAxisAlignment, Column, FontWeight, TextButton, AlertDialog, padding, TextThemeStyle, DataRow, DataCell, Row, icons, IconButton, ElevatedButton
from flet_route import Params, Basket

from time import sleep
from datetime import datetime
from gestores.gestorLogin import gestionLogin
from controlador.mensajes import mensaje
from controlador.rutas import rutas
from controlador.conexion import db
from modelo.consultas import consulta

class login:
    def __init__(self):
        #LOGO
        self.logo = Image(src=rf"{rutas.rutaActualArreglada}\img\clap.png")

    def view(self, page:Page, params:Params, basket:Basket):
        #CAPTURAR EL EVENTO DE CIERRE DE VENTANA
        def window_event(e):
            if e.data == "close":
                if bool(mensaje.datosUsuarioLista) == True:
                    fechaS = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    db.consultaSinRetorno(consulta.guardarSalidaBitacora, [fechaS, mensaje.datosUsuarioLista[0][5], mensaje.datosUsuarioLista[0][4]])
                    page.window.destroy()
                else:
                    page.window.destroy()

        #CARACTERISTICAS DE LA VENTANA
        page.window.prevent_close = True
        page.window.on_event =  window_event
        page.window_maximizable = False
        page.title = "CLAP"
        page.window_resizable = False
        page.window_height = "725"
        page.window_width = "500"
        page.window_center()
        page.window_bgcolor = colors.TRANSPARENT
        page.bgcolor = colors.TRANSPARENT
        sleep(1)
        page.window_visible = True

        #WIDGETS
        self.usuario = TextField(hint_text=mensaje.ingresaUsuario, label="Usuario", border_radius=30, border_color="#820000", prefix_icon=icons.PERSON, width=300, height=60, on_change=lambda _: mensaje.quitarError(page, self.usuario))
        self.contrasena = TextField(hint_text=mensaje.ingresaContrasena, label="Contraseña", border_radius=30, border_color="#820000", prefix_icon=icons.LOCK, password=True, can_reveal_password=True, width=300, height=60, on_change=lambda _: mensaje.quitarError(page, self.contrasena))
        self.text_recuperar = TextButton(mensaje.recuperarContrasena, on_click=lambda _: rutas.enrutamiento(page, rutas.routeRecuperar))
        self.iniciar_sesion = ElevatedButton(mensaje.inicioSeccion, width=300, bgcolor="#cb3234", color="#ffffff", on_click=lambda _:gestionLogin.camposVacios(page, self.usuario, self.contrasena))
        self.registrarTxt = Text(mensaje.registrate)
        self.registrarBtn =  TextButton(mensaje.crearCuenta, on_click=lambda _: rutas.enrutamiento(page, rutas.routeRegistrar))
        self.derechos_autor = Text(mensaje.derechosAutores, size=15)

        #CONTENIDO DE LA PAGINA
        self.body = Container(
            height=690,
            width=500,
            bgcolor="#820000",
            border_radius=50,
            content=Column(
                controls=[
                    Container(
                        height=150,
                        alignment=alignment.center,
                        content=self.logo
                    ),

                    Container(
                        bgcolor="white",
                        height=550,
                        width=500,
                        border_radius=border_radius.only(top_left=50, bottom_left=50, bottom_right=50),
                        padding=padding.all(30),
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                Column(
                                    spacing=20,
                                    controls=[self.usuario,self.contrasena,]
                                ),
                                self.text_recuperar,
                                self.iniciar_sesion,
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[self.registrarTxt, self.registrarBtn]
                                ),
                                self.derechos_autor
                            ]
                        )
                    )
                ]
            )
        )

        return View(
            "/",
            horizontal_alignment="center",
            vertical_alignment="center",
            padding=0,
            bgcolor="transparent",
            controls=[
                self.body,
            ]
        )
