from flet import *
from flet import View, Stack, AnimatedSwitcher, AnimatedSwitcherTransition, AnimationCurve, ScrollMode, Container, Text, SnackBar, Dropdown, dropdown, alignment, border_radius, border, TextCapitalization, TextField, CrossAxisAlignment, MainAxisAlignment, Column, FontWeight, TextButton, AlertDialog, padding, TextThemeStyle, DataRow, DataCell, Row, icons, IconButton, ElevatedButton

from flet_route import Params, Basket
from controlador.rutas import rutas
from controlador.mensajes import mensaje, validaciones
from gestores.gestorRegister import *
from gestores.gestorRegister import gestionRegister

from controlador.mensajes import mensaje

#EL ESTATUS 1 ES HABILITADO
#EL ESTATUS 2 ES INHABILITADO

class register:
    def __init__(self):
        self.route = "/"

    def view(self, page:Page, params:Params, basket:Basket):

        page.title = "CLAP"
        page.window_resizable = False
        page.window_maximizable = False

        #WIDGET
        self.usuario = TextField(label="Usuario", hint_text=mensaje.minimoCaracteres(5), max_length=10, border_color="#820000", border_radius=20, prefix_icon=icons.PERSON, width=280, height=60, on_change=lambda _: [mensaje.quitarError(page, self.usuario), validaciones.validarCamposIn(self.usuario, page, validaciones.condicionEspacios)])
        self.contrasena = TextField(label="Contrasena", hint_text=mensaje.minimoCaracteres(6), max_length=12, border_color="#820000", border_radius=20, prefix_icon=icons.LOCK, width=280, height=60, on_change=lambda _: [mensaje.quitarError(page, self.contrasena), validaciones.validarCamposIn(self.contrasena, page, validaciones.condicionEspacios)])
        self.confirmarContrasena = TextField(hint_text="Confirmar Contrasena", border_color="#820000", border_radius=20, prefix_icon=icons.LOCK, width=280, height=60, on_change=lambda _: [mensaje.quitarError(page, self.confirmarContrasena), validaciones.validarCamposIn(self.confirmarContrasena, page, validaciones.condicionEspacios)])
        self.nombre = TextField(label="Nombre", hint_text=mensaje.minimoCaracteres(3), max_length=12, capitalization=TextCapitalization.SENTENCES, border_color="#820000", border_radius=20, width=140, height=60, on_change=lambda _: [mensaje.quitarError(page, self.nombre), validaciones.validarCamposNot(self.nombre, page, False, validaciones.condicionNombres)])
        self.apellido = TextField(label="Apellido", hint_text=mensaje.minimoCaracteres(4), max_length=12, capitalization=TextCapitalization.SENTENCES, border_color="#820000", border_radius=20, width=140, height=60, on_change=lambda _: [mensaje.quitarError(page, self.apellido), validaciones.validarCamposNot(self.apellido, page, False, validaciones.condicionNombres)])
        
        self.tipoCedula = Dropdown(label="Tipo", color="black",border_color="#820000", border_radius=20, width=100, height=60, on_change=lambda _: mensaje.quitarError(page, self.tipoCedula), options=[
                dropdown.Option("V"), dropdown.Option("E")])
        self.tipoCedula.value = "V"
        self.cedula = TextField(label="Cedula", hint_text=mensaje.minimoCaracteres(7), border_color="#820000", border_radius=20, width=180, height=60, max_length=8, on_change=lambda _: [mensaje.quitarError(page, self.cedula), validaciones.validarCamposNot(self.cedula, page, True, validaciones.condicionNumeros)])
        
        self.codigoTelefono = Dropdown(hint_text="Codigo", color="black",border_color="#820000", border_radius=20, width=100, height=60, on_change=lambda _: mensaje.quitarError(page, self.codigoTelefono), options=[
                dropdown.Option("0412"), dropdown.Option("0414"), dropdown.Option("0416"), dropdown.Option("0424"), dropdown.Option("0238")])
        self.numeroTelefono = TextField(label="N telefono", hint_text="0000000", border_color="#820000", border_radius=20, width=180, height=60, max_length=7, on_change=lambda _: [mensaje.quitarError(page, self.numeroTelefono), validaciones.validarCamposNot(self.numeroTelefono, page, True, validaciones.condicionNumeros)])
        self.correo = TextField(label="Direccion", hint_text="ej: clapcamoruco", border_color="#820000", border_radius=20, width=180, height=60, on_change=lambda _: [mensaje.quitarError(page, self.correo), validaciones.validarCamposIn(self.correo, page, validaciones.condicinCorreo)])
        self.tipoCorreo = Dropdown(hint_text="Correo", color="black",border_color="#820000", border_radius=20, width=120, height=60, on_change=lambda _: mensaje.quitarError(page, self.tipoCorreo), options=[
                dropdown.Option("@gmail.com"), dropdown.Option("@hotmail.com"), dropdown.Option("@outlook.com")])

        self.ubicacion = TextField(label="Ingresa tu ubicacion", hint_text="Ej : Camoruco v12", max_length=30, border_color="#820000", border_radius=20, capitalization=TextCapitalization.SENTENCES, width=280, height=60, on_change=lambda _: [mensaje.quitarError(page, self.ubicacion), validaciones.validarCamposNot(self.ubicacion ,page, True, validaciones.condicionAlfanumericos)])

        self.pregunta = Dropdown(hint_text="Elegir Pregunta de Seguridad", color="black",border_color="#820000", border_radius=20, width=280, height=60, on_change=lambda _: mensaje.quitarError(page, self.pregunta))
        self.respuesta = TextField(label="Respuesta", hint_text=mensaje.minimoCaracteres(3), max_length=20, capitalization=TextCapitalization.SENTENCES, border_color="#820000", border_radius=20, width=280, height=60, on_change=lambda _: [mensaje.quitarError(page, self.respuesta), validaciones.validarCamposNot(self.respuesta, page, False, validaciones.condicionNombres)])
        self.nivelUser = Dropdown(hint_text="Cargo", color="black",border_color="#820000", border_radius=20, width=280, height=60, on_change=lambda _: mensaje.quitarError(page, self.nivelUser), options=[
                dropdown.Option("Lider de Calle"), dropdown.Option("Lider Politico")])

        #LLENAR COMBO DE PREGUNTAS
        gestionRegister.llenarPreguntas(self.pregunta)
        
        #CONTENEDORES
        self.contenedorLider = Container(
            height=725,
            width=500,
            border_radius=50,
            bgcolor="#820000",
            content=Column(
                controls=[
                    Container(
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
                                                    Container(
                                                        height=20,
                                                        width=20,
                                                        border_radius=border_radius.all(50),
                                                        bgcolor="blue"
                                                    )
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
                                                    Container(
                                                        height=20,
                                                        width=20,
                                                        border_radius=border_radius.all(50),
                                                        bgcolor="white"
                                                    )
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
                                                    Container(
                                                        height=20,
                                                        width=20,
                                                        border_radius=border_radius.all(50),
                                                        bgcolor="white"
                                                    )
                                                ]
                                            )
                                        )
                                    ]
                                ),
                            ]
                        )
                    ),

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
                                Text("Datos Personales", style=TextThemeStyle.TITLE_LARGE),
                                Container(
                                    height=350,
                                    content=Column(
                                        spacing=20,
                                        height=350,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        width=480,
                                        scroll=ScrollMode.ALWAYS,
                                        controls=[
                                            Row(
                                                alignment=MainAxisAlignment.CENTER,
                                                controls=[
                                                    self.nombre,
                                                    self.apellido,
                                                ]
                                            ),
                                            Row(
                                                alignment=MainAxisAlignment.CENTER,
                                                spacing=1,
                                                controls=[
                                                    self.tipoCedula,
                                                    self.cedula,
                                                ]
                                            ),
                                            self.nivelUser,
                                            self.ubicacion,
                                            Text("Numero de telefono"),
                                            Row(
                                                alignment=MainAxisAlignment.CENTER,
                                                spacing=1,
                                                controls=[
                                                    self.codigoTelefono,
                                                    self.numeroTelefono,
                                                ]
                                            ),
                                            Text("Correo electronico"),
                                            Row(
                                                alignment=MainAxisAlignment.CENTER,
                                                spacing=1,
                                                controls=[
                                                    self.correo,
                                                    self.tipoCorreo,
                                                ]
                                            ),
                                        ]
                                    )    
                                ),
                                ElevatedButton("Siguiente", width=300, bgcolor="#cb3234", color="#ffffff", on_click=lambda _: self.gestionar1(page, self.contenedorLider, self.contenedorUsuario)),
                                ElevatedButton("Salir", bgcolor="#cb3234", color="#ffffff", on_click=lambda _: rutas.enrutamiento(page, rutas.routeLogin))
                            ]
                        )
                    )
                ]
            )
        )

        self.contenedorUsuario = Container(
            height=725,
            width=500,
            border_radius=50,
            bgcolor="#820000",
            content=Column(
                controls=[
                    Container(
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
                                                    Container(
                                                        height=20,
                                                        width=20,
                                                        border_radius=border_radius.all(50),
                                                        bgcolor="white"
                                                    )
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
                                                    Container(
                                                        height=20,
                                                        width=20,
                                                        border_radius=border_radius.all(50),
                                                        bgcolor="blue"
                                                    )
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
                                                    Container(
                                                        height=20,
                                                        width=20,
                                                        border_radius=border_radius.all(50),
                                                        bgcolor="white"
                                                    )
                                                ]
                                            )
                                        )
                                    ]
                                ),
                            ]
                        )
                    ),

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
                                Text("Usuario y Contraseña", style=TextThemeStyle.TITLE_LARGE),
                                self.usuario,
                                self.contrasena,
                                self.confirmarContrasena,
                                ElevatedButton("Siguiente", width=300, bgcolor="#cb3234", color="#ffffff", on_click=lambda _: self.gestionar2(page, self.contenedorUsuario, self.contenedorPregunta)),
                                ElevatedButton("Regresar", bgcolor="#cb3234", color="#ffffff", on_click=lambda _: self.regresar1(page, self.contenedorUsuario, self.contenedorLider))
                                
                            ]
                        )
                    )
                ]
            )
        )

        self.contenedorPregunta = Container(
            height=725,
            width=500,
            border_radius=50,
            bgcolor="#820000",
            content=Column(
                controls=[
                    Container(
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
                                                    Container(
                                                        height=20,
                                                        width=20,
                                                        border_radius=border_radius.all(50),
                                                        bgcolor="white"
                                                    )
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
                                                    Container(
                                                        height=20,
                                                        width=20,
                                                        border_radius=border_radius.all(50),
                                                        bgcolor="white"
                                                    )
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
                                                    Container(
                                                        height=20,
                                                        width=20,
                                                        border_radius=border_radius.all(50),
                                                        bgcolor="blue"
                                                    )
                                                ]
                                            )
                                        )
                                    ]
                                ),
                            ]
                        )
                    ),

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
                                Text("Pregunta de Seguridad", style=TextThemeStyle.TITLE_LARGE),
                                self.pregunta,
                                self.respuesta,
                                ElevatedButton("Siguiente", width=300, bgcolor="#cb3234", color="#ffffff", on_click=lambda _: self.gestionar3(page)),
                                ElevatedButton("Regresar", bgcolor="#cb3234", color="#ffffff", on_click=lambda _: self.regresar2(page, self.contenedorPregunta, self.contenedorUsuario))
                                
                            ]
                        )
                    )
                ]
            )
        )

        self.formulario = AnimatedSwitcher(
            self.contenedorLider,
            expand=True, 
            transition=AnimatedSwitcherTransition.FADE,
            duration=500,
            reverse_duration=100,
            switch_in_curve=AnimationCurve.BOUNCE_OUT,
            switch_out_curve=AnimationCurve.BOUNCE_IN
        )

        return View(
            "/register",
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="transparent",
            padding=0,
            controls=[
                self.formulario
            ]
        )

    def gestionar1(self, pagee, contenedor1, contenedor2):
        pagee = pagee
        contenedor1 = contenedor1
        contenedor2 = contenedor2
        gestionRegister.formulario1(pagee, self.nombre, self.apellido, self.cedula, self.numeroTelefono, self.correo, self.ubicacion, self.nivelUser, self.tipoCorreo, self.codigoTelefono, self.tipoCedula, self.formulario, contenedor1, contenedor2)
        

    def gestionar2(self, pagee, contenedor1, contenedor2):
        pagee = pagee
        contenedor1 = contenedor1
        contenedor2 = contenedor2
        gestionRegister.formulario2(pagee, self.usuario, self.contrasena, self.confirmarContrasena, self.formulario, contenedor1, contenedor2, self.nivelUser)

    def gestionar3(self, pagee):
        pagee = pagee
        gestionRegister.formulario3(pagee, self.pregunta, self.respuesta)

    def regresar1(self, pagee, contenedor1, contenedor2):
        pagee = pagee
        contenedor1 = contenedor1
        contenedor2 = contenedor2
        gestionRegister.regresarF1(pagee, self.formulario, contenedor1, contenedor2)

    def regresar2(self, pagee, contenedor1, contenedor2):
        pagee = pagee
        contenedor1 = contenedor1
        contenedor2 = contenedor2
        gestionRegister.regresarF2(pagee, self.formulario, contenedor1, contenedor2)    