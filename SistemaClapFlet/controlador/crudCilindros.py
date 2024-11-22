from flet import *
from flet import Text, AlertDialog, TextButton, Dropdown, dropdown, Column, CrossAxisAlignment, MainAxisAlignment, Row, ElevatedButton, SnackBar
from datetime import datetime
from controlador.conexion import db
from controlador.mensajes import mensaje, validaciones
from gestores.gestorPincipal import formularioJefeFamilia
from modelo.consultas import consulta

class crudCilindros:
    def __init__(self, page, tablaCilindros, tablaPedido):
        self.page = page
        self.tablaCilindros = tablaCilindros
        self.tablaPedido = tablaPedido

    #ACCION PARA EJECUTAR EL CRUD
    def abrirEliminarCilindro(self, idCilindro, nombre, cedulaIdentidad):

        alertEliminar = AlertDialog(modal=True, content=Text("Seguro que deseas eleminar el cilindro?"), actions=[TextButton("Si", on_click=lambda _: self.EliminarCilindro(idCilindro, nombre, alertEliminar, cedulaIdentidad)), TextButton("No", on_click=lambda _:mensaje.cerrarAlert(self.page, alertEliminar))])

        self.page.dialog = alertEliminar
        alertEliminar.open = True

        self.page.update()

    def abrirAnadirCilindro(self, cedulaIdentidad):
        empresaAnadir = Dropdown(hint_text="Seleccionar empresa", height=60, width=240, on_change=lambda _: mensaje.quitarError(self.page, empresaAnadir))
        tamanoAnadir = Dropdown(hint_text="Seleccionar tamaño", height=60, width=240, on_change=lambda _: mensaje.quitarError(self.page, tamanoAnadir))
        picoAnadir = Dropdown(hint_text="Seleccionar pico", height=60, width=240, on_change=lambda _: mensaje.quitarError(self.page, picoAnadir))

        for emp in db.consultaConRetorno(consulta.obtenerEmpresas):
            empresaAnadir.options.append(dropdown.Option(emp[0]))
            
        for tam in db.consultaConRetorno(consulta.obtenerTamanos):
            tamanoAnadir.options.append(dropdown.Option(tam[0]))

        for pic in db.consultaConRetorno(consulta.obtenerPicos):
            picoAnadir.options.append(dropdown.Option(pic[0]))

        alertAnadir = AlertDialog(
            content=Container(
                height=300,
                width=150,
                bgcolor="white",
                content=Column(
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    spacing=10,
                    controls=[
                        empresaAnadir,
                        tamanoAnadir,
                        picoAnadir
                    ]
                )
            ),
            actions=[
                Row(
                    controls=[
                        ElevatedButton("Agregar", on_click=lambda _:self.anadirCilindro(empresaAnadir, tamanoAnadir, picoAnadir, alertAnadir, cedulaIdentidad)),
                        ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(self.page, alertAnadir))
                    ]
                )
            ]
        )

        self.page.dialog = alertAnadir
        alertAnadir.open = True

        self.page.update()

    def abrirEditarCilindro(self, ids, nombre, cedulaIdentidad):

        empresaEdit = Dropdown(hint_text="Seleccionar empresa", height=60, width=240)
        tamanoEdit = Dropdown(hint_text="Seleccionar tamaño", height=60, width=240)
        picoEdit = Dropdown(hint_text="Seleccionar pico", height=60, width=240)

        for emp in db.consultaConRetorno(consulta.obtenerEmpresas):
            empresaEdit.options.append(dropdown.Option(emp[0]))
            
        for tam in db.consultaConRetorno(consulta.obtenerTamanos):
            tamanoEdit.options.append(dropdown.Option(tam[0]))

        for pic in db.consultaConRetorno(consulta.obtenerPicos):
            picoEdit.options.append(dropdown.Option(pic[0]))

        resultadoGeneral = db.consultaConRetorno(consulta.editarCilindro, [ids,])

        empresaV = resultadoGeneral[0][0]
        tamanoV = resultadoGeneral[0][1]
        picoV = resultadoGeneral[0][2]

        #SELECCIONAR EMPRESA
        empresaEdit.value = empresaV
        #SELECCIONAR TAMANO
        tamanoEdit.value = tamanoV
        #SELECCIONAR PICO   
        picoEdit.value = picoV
        self.page.update()

        alertEditar = AlertDialog(
            content=Container(
                height=250,
                width=150,
                bgcolor="white",
                content=Column(
                    spacing=10,
                    controls=[
                        empresaEdit,
                        tamanoEdit,
                        picoEdit
                    ]
                )
            ),
            actions=[
                Row(
                    controls=[
                        ElevatedButton("Guardar Cambios", on_click=lambda _:self.editarCilindro(empresaEdit, tamanoEdit, picoEdit, ids, nombre, alertEditar, cedulaIdentidad)),
                        ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(self.page, alertEditar))
                    ]
                )
            ]
        )

        self.page.dialog = alertEditar
        alertEditar.open = True

        self.page.update()
    
    #FUNCIONES QUE SE ENCARGAN DEL CRUD
    def EliminarCilindro(self, idCilindro, nombre, alertEliminar, cedulaIdentidad):
        db.consultaSinRetorno(consulta.eliminarCilindro, [idCilindro,])
        mensaje.cerrarAlert(self.page, alertEliminar)
        formularioJefeFamilia.generarJefe(cedulaIdentidad, self.page, nombre, self.tablaCilindros, self.tablaPedido)

        self.page.snack_bar = SnackBar(bgcolor="GREEN", content=Text("El cilindro se elimino correctamente"))
        self.page.snack_bar.open = True

        self.page.update()

    def anadirCilindro(self, empresa, tamano, pico, alertAnadir, cedulaIdentidad):

        if (empresa.value == None) or (tamano.value == None) or (pico.value == None): 
            for control in (empresa, tamano, pico):
                if not control.value:
                    control.error_text = mensaje.campoFaltante
                    self.page.update()
            else:
                return
        else:
            resultadoIdEmpresa = db.consultaConRetorno(consulta.obtenerIdEmpresa, [empresa.value,])
            resultadoIdTamano = db.consultaConRetorno(consulta.obtenerIdTamano, [tamano.value,])
            resultadoIdPico = db.consultaConRetorno(consulta.obtenerIdPico, [pico.value,])

            fecha = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            db.consultaSinRetorno(consulta.guardarCilindros, [resultadoIdEmpresa[0][0], resultadoIdPico[0][0], resultadoIdTamano[0][0], cedulaIdentidad, fecha])
            mensaje.cerrarAlert(self.page, alertAnadir)

            nombre = db.consultaConRetorno(consulta.mostrarDatosJefe, [cedulaIdentidad,])

            formularioJefeFamilia.generarJefe(cedulaIdentidad, self.page, nombre[0][0], self.tablaCilindros, self.tablaPedido)

            self.page.snack_bar = SnackBar(bgcolor="GREEN", content=Text("Se agrego el cilindro correctamente"))
            self.page.snack_bar.open = True

            self.page.update()

    def editarCilindro(self, emp, tamn, pic, idsss, nombree, alertEditar, cedulaIdentidad):
        resultadoIdEmpresa = db.consultaConRetorno(consulta.obtenerIdEmpresa, [emp.value,])
        resultadoIdTamano = db.consultaConRetorno(consulta.obtenerIdTamano, [tamn.value,])
        resultadoIdPico = db.consultaConRetorno(consulta.obtenerIdPico, [pic.value,])

        db.consultaSinRetorno(consulta.guardarCambioCilindro, [resultadoIdEmpresa[0][0], resultadoIdPico[0][0], resultadoIdTamano[0][0], idsss])
        mensaje.cerrarAlert(self.page, alertEditar)
        formularioJefeFamilia.generarJefe(cedulaIdentidad, self.page, nombree, self.tablaCilindros, self.tablaPedido)

        self.page.snack_bar = SnackBar(content=Text(f"se edito el cilindro n{idsss}"), bgcolor="#4CBD49")
        self.page.snack_bar.open = True

        self.page.update()

    def eliminarJornadaJefe(self, idCilindro, nombre, cedulaIdentidad):
        db.consultaSinRetorno(consulta.eliminarCilindroJornadaJefe, [idCilindro,])

        formularioJefeFamilia.generarJefe(cedulaIdentidad, self.page, nombre, self.tablaCilindros, self.tablaPedido)

        self.page.update()