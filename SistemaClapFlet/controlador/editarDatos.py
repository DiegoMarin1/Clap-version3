from flet import *
from flet import TextOnlyInputFilter, TextCapitalization, TextField, dropdown, Dropdown, NumbersOnlyInputFilter, InputFilter, ElevatedButton, SnackBar, Text
from modelo.modelVista import seccionesEditar, seccionesEditarCompleja
from controlador.mensajes import mensaje, validaciones
from controlador.conexion import db
from modelo.consultas import consulta


class editarDatosUsuario:
    def __init__(self, page, valor, slider, funcion):
        self.page = page
        self.valor = valor
        self.slider = slider
        self.funcion = funcion

        self.entryNombre = TextField(label="Nombre", hint_text=mensaje.minimoCaracteres(3), max_length=12, capitalization=TextCapitalization.SENTENCES, border_radius=30, border_color="#820000", width=300, height=60, input_filter=TextOnlyInputFilter(),on_change=lambda _:mensaje.quitarError(self.page, self.entryNombre))
        self.entryApellido = TextField(label="Apellido", hint_text=mensaje.minimoCaracteres(4), max_length=12, capitalization=TextCapitalization.SENTENCES, border_radius=30, border_color="#820000", width=300, height=60, input_filter=TextOnlyInputFilter(), on_change=lambda _:mensaje.quitarError(self.page, self.entryApellido))
        self.selectTipoTelefono = Dropdown(hint_text="Codigo", color="black",border_color="#820000", border_radius=20, width=100, height=60, on_change=lambda _: mensaje.quitarError(self.page, self.selectTipoTelefono), options=[
                dropdown.Option("0412"), dropdown.Option("0414"), dropdown.Option("0416"), dropdown.Option("0424"), dropdown.Option("0238")])
        self.entryTelefono = TextField(label="N telefono", hint_text="0000000", border_color="#820000", border_radius=20, width=180, height=60, max_length=7, input_filter=NumbersOnlyInputFilter(), on_change=lambda _: mensaje.quitarError(self.page, self.entryTelefono))
        self.selectTipoCorreo = Dropdown(hint_text="Correo", color="black",border_color="#820000", border_radius=20, width=120, height=60, on_change=lambda _: mensaje.quitarError(self.page, self.selectTipoCorreo), options=[
                dropdown.Option("@gmail.com"), dropdown.Option("@hotmail.com")])
        self.entryCorreo = TextField(label="Direccion", hint_text="ej: clapcamoruco", border_color="#820000", border_radius=20, width=180, height=60, input_filter=InputFilter(regex_string=validaciones.condicionAlfanum), on_change=lambda _:mensaje.quitarError(self.page, self.entryCorreo))

    def editNombre(self, query, identificador):
        self.entryNombre.value = self.valor.value
        alertEditNombre = seccionesEditar(self.page, self.entryNombre)
        alertEditNombre.pasarBoton([ElevatedButton("Guardar Cambios", on_click=lambda _:self.ValidarEdicionSencilla(alertEditNombre.entry, alertEditNombre.alert, 3, query, self.funcion, mensaje.nombreEditadoFinal, True, identificador)), ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(self.page, alertEditNombre.alert))])

        self.page.dialog = alertEditNombre.alert
        alertEditNombre.alert.open = True

        self.page.update()
    
    def editApellido(self, query, identificador):
        self.entryApellido.value = self.valor.value
        alertEditApellido = seccionesEditar(self.page, self.entryApellido)
        alertEditApellido.pasarBoton([ElevatedButton("Guardar Cambios", on_click=lambda _:self.ValidarEdicionSencilla(alertEditApellido.entry, alertEditApellido.alert, 4, query, self.funcion, mensaje.apellidoEditadoFinal, False, identificador)), ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(self.page, alertEditApellido.alert))])

        self.page.dialog = alertEditApellido.alert
        alertEditApellido.alert.open = True

        self.page.update()

    def editTelefono(self, queryVerificar, queryGuardar, identificador):
        codigo = self.valor.value[:4]
        telefono = self.valor.value[-7:]

        self.selectTipoTelefono.value = codigo        
        self.entryTelefono.value = telefono

        alertEditTelefono = seccionesEditarCompleja(self.page, self.selectTipoTelefono, self.entryTelefono)
        alertEditTelefono.pasarBoton([ElevatedButton("Guardar Cambios", on_click=lambda _:self.validarEdicionCompleja(alertEditTelefono.entry, alertEditTelefono.entry2, alertEditTelefono.alert, mensaje.telefonoInvalido, queryVerificar, mensaje.telefonoRegistrado, queryGuardar, self.funcion, mensaje.telefonoGuardado, 7, True, identificador)), ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(self.page, alertEditTelefono.alert))])

        self.page.dialog = alertEditTelefono.alert
        alertEditTelefono.alert.open = True

        self.page.update()

    def editCorreo(self, queryVerficar, queryGuardar, identificador):
        if self.valor.value[-10:] == "@gmail.com":
            direccion = self.valor.value[:-10]
            tipo = self.valor.value[-10:]
        else:
            direccion = self.valor.value[:-12]
            tipo = self.valor.value[-12:]

        self.entryCorreo.value = direccion
        self.selectTipoCorreo.value = tipo

        alertEditCorreo = seccionesEditarCompleja(self.page, self.entryCorreo, self.selectTipoCorreo)
        alertEditCorreo.pasarBoton([ElevatedButton("Guardar Cambios", on_click=lambda _:self.validarEdicionCompleja(alertEditCorreo.entry2, alertEditCorreo.entry, alertEditCorreo.alert, mensaje.correoInvalido, queryVerficar, mensaje.correoRegistrado, queryGuardar, self.funcion, mensaje.correoGuardado, 3, False, identificador)), ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(self.page, alertEditCorreo.alert))])

        self.page.dialog = alertEditCorreo.alert
        alertEditCorreo.alert.open = True

        self.page.update()

    def ValidarEdicionSencilla(self, widget, alertEdicion, rango, query, funcion, mensajeFinal, condicion, identificador):
        if not (widget.value) or (len(widget.value) in range(1, rango)):
            if not widget.value:
                widget.error_text = mensaje.campoFaltante
            if len(widget.value) in range(1, rango):
                widget.error_text = mensaje.minimoCaracteres(rango)
                self.page.update()
        else:
            db.consultaSinRetorno(query, [widget.value, identificador])
            if condicion == True:
                self.slider.value = f"{widget.value}"
            funcion(self.page)
            mensaje.cerrarAlert(self.page, alertEdicion)
            self.page.snack_bar = SnackBar(bgcolor="GREEN", content=Text(mensajeFinal))
            self.page.snack_bar.open = True
            self.page.update()

    def validarEdicionCompleja(self, campo1, campo2, alertEdicion, mensajeInvalido, query, mensajeRepetido, queryGuardar, funcion, mensajeFinal, rango, condicion, identificador):
        #TRUE PARA TELEFONO
        if condicion == True:
            arreglo = f"{campo1.value}-{campo2.value}"
        #FALSE PARA CORREO
        if condicion == False:
            arreglo = f"{campo2.value}{campo1.value}"
        if  not (campo2.value) or (len(campo2.value) < rango):
            if not campo2.value:
                campo2.error_text = mensaje.campoFaltante
                self.page.update()
            if len(campo2.value) < rango:
                campo2.error_text = mensajeInvalido
                self.page.update()
        elif db.consultaConRetorno(query, [arreglo,]):
            self.page.snack_bar = SnackBar(content=Text(mensajeRepetido))
            self.page.snack_bar.open = True
            self.page.update()
        
        else:
            db.consultaSinRetorno(queryGuardar, [arreglo, identificador])
            funcion(self.page)
            mensaje.cerrarAlert(self.page, alertEdicion)
            self.page.snack_bar = SnackBar(bgcolor="GREEN", content=Text(mensajeFinal))
            self.page.snack_bar.open = True
            self.page.update()
        self.page.update()