from flet import *
from flet import View, Stack, AnimatedSwitcher, AnimatedSwitcherTransition, AnimationCurve, Container, Text, SnackBar, Dropdown, dropdown, alignment, border_radius, border, TextCapitalization, TextField, CrossAxisAlignment, MainAxisAlignment, Column, FontWeight, TextButton, AlertDialog, padding, TextThemeStyle, DataRow, DataCell, Row, icons, IconButton, ElevatedButton

from flet_route import Params, Basket
from gestores.gestorRecuperar import *
from gestores.gestorRecuperar import gestionRecuperar
from controlador.mensajes import mensaje, validaciones
from modelo.modelVista import encabezado
from controlador.rutas import rutas

class recuperar:
    def __init__(self):
        #RUTA
        self.route = "/"

    def view(self, page:Page, params:Params, basket:Basket):
        #TEXTFLIEDS
        self.tipoCedula = Dropdown(label="Tipo", color="black",border_color="#820000", border_radius=20, width=100, height=60, on_change=lambda _: mensaje.quitarError(page, self.tipoCedula), options=[
                dropdown.Option("V"), dropdown.Option("E")])
        self.tipoCedula.value = "V"
        self.cedula = TextField(label="Cedula", hint_text=mensaje.minimoCaracteres(7), border_color="#820000", border_radius=20, width=180, height=60, max_length=8, on_change=lambda _: [mensaje.quitarError(page, self.cedula), validaciones.validarCamposNot(self.cedula, page, True, validaciones.condicionNumeros)])
        self.pregunta = Text("", style=TextThemeStyle.TITLE_MEDIUM)
        self.respuesta = TextField(hint_text="Escriba su respuesta", capitalization=TextCapitalization.SENTENCES, label="Respuesta", border_radius=30, border_color="#820000", width=280, height=60, on_change=lambda _:[mensaje.quitarError(page, self.respuesta), validaciones.validarCamposNot(self.respuesta, page, False, validaciones.condicionNombres)])
        self.contrasena = TextField(hint_text=mensaje.minimoCaracteres(6), label="Contraseña", border_radius=30, border_color="#820000", prefix_icon=icons.LOCK, width=280, height=60, max_length=12, on_change=lambda _:[mensaje.quitarError(page, self.contrasena), validaciones.validarCamposIn(self.contrasena, page, validaciones.condicionEspacios)])
        self.confimarContrasena = TextField(hint_text="Confirmar contraseña", label="Confirmar", border_radius=30, border_color="#820000", prefix_icon=icons.LOCK, width=280, height=60, on_change=lambda _:[mensaje.quitarError(page, self.confimarContrasena), validaciones.validarCamposIn(self.confimarContrasena, page, validaciones.condicionEspacios)])

        page.title = "CLAP"
        page.window_resizable = False
        page.window_maximizable = False
        #CONTENEDORES
        self.encabezado = encabezado(page)
        self.containerCedula = Container(
            height=725,
            width=500,
            content=Column(
                controls=[   
                    self.encabezado.encabezado,
                    Container(
                        bgcolor="white",
                        height=550,
                        width=500,
                        border_radius=border_radius.only(top_left=50),
                        padding=padding.all(30),
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            spacing=20,
                            controls=[
                                Text("Identificación", style=TextThemeStyle.TITLE_LARGE),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=1,
                                    controls=[
                                        self.tipoCedula,
                                        self.cedula,
                                    ]
                                ),
                                ElevatedButton("Siguiente", width=300, bgcolor="#cb3234", color="#ffffff", on_click=lambda _: self.gestionar1(page, self.containerCedula, self.containerRespuesta)),
                                ElevatedButton("Atras", bgcolor="#cb3234", color="#ffffff", on_click=lambda _: rutas.enrutamiento(page, rutas.routeLogin))
                            ]
                        )
                    )
                ]
            )
        )

        self.containerRespuesta = Container(
            height=725,
            width=500,
            content=Column(
                controls=[
                    self.encabezado.encabezado,
                    Container(
                        bgcolor="white",
                        height=550,
                        width=500,
                        border_radius=border_radius.only(top_left=50),
                        padding=padding.all(30),
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            spacing=20,
                            controls=[
                                Text("Pregunta de seguridad", style=TextThemeStyle.TITLE_LARGE),
                                self.pregunta,
                                self.respuesta,
                                ElevatedButton("Siguiente", width=300, bgcolor="#cb3234", color="#ffffff", on_click=lambda _: self.gestionar2(page, self.containerRespuesta, self.containerContrasena)),
                                ElevatedButton("Atras", bgcolor="#cb3234", color="#ffffff", on_click=lambda _: self.regresar1(page, self.containerRespuesta, self.containerCedula))
                            ]
                        )
                    )
                ]
            )
        )

        self.containerContrasena = Container(
            height=725,
            width=500,
            content=Column(
                controls=[
                    self.encabezado.encabezado,
                    Container(
                        bgcolor="white",
                        height=550,
                        width=500,
                        border_radius=border_radius.only(top_left=50),
                        padding=padding.all(30),
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            spacing=20,
                            controls=[
                                Text("Asignar Nueva Contraseña", style=TextThemeStyle.TITLE_LARGE),
                                self.contrasena,
                                self.confimarContrasena,
                                ElevatedButton("Guardar", width=300, bgcolor="#cb3234", color="#ffffff", on_click=lambda _: self.gestionar3(page)),
                                ElevatedButton("Atras", bgcolor="#cb3234", color="#ffffff", on_click=lambda _: self.regresar2(page, self.containerContrasena, self.containerRespuesta))
                            ]
                        )
                    )
                ]
            )
        )

        self.formulario = AnimatedSwitcher(
            self.containerCedula,
            expand=True, 
            transition=AnimatedSwitcherTransition.FADE,
            duration=500,
            reverse_duration=100,
            switch_in_curve=AnimationCurve.BOUNCE_OUT,
            switch_out_curve=AnimationCurve.BOUNCE_IN
        )


        return View(
            "/recuperar",
            horizontal_alignment="center",
            vertical_alignment="center",
            padding=0,
            bgcolor="#820000",
            controls=[
                self.formulario
            ]
        )

    def gestionar1(self, pagee, contenedor1, contenedor2):
        pagee = pagee
        contenedor1 = contenedor1
        contenedor2 = contenedor2
        gestionRecuperar.formulario1(pagee, self.tipoCedula, self.cedula, self.pregunta, self.formulario, contenedor1, contenedor2, self.encabezado)
        

    def gestionar2(self, pagee, contenedor1, contenedor2):
        pagee = pagee
        contenedor1 = contenedor1
        contenedor2 = contenedor2
        gestionRecuperar.formulario2(pagee, self.tipoCedula, self.cedula, self.respuesta, self.formulario, contenedor1, contenedor2, self.encabezado)

    def gestionar3(self, pagee):
        pagee = pagee
        gestionRecuperar.formulario3(pagee, self.tipoCedula, self.cedula, self.contrasena, self.confimarContrasena)

    def regresar1(self, pagee, contenedor1, contenedor2):
        pagee = pagee
        contenedor1 = contenedor1
        contenedor2 = contenedor2
        self.encabezado.cambiarColor(self.encabezado.punto1, self.encabezado.punto2, self.encabezado.punto3)
        gestionRecuperar.regresarF1(pagee, self.formulario, contenedor1, contenedor2)

    def regresar2(self, pagee, contenedor1, contenedor2):
        pagee = pagee
        contenedor1 = contenedor1
        contenedor2 = contenedor2
        self.encabezado.cambiarColor(self.encabezado.punto2, self.encabezado.punto1, self.encabezado.punto3)
        gestionRecuperar.regresarF2(pagee, self.formulario, contenedor1, contenedor2)
