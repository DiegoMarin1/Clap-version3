from flet import *
from flet import dropdown, Dropdown, border_radius, border, Column, CrossAxisAlignment, FontWeight, Text, AlertDialog, TextButton
from modelo.consultas import consulta
from controlador.mensajes import mensaje, validaciones
from controlador.rutas import rutas
from controlador.conexion import db
from modelo.modelPrincipal import jefeFamiliar

from datetime import datetime
from time import sleep

from gestores.gestorPincipal import regresarAtras

class registrarJefeFamiliaCilindros:
    def __init__(self, page, appbar, formulario, formularioCilindro, tablaPedido, tablaCilindros, columnaContenedor):
        self.page = page
        self.appbar = appbar
        self.formulario = formulario
        self.formularioCilindro = formularioCilindro
        self.tablaPedido = tablaPedido
        self.tablaCilindros = tablaCilindros
        self.columnaContenedor = columnaContenedor

        self.itemsCilindrosLista = []
        self.datosCilindrosLista = []
        self.listaId = []

    def validarFormularioJefesFamilia(self, nombre, apellido, cedula, tipoCedula, numeroTelefono, correo, tipoCorreo, codigoTelefono, cantidadCi):
        arregloCedula = f"{tipoCedula.value}-{cedula.value}"
        arregloCorreo = f"{correo.value}{tipoCorreo.value}"
        arregloTelefono = f"{codigoTelefono.value}-{numeroTelefono.value}"

        listaCondicion = {
            "nombre" : {"min": 3},
            "apellido" : {"min": 4},
            "cedula" : {"min":7, "query":consulta.verificarCedulaJefesFamilia, "param":[arregloCedula,], "msj":f"Esta cedula ya esta registrada"},
            "numeroTelefono" : {"min":7, "query":consulta.verificarTelefonoJefesFamilia, "param":[arregloTelefono,], "msj":"Este numero de telefono ya esta asignado a un usuario"},
            "correo" : {"min":3, "query":consulta.verificarCorreoJefesFamilia, "param":[arregloCorreo,], "msj":mensaje.correoRegistrado},
            "tipoCorreo" : {"min":4},
            "codigoTelefono" : {"min":4},
            "cantidadCi": {"min":1}
        }

        todoValido = True

        for nombreCampo, config in listaCondicion.items():
            if not (eval(nombreCampo).value) or (len(eval(nombreCampo).value) < config["min"]):
                validaciones.validarCampos(self.page, eval(nombreCampo), config["min"])
                todoValido = False
            if "query" in config:
                if bool(validaciones.validarConsultas(self.page, config["query"], config["param"], config["msj"]) == False):
                    todoValido = False

        if cantidadCi.value == 0:
                cantidadCi.error_text = "Campo vacio, por favor seleccione para continuar"
                self.page.update()

        if todoValido:
            self.appbar.cambiarTitulo(f"Datos de Cilindros de {nombre.value} {apellido.value}")
            rutas.animar(self.formulario, self.formularioCilindro, self.formularioCilindro, self.page)

    #GENERAR EL FORMULARIO DE CILINDROS
    def volverGenerarCilindros(self, cantidadCi):
        self.columnaContenedor.controls = self.itemsCilindros(int(cantidadCi.value))
        self.page.update()

    def itemsCilindros(self, cantidadCi):
        cantidadCi = cantidadCi + 1
        self.datosCilindrosLista.clear()
        self.itemsCilindrosLista.clear()

        for formularioIndividual in range(1, cantidadCi):

            empresa = Dropdown(hint_text="Seleccionar empresa", height=60, width=130)
            tamano = Dropdown(hint_text="Seleccionar tamaño", height=60, width=130)
            pico = Dropdown(hint_text="Seleccionar pico", height=60, width=130)
            
            for emp in db.consultaConRetorno(consulta.obtenerEmpresas):
                empresa.options.append(dropdown.Option(emp[0]))

            
            for tam in db.consultaConRetorno(consulta.obtenerTamanos):
                tamano.options.append(dropdown.Option(tam[0]))


            for pic in db.consultaConRetorno(consulta.obtenerPicos):
                pico.options.append(dropdown.Option(pic[0]))

            empresa.value = "Radelco"
            tamano.value = "Pequeña"
            pico.value = "Presion"

            self.itemsCilindrosLista.append(
                Container(
                    height=250,
                    border_radius=border_radius.all(15),
                    width=150,
                    bgcolor="WHITE",
                    border=border.all(2, "#C5283D"),
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=0,
                        controls=[
                            Text(f"Cilindro {str(formularioIndividual)}", weight=FontWeight.W_500,),
                            Text("Empresa:", size=10, weight=FontWeight.W_900),
                            empresa,
                            Text("Tamaño:", size=10, weight=FontWeight.W_900),
                            tamano,
                            Text("Pico:", size=10, weight=FontWeight.W_900),
                            pico
                        ]
                    )
                )
            )

            self.datosCilindrosLista.append([empresa, tamano, pico])

            self.page.update()
        
        return self.itemsCilindrosLista

    def abrirAlertConfirmarCilindros(self, nombre, apellido, cedula, tipoCedula, correo, tipoCorreo, numeroTelefono, codigoTelefono, cantidadCi, iDLiderCalle):
        textoConfirmar = Text(f"Estas seguro que desea registrar al jefe de familia {nombre.value} {apellido.value}?")
        nuevoJefe = jefeFamiliar(f"{tipoCedula.value}-{cedula.value}", nombre.value, apellido.value, f"{codigoTelefono.value}-{numeroTelefono.value}", f"{correo.value}{tipoCorreo.value}", True, iDLiderCalle, 1)
        alertConfirmarCilindros = AlertDialog(content=textoConfirmar,
            actions=[TextButton("Confirmar", on_click=lambda _:self.guardarJefe(alertConfirmarCilindros, nuevoJefe, cantidadCi, textoConfirmar)), 
            TextButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(self.page, alertConfirmarCilindros))]
        )

        self.page.dialog = alertConfirmarCilindros
        alertConfirmarCilindros.open = True
        nuevoJefe.telefono
        self.page.update()

    def guardarJefe(self, alert, nuevoJefe, cantidadCi, textoConfirmar):
        alert.actions.clear()
        textoConfirmar.value = "Guardando datos, por favor espere"
        self.page.update()

        #INSERTAR LOS DATOS DEL LIDER DE FAMILIA
        db.consultaSinRetorno(consulta.guardarJefeFamilia, [nuevoJefe.cedula, nuevoJefe.nombre, nuevoJefe.apellido, nuevoJefe.telefono, nuevoJefe.correo, nuevoJefe.get_liderId()])

        #OBTENER EL ID DEL LIDER DE FAMILIA
        idJefeFamiliar = db.consultaConRetorno(consulta.obtenerIdJefeFamilia, [nuevoJefe.cedula,])

        #CICLO PARA OBTENER LOS IDS
        for empresa, tamano, pico in self.datosCilindrosLista:
            resultadoIdEmpresa = db.consultaConRetorno(consulta.obtenerIdEmpresa, [empresa.value,])
            resultadoIdEmpresa = resultadoIdEmpresa[0][0]

            resultadoIdTamano = db.consultaConRetorno(consulta.obtenerIdTamano, [tamano.value,])
            resultadoIdTamano = resultadoIdTamano[0][0]

            resultadoIdPico = db.consultaConRetorno(consulta.obtenerIdPico, [pico.value,])
            resultadoIdPico = resultadoIdPico[0][0]

            self.listaId.append([resultadoIdEmpresa, resultadoIdPico, resultadoIdTamano])

        #GUARDAMOS LOS CILINDROS EN LA BASE DE DATOS
        for empresaId, picoId, tamanoId in self.listaId:
            fecha = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            fecha = str(fecha)

            db.consultaSinRetorno(consulta.guardarCilindros, [str(empresaId), str(picoId), str(tamanoId), idJefeFamiliar[0][0], str(fecha)])
            sleep(0.1)

        mensaje.cerrarAlert(self.page, alert)
        self.appbar.cambiarTitulo("Lideres de Calle")
        regresarAtras.regresarAlInicioCompletado(self.page, cantidadCi, empresa, pico, tamano, nuevoJefe.get_liderId(), self.tablaPedido, self.tablaCilindros)