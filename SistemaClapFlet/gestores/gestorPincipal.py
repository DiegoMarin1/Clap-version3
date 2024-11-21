from flet import ScrollMode, Container, Text, SnackBar, Dropdown, dropdown, alignment, border_radius, border, TextCapitalization, TextField, CrossAxisAlignment, MainAxisAlignment, Column, FontWeight, TextButton, AlertDialog, padding, TextThemeStyle, DataRow, DataCell, Row, icons, IconButton, ElevatedButton
from controlador.conexion import db
from controlador.rutas import rutas
from controlador.mensajes import mensaje, validaciones
from gestores.gestorLiderPolitico import archivos
from modelo.modelPrincipal import jefeFamiliar, lider, cilindro
from modelo.consultas import consulta
from modelo.modelVista import seccionesEditar, seccionesEditarCompleja
from controlador.cartas import cartas

import modelo.reporte
from modelo.reporte import Pdf

import os
import pathlib
import shutil

from datetime import datetime
from time import sleep

#USADA PARA OBTNER LOS ELEMENTOS QUE NECESITAN LAS OTRAS CLASES

"""class gestorAcciones:
    def __init__(self, page, iDLiderCalle, tablaPedido, tablaCilindros, columnaCards, tituloAgregarJefes):
        self.page = page
        self.iDLiderCalle = iDLiderCalle
        self.tablaPedido = tablaPedido
        self.tablaCilindros = tablaCilindros
        self.columnaCards = columnaCards
        self.tituloAgregarJefes = tituloAgregarJefes

        self.carticas = cartas(page, self.iDLiderCalle, self.tablaPedido, self.tablaCilindros, formularioJefeFamilia.generarJefe, consulta.obtenerInfoJefesFamiliaCartas, gestionPrincipal.cartas)

    def volverGenerarCartas(self):
        if db.consultaConRetorno(consulta.verificarJefesFamiliaCartas, [self.iDLiderCalle,]):
            self.tituloAgregarJefes.visible = False            
            self.columnaCards.controls.clear()
            self.columnaCards.controls = self.carticas.generarCards()
            self.page.update()
        else:
            pass
"""

class gestionPrincipal:
    itemsCilindrosLista = []
    datosCilindrosLista = []
    listaId = []
    cells = []
    listPedido = []
    cartas = []
    jorn = []
    contenido = []
    bitacoraLista = []
    his = []
    
    formulario = None

    columnaCards = None

    #DATOS DEL JEFE DE FAMILIA
    nombreJ = None
    apellidoJ = None
    cedulaJ = None
    ubicacionJ = None
    telefonoJ = None
    correoJ = None

    #DATOS DEL LIDER DE CALLE
    nombreLi = None
    apellidoLi = None
    cedulaLi = None
    ubicacionLi = None
    telefonoLi = None
    correoLi = None

    #TITULOS
    tituloAgregarJefes = None
    tituloCilindroSeleccionado = None
    tituloCilindroPropietario = None
    titulo = None

    #CONTENEDORES
    contenedorInicio = None
    contenedorReporte = None
    contenedorHistorial = None
    contenedorPerfilJefe = None
    contenedorPerfilLider = None
    formularioJefe = None
    formularioCilindro = None
    contenedorJefeFamilia = None

    #TABLAS
    tablaJornadaPrincipal = None
    tablaLlenarHistorial = None
    textoSlider = None

    appbar = None

    def obtenerWidget(formulario, nombre, apellido, cedula, ubicacion, telefono, correo, columnaCards, tituloAgregarJefes, tituloCilindroSeleccionado, 
    tituloCilindroPropietario, titulo, contenedorInicio, contenedorReporte, contenedorHistorial, contenedorPerfilJefe, contenedorPerfilLider, 
    formularioJefe, formularioCilindro, contenedorJefeFamilia, tablaJornadaPrincipal, nombreLi, apellidoLi, cedulaLi, ubicacionLi, telefonoLi, 
    correoLi, textoSlider, tablaLlenarHistorial, tablaSeleccionarHistorial, appbar):
        gestionPrincipal.formulario = formulario

        gestionPrincipal.nombreJ = nombre
        gestionPrincipal.apellidoJ = apellido
        gestionPrincipal.cedulaJ = cedula
        gestionPrincipal.ubicacionJ = ubicacion
        gestionPrincipal.telefonoJ = telefono
        gestionPrincipal.correoJ = correo

        gestionPrincipal.columnaCards = columnaCards

        gestionPrincipal.tituloAgregarJefes = tituloAgregarJefes
        gestionPrincipal.tituloCilindroSeleccionado = tituloCilindroSeleccionado
        gestionPrincipal.tituloCilindroPropietario = tituloCilindroPropietario
        gestionPrincipal.titulo = titulo

        gestionPrincipal.contenedorInicio = contenedorInicio
        gestionPrincipal.contenedorReporte = contenedorReporte
        gestionPrincipal.contenedorHistorial = contenedorHistorial
        gestionPrincipal.contenedorPerfilJefe = contenedorPerfilJefe
        gestionPrincipal.contenedorPerfilLider = contenedorPerfilLider
        gestionPrincipal.formularioJefe = formularioJefe
        gestionPrincipal.formularioCilindro = formularioCilindro
        gestionPrincipal.contenedorJefeFamilia = contenedorJefeFamilia

        gestionPrincipal.tablaJornadaPrincipal = tablaJornadaPrincipal

        gestionPrincipal.nombreLi = nombreLi
        gestionPrincipal.apellidoLi = apellidoLi
        gestionPrincipal.cedulaLi = cedulaLi
        gestionPrincipal.ubicacionLi = ubicacionLi
        gestionPrincipal.telefonoLi = telefonoLi
        gestionPrincipal.correoLi = correoLi

        gestionPrincipal.textoSlider = textoSlider
        gestionPrincipal.tablaLlenarHistorial = tablaLlenarHistorial
        gestionPrincipal.tablaSeleccionarHistorial = tablaSeleccionarHistorial
        gestionPrincipal.appbar = appbar

#GENERAR CARTAS DE JEFES DE FAMILIA Y VER SU CONTENIDO
class cartasJefesFamilia:
    #LIMPIA EL CONTEDOR DE LAS CARTAS
    def volverGenerarCartas(page, iDLiderCalle, tablaPedido, tablaCilindros):
        global carticas
        if db.consultaConRetorno(consulta.verificarJefesFamiliaCartas, [iDLiderCalle,]):
            gestionPrincipal.tituloAgregarJefes.visible = False            
            carticas = cartas(page, iDLiderCalle, tablaPedido, tablaCilindros, formularioJefeFamilia.generarJefe, consulta.obtenerInfoJefesFamiliaCartas, gestionPrincipal.cartas)
            gestionPrincipal.columnaCards.controls.clear()
            gestionPrincipal.columnaCards.controls = carticas.generarCards()
            page.update()
        else:
            pass
    
class formularioJefeFamilia:
    #VER CONTENIDO
    #ESTA FUNCION HACE UNA CONSULTA A LA TABLA PEDIDOS SI RETORNA ALGO SE ACTIVA LA OTRA DATATABLE
    def generarJefe(idJefeFamilia, page, nombre, tablaCilindros, tablaPedido):
        resultadoQuery = db.consultaConRetorno(consulta.obtenerCilindrosJefeFamilia, [idJefeFamilia,])

        tablaCilindros.rows.clear()
        gestionPrincipal.appbar.cambiarTitulo(f"cilindros de {nombre}")
        tablaCilindros.rows = formularioJefeFamilia.mostrarCilindrosJefes(idJefeFamilia, page, nombre, tablaCilindros, tablaPedido)

        if resultadoQuery:
            gestionPrincipal.tituloCilindroSeleccionado.value = "Cilindros Seleccionados"
            tablaPedido.visible = True
            tablaPedido.rows.clear()
            tablaPedido.rows = formularioJefeFamilia.seleccionarPedido(resultadoQuery, page, nombre, tablaCilindros, tablaPedido)
            formularioJefeFamilia.quitarCilindrosRepetidos(page, idJefeFamilia, tablaCilindros)
            page.update()
        else:
            gestionPrincipal.tituloCilindroSeleccionado.value = ""
            tablaPedido.visible = False
            page.update()

        rutas.animar(gestionPrincipal.formulario, gestionPrincipal.contenedorJefeFamilia, gestionPrincipal.contenedorJefeFamilia, page)

        page.update()

    def quitarCilindrosRepetidos(page, idJefeFamilia, tablaCilindros):
        resultadoC = db.consultaConRetorno(consulta.obtenerCilindrosRepetidos, [idJefeFamilia,])

        numFilas = tablaCilindros.rows[:]

        for i in numFilas:
            numFila = numFilas.index(i)
            valor = tablaCilindros.rows[numFila].cells[0].content.value
            for e in resultadoC:
                if valor == f"{e[0]}":
                    tablaCilindros.rows[numFila].visible = False
                    page.update()
                    break

    def mostrarCilindrosJefes(idJefeFamilia, page, nombre, tablaCilindros, tablaPedido):
        global cedulaIdentidad
        cedulaIdentidad = idJefeFamilia

        resultado = db.consultaConRetorno(consulta.mostrarCilindrosJefeFamilia, [idJefeFamilia,])

        for idss, empresa, tamano, pico, fecaRegistrada in resultado:
            gestionPrincipal.cells.append(DataRow(
                color="WHITE",
                cells=[
                    DataCell(Text(f"{idss}")),
                    DataCell(Text(f"{empresa}")),
                    DataCell(Text(f"{tamano}")),
                    DataCell(Text(f"{pico}")),
                    DataCell(Text(f"{fecaRegistrada[:-13]}")),
                    DataCell(Row(controls=[IconButton(icon=icons.EDIT, tooltip="Editar Cilindro", on_click=lambda _, idss=idss: crudCilindros.abrirEditarCilindro(page, idss, nombre, tablaCilindros, tablaPedido)), IconButton(icon=icons.DELETE, tooltip="Eliminar Cilindro", on_click=lambda _, idss=idss: crudCilindros.abrirEliminarCilindro(page, idss, nombre, tablaCilindros, tablaPedido))]))
                ],
                on_select_changed=lambda _, idss=idss: formularioJefeFamilia.seleccionarJornada(idss, idJefeFamilia, page, nombre, tablaCilindros, tablaPedido),
            ),
            )

            page.update()

        return gestionPrincipal.cells

    def seleccionarPedido(contenidoCilindrosJefe, page, nombre, tablaCilindros, tablaPedido):
        for idPedido, ids, empr, tamn, pic in contenidoCilindrosJefe:
            gestionPrincipal.listPedido.append(DataRow(
                color="WHITE",
                cells=[
                    DataCell(Text(f"{ids}")),
                    DataCell(Text(f"{empr}")),
                    DataCell(Text(f"{tamn}")),
                    DataCell(Text(f"{pic}")),
                    DataCell(Row(controls=[IconButton(icon=icons.CANCEL, tooltip="Quitar", on_click=lambda _, idPedido=idPedido: crudCilindros.eliminarJornadaJefe(idPedido, page, nombre, tablaCilindros, tablaPedido))]))
                ],
            ),
            )

            page.update()

        return gestionPrincipal.listPedido

    def seleccionarJornada(idsss, idJefeFamilia, page, nombre, tablaCilindros, tablaPedido):
        fecha = datetime.today().strftime('%d-%m-%Y')
        db.consultaSinRetorno(consulta.guardarCilindrosPedidos, [idsss, fecha])

        formularioJefeFamilia.generarJefe(idJefeFamilia, page, nombre, tablaCilindros, tablaPedido)

        page.snack_bar = SnackBar(bgcolor="GREEN", content=Text("El cilindro fue seleccionado"))
        page.snack_bar.open = True
        page.update()

#FORMULARIO DE JEFES DE FAMILIA Y CILINDROS
class registrarJefeFamiliaCilindros:
    def validarFormularioJefesFamilia(page, nombre, apellido, cedula, tipoCedula, numeroTelefono, correo, tipoCorreo, codigoTelefono, cantidadCi):
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
                validaciones.validarCampos(page, eval(nombreCampo), config["min"])
                todoValido = False
            if "query" in config:
                if bool(validaciones.validarConsultas(page, config["query"], config["param"], config["msj"]) == False):
                    todoValido = False

        if cantidadCi.value == 0:
                cantidadCi.error_text = "Campo vacio, por favor seleccione para continuar"
                page.update()

        if todoValido:
            gestionPrincipal.appbar.cambiarTitulo(f"Datos de Cilindros de {nombre.value} {apellido.value}")
            rutas.animar(gestionPrincipal.formulario, gestionPrincipal.formularioCilindro, gestionPrincipal.formularioCilindro, page)

    #GENERAR EL FORMULARIO DE CILINDROS
    def volverGenerarCilindros(page, widget, cantidadCi):
        widget.controls = registrarJefeFamiliaCilindros.itemsCilindros(page, int(cantidadCi.value))
        page.update()

    def itemsCilindros(page, cantidadCi):
        cantidadCi = cantidadCi + 1
        gestionPrincipal.datosCilindrosLista.clear()
        gestionPrincipal.itemsCilindrosLista.clear()

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

            gestionPrincipal.itemsCilindrosLista.append(
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

            gestionPrincipal.datosCilindrosLista.append([empresa, tamano, pico])

            page.update()
        
        return gestionPrincipal.itemsCilindrosLista

    def abrirAlertConfirmarCilindros(page, nombre, apellido, cedula, tipoCedula, correo, tipoCorreo, numeroTelefono, codigoTelefono, cantidadCi, iDLiderCalle, tablaPedido, tablaCilindros):
        textoConfirmar = Text(f"Estas seguro que desea registrar al jefe de familia {nombre.value} {apellido.value}?")
        nuevoJefe = jefeFamiliar(f"{tipoCedula.value}-{cedula.value}", nombre.value, apellido.value, f"{codigoTelefono.value}-{numeroTelefono.value}", f"{correo.value}{tipoCorreo.value}", True, iDLiderCalle, 1)
        alertConfirmarCilindros = AlertDialog(content=textoConfirmar,
            actions=[TextButton("Confirmar", on_click=lambda _:[registrarJefeFamiliaCilindros.guardarJefe(page, alertConfirmarCilindros, nuevoJefe, cantidadCi, textoConfirmar, tablaPedido, tablaCilindros)]), 
            TextButton("Cancelar", on_click=lambda _:[mensaje.cerrarAlert(page, alertConfirmarCilindros)])]
        )

        page.dialog = alertConfirmarCilindros
        alertConfirmarCilindros.open = True
        nuevoJefe.telefono
        page.update()

    def guardarJefe(page, alert, nuevoJefe, cantidadCi, textoConfirmar, tablaPedido, tablaCilindros):
        alert.actions.clear()
        textoConfirmar.value = "Guardando datos, por favor espere"
        page.update()

        #INSERTAR LOS DATOS DEL LIDER DE FAMILIA
        db.consultaSinRetorno(consulta.guardarJefeFamilia, [nuevoJefe.cedula, nuevoJefe.nombre, nuevoJefe.apellido, nuevoJefe.telefono, nuevoJefe.correo, nuevoJefe.get_liderId()])

        #OBTENER EL ID DEL LIDER DE FAMILIA
        idJefeFamiliar = db.consultaConRetorno(consulta.obtenerIdJefeFamilia, [nuevoJefe.cedula,])

        #CICLO PARA OBTENER LOS IDS
        for empresa, tamano, pico in gestionPrincipal.datosCilindrosLista:
            resultadoIdEmpresa = db.consultaConRetorno(consulta.obtenerIdEmpresa, [empresa.value,])
            resultadoIdEmpresa = resultadoIdEmpresa[0][0]

            resultadoIdTamano = db.consultaConRetorno(consulta.obtenerIdTamano, [tamano.value,])
            resultadoIdTamano = resultadoIdTamano[0][0]

            resultadoIdPico = db.consultaConRetorno(consulta.obtenerIdPico, [pico.value,])
            resultadoIdPico = resultadoIdPico[0][0]

            gestionPrincipal.listaId.append([resultadoIdEmpresa, resultadoIdPico, resultadoIdTamano])

        #GUARDAMOS LOS CILINDROS EN LA BASE DE DATOS
        for empresaId, picoId, tamanoId in gestionPrincipal.listaId:
            fecha = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            fecha = str(fecha)

            db.consultaSinRetorno(consulta.guardarCilindros, [str(empresaId), str(picoId), str(tamanoId), idJefeFamiliar[0][0], str(fecha)])
            sleep(0.1)

        mensaje.cerrarAlert(page, alert)
        gestionPrincipal.appbar.cambiarTitulo("Lideres de Calle")
        regresarAtras.regresarAlInicioCompletado(page, cantidadCi, empresa, pico, tamano, nuevoJefe.get_liderId(), tablaPedido, tablaCilindros)

class crudCilindros:
    #ACCION PARA EJECUTAR EL CRUD
    def abrirEliminarCilindro(page, idCilindro, nombre, tablaCilindros, tablaPedido):

        alertEliminar = AlertDialog(modal=True, content=Text("Seguro que deseas eleminar el cilindro?"), actions=[TextButton("Si", on_click=lambda _: crudCilindros.EliminarCilindro(idCilindro, page, nombre, tablaCilindros, tablaPedido, alertEliminar)), TextButton("No", on_click=lambda _:mensaje.cerrarAlert(page, alertEliminar))])

        page.dialog = alertEliminar
        alertEliminar.open = True

        page.update()

    def abrirAnadirCilindro(page, tablaCilindros, tablaPedido):
        empresaAnadir = Dropdown(hint_text="Seleccionar empresa", height=60, width=240, on_change=lambda _: mensaje.quitarError(page, empresaAnadir))
        tamanoAnadir = Dropdown(hint_text="Seleccionar tamaño", height=60, width=240, on_change=lambda _: mensaje.quitarError(page, tamanoAnadir))
        picoAnadir = Dropdown(hint_text="Seleccionar pico", height=60, width=240, on_change=lambda _: mensaje.quitarError(page, picoAnadir))

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
                        ElevatedButton("Agregar", on_click=lambda _:crudCilindros.anadirCilindro(page, empresaAnadir, tamanoAnadir, picoAnadir, tablaCilindros, tablaPedido, alertAnadir)),
                        ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(page, alertAnadir))
                    ]
                )
            ]
        )

        page.dialog = alertAnadir
        alertAnadir.open = True

        page.update()

    def abrirEditarCilindro(page, ids, nombre, tablaCilindros, tablaPedido):

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
        page.update()

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
                        ElevatedButton("Guardar Cambios", on_click=lambda _:crudCilindros.editarCilindro(page, empresaEdit, tamanoEdit, picoEdit, ids, nombre, tablaCilindros, tablaPedido, alertEditar)),
                        ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(page, alertEditar))
                    ]
                )
            ]
        )

        page.dialog = alertEditar
        alertEditar.open = True

        page.update()
    
    #FUNCIONES QUE SE ENCARGAN DEL CRUD
    def EliminarCilindro(idCilindro, page, nombre, tablaCilindros, tablaPedido, alertEliminar):
        db.consultaSinRetorno(consulta.eliminarCilindro, [idCilindro,])
        mensaje.cerrarAlert(page, alertEliminar)
        formularioJefeFamilia.generarJefe(cedulaIdentidad, page, nombre, tablaCilindros, tablaPedido)

        page.snack_bar = SnackBar(bgcolor="GREEN", content=Text("El cilindro se elimino correctamente"))
        page.snack_bar.open = True

        page.update()

    def anadirCilindro(page, empresa, tamano, pico, tablaCilindros, tablaPedido, alertAnadir):

        if (empresa.value == None) or (tamano.value == None) or (pico.value == None):
            
            for control in (empresa, tamano, pico):
                if not control.value:
                    control.error_text = mensaje.campoFaltante
                    page.update()
            
            else:
                return

        else:
            resultadoIdEmpresa = db.consultaConRetorno(consulta.obtenerIdEmpresa, [empresa.value,])
            resultadoIdTamano = db.consultaConRetorno(consulta.obtenerIdTamano, [tamano.value,])
            resultadoIdPico = db.consultaConRetorno(consulta.obtenerIdPico, [pico.value,])

            fecha = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            db.consultaSinRetorno(consulta.guardarCilindros, [resultadoIdEmpresa[0][0], resultadoIdPico[0][0], resultadoIdTamano[0][0], cedulaIdentidad, fecha])
            mensaje.cerrarAlert(page, alertAnadir)

            nombre = db.consultaConRetorno(consulta.mostrarDatosJefe, [cedulaIdentidad,])

            formularioJefeFamilia.generarJefe(cedulaIdentidad, page, nombre[0][0], tablaCilindros, tablaPedido)

            page.snack_bar = SnackBar(bgcolor="GREEN", content=Text("Se agrego el cilindro correctamente"))
            page.snack_bar.open = True

            page.update()

    def editarCilindro(page, emp, tamn, pic, idsss, nombree, tablaCilindros, tablaPedido, alertEditar):
        resultadoIdEmpresa = db.consultaConRetorno(consulta.obtenerIdEmpresa, [emp.value,])
        resultadoIdTamano = db.consultaConRetorno(consulta.obtenerIdTamano, [tamn.value,])
        resultadoIdPico = db.consultaConRetorno(consulta.obtenerIdPico, [pic.value,])

        db.consultaSinRetorno(consulta.guardarCambioCilindro, [resultadoIdEmpresa[0][0], resultadoIdPico[0][0], resultadoIdTamano[0][0], idsss])
        mensaje.cerrarAlert(page, alertEditar)
        formularioJefeFamilia.generarJefe(cedulaIdentidad, page, nombree, tablaCilindros, tablaPedido)

        page.snack_bar = SnackBar(content=Text(f"se edito el cilindro n{idsss}"), bgcolor="#4CBD49")
        page.snack_bar.open = True

        page.update()

    def eliminarJornadaJefe(idCilindro, page, nombre, tablaCilindros, tablaPedido):
        db.consultaSinRetorno(consulta.eliminarCilindroJornadaJefe, [idCilindro,])

        formularioJefeFamilia.generarJefe(cedulaIdentidad, page, nombre, tablaCilindros, tablaPedido)

        page.update()

class reporteJornada:
    #LIMPIAR EL CONTENEDOR DE LAS JORNADAS
    def volverGenerarJornada(page, iDLiderCalle):
        gestionPrincipal.tablaJornadaPrincipal.rows.clear()
        gestionPrincipal.tablaJornadaPrincipal.rows = reporteJornada.generarJornada(page, iDLiderCalle)
        page.update()

    def generarJornada(page, iDLiderCalle):
        resultado = db.consultaConRetorno(consulta.obtenerReportesPedidos, [iDLiderCalle,])

        for idss, cii, nom, ape, empresa, tamano, pico, fechaAgregado in resultado:
            gestionPrincipal.jorn.append(DataRow(
                color="WHITE",
                cells=[
                    DataCell(Text(f"{cii}")),
                    DataCell(Text(f"{nom}")),
                    DataCell(Text(f"{ape}")),
                    DataCell(Text(f"{empresa}")),
                    DataCell(Text(f"{tamano}")),
                    DataCell(Text(f"{pico}")),
                    DataCell(Text(f"{fechaAgregado}")),
                    DataCell(Row(controls=[IconButton(icon=icons.CANCEL, tooltip="Quitar", on_click=lambda _, idss=idss: reporteJornada.eliminarJornada(idss, page))]))
                ],
            ),
            )

            page.update()

        return gestionPrincipal.jorn

    #REMOVER CILINDROS DE UNA JORNADA
    def eliminarJornada(ids, page):
        db.consultaSinRetorno(consulta.eliminarCilindroJornada, [ids,])

        reporteJornada.volverGenerarJornada(page, mensaje.datosUsuarioLista[0][0])

        page.update()

    #ACCION BTN
    def confirmarReporte(page, indicator):
        textoEspera = Text("Estas seguro que deseas generar el reporte final?. La planilla se vaciara")

        alertJornada = AlertDialog(content=textoEspera,
            actions=[TextButton("Generar", on_click=lambda _: reporteJornada.abrirJornada(page, alertJornada, indicator, textoEspera)), TextButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(page, alertJornada))]
        )

        page.dialog = alertJornada
        alertJornada.open = True

        page.update()
        
    #ESTA FUNCION COMPRUEBA ALGUNAS CONDICIONES PARA GENERAR EL PDF
    def abrirJornada(page, alertJornada, indicator, textoEspera):
        fecha = datetime.today().strftime('%d-%m-%Y')

        if db.consultaConRetorno(consulta.verificarPedidos, [mensaje.datosUsuarioLista[0][0],]):
            if db.consultaConRetorno(consulta.verificarGeneracion, [mensaje.datosUsuarioLista[0][0], fecha]):
                mensaje.cerrarAlert(page, alertJornada)
                page.snack_bar = SnackBar(content=Text("Solo puedes generar un Reporte por Dia"))
                page.snack_bar.open = True
                page.update()
            else:
                alertJornada.actions.clear()
                textoEspera.value = "Generando Pdf, por favor espere"
                page.update()
                instancia = Pdf()
                mensaje.cerrarAlert(page, alertJornada)
                rutas.animar(gestionPrincipal.formulario, gestionPrincipal.contenedorInicio, gestionPrincipal.contenedorInicio, page)
                mensaje.cambiarPagina(indicator, 5.5)
                page.snack_bar = SnackBar(content=Text("Informe generado correctamente en la carpeta Reportas del escritorio"), bgcolor="GREEN")
                page.snack_bar.open = True
                page.update()
        else:
            mensaje.cerrarAlert(page, alertJornada)
            page.snack_bar = SnackBar(content=Text("No puedes generar el reporte sin agregar a jefes de familia a la jornada"))
            page.snack_bar.open = True
            page.update()

class historial:
    def abrirHistorial(page, fechaa, idss):
        gestionPrincipal.tablaLlenarHistorial.rows.clear()
        gestionPrincipal.tablaLlenarHistorial.rows = historial.llenarHistroial(page, idss)

        alertHistorial = AlertDialog(
            content=Column(
                controls=[
                    Text(f"Jornada realizada el {fechaa}"),
                    Container(
                        bgcolor="white",
                        height=550,
                        border_radius=border_radius.all(7),  
                        content=Column(
                            expand=True,
                            height=550,
                            scroll=ScrollMode.ALWAYS,
                            controls=[
                                gestionPrincipal.tablaLlenarHistorial,
                            ]
                        )
                    ),
                ]
            ),
            actions=[ElevatedButton("Descargar Pdf", on_click=lambda _:archivoPdf.descargarArchivo(page, alertHistorial, idss)), ElevatedButton("Regresar", on_click=lambda _:mensaje.cerrarAlert(page, alertHistorial))]
        )

        page.dialog = alertHistorial
        alertHistorial.open = True

        page.update()

    def llenarHistroial(page, ids):
        resultado = db.consultaConRetorno(consulta.obtenerHistorial, [ids,])

        for idss, cii, nom, ape, empresa, tamano, pico, fech in resultado:
            gestionPrincipal.contenido.append(DataRow(
                color="WHITE",
                cells=[
                    DataCell(Text(f"{cii}")),
                    DataCell(Text(f"{nom}")),
                    DataCell(Text(f"{ape}")),
                    DataCell(Text(f"{empresa}")),
                    DataCell(Text(f"{tamano}")),
                    DataCell(Text(f"{pico}")),
                    DataCell(Text(f"{fech}")),
                ],
            ),
            )

            page.update()

        return gestionPrincipal.contenido

class archivoPdf:
    #LIMPIAN LOS CONTENEDORES ANTES DE CARGAR LA INFORAMCION
    def volverGenerarArchivos(page):
        archivos.volverGenerarArchivos(page, consulta.obtenerIdArchivos, mensaje.datosUsuarioLista[0][0], gestionPrincipal.tablaSeleccionarHistorial, historial.abrirHistorial)

class editarDatosJefeFamilia:
    #MOSTRAR LOS DATOS DE LOS JEFES
    def cargarDatosJefe(page):
        global datosJefeFamilia
        resultado = db.consultaConRetorno(consulta.mostrarDatosJefe, [cedulaIdentidad,])
        datosJefeFamilia = jefeFamiliar(resultado[0][2], resultado[0][0], resultado[0][1], resultado[0][3], resultado[0][4], resultado[0][5], resultado[0][6], resultado[0][7])

        gestionPrincipal.nombreJ.value = f"{datosJefeFamilia.nombre}"
        gestionPrincipal.apellidoJ.value = f"{datosJefeFamilia.apellido}"
        gestionPrincipal.cedulaJ.value = f"{datosJefeFamilia.cedula}"
        gestionPrincipal.telefonoJ.value = f"{datosJefeFamilia.telefono}"
        gestionPrincipal.correoJ.value = f"{datosJefeFamilia.correo}"
        gestionPrincipal.ubicacionJ.value = f"{datosJefeFamilia.ubicacion}"

        rutas.animar(gestionPrincipal.formulario, gestionPrincipal.contenedorPerfilJefe, gestionPrincipal.contenedorPerfilJefe, page)
    
        page.update()

    def ejecutarEdicionSencilla(objeto, consulta):
        objeto(consulta, cedulaIdentidad)

    def ejecutarEdicionCompleja(consultaVerificar, consultaGuardar, objeto):
        objeto(consultaVerificar, consultaGuardar, cedulaIdentidad)

class editarDatosLiderCalle:
    def cargarDatosLider(page):
        global datosLiderCalle
        resultado = db.consultaConRetorno(consulta.mostrarDatosLider, [mensaje.datosUsuarioLista[0][0],])
        datosLiderCalle = lider(resultado[0][2], resultado[0][0], resultado[0][1], resultado[0][3], resultado[0][4], resultado[0][5], resultado[0][6], resultado[0][7], resultado[0][8], resultado[0][9], resultado[0][10], resultado[0][11])

        gestionPrincipal.nombreLi.value = datosLiderCalle.nombre
        gestionPrincipal.apellidoLi.value = datosLiderCalle.apellido
        gestionPrincipal.cedulaLi.value = datosLiderCalle.cedula
        gestionPrincipal.telefonoLi.value = datosLiderCalle.telefono
        gestionPrincipal.correoLi.value = datosLiderCalle.correo
        gestionPrincipal.ubicacionLi.value = datosLiderCalle.ubicacion

        page.update()

class regresarAtras:

    #RETRODECER EN FORMULARIOS
    def regresarInicio(page, nombre, apellido, cedula, cantidadCi, numeroTelefono, codigoTelefono, correo, tipoCorreo, tipoCedula):
        nombre.value = ""
        apellido.value = ""
        cedula.value = ""
        cantidadCi.value = 0
        numeroTelefono.value = ""
        codigoTelefono.value = None
        correo.value = ""
        tipoCorreo.value = None
        tipoCedula.value = "V"

        gestionPrincipal.appbar.cambiarTitulo("Lideres de calle")
        rutas.animar(gestionPrincipal.formulario, gestionPrincipal.contenedorInicio, gestionPrincipal.contenedorInicio, page)

        page.update()

    def regresarFormularioJefe(page, cantidadCi):
        cantidadCi.value = 0
        
        gestionPrincipal.datosCilindrosLista.clear()
        gestionPrincipal.itemsCilindrosLista.clear()

        rutas.animar(gestionPrincipal.formulario, gestionPrincipal.formularioJefe, gestionPrincipal.formularioJefe, page)

        page.update()

    #ARREGLAR ESTO
    def regresarAlInicioCompletado(page, cantidadCi, empresa, pico, tamano, iDLiderCalle, tablaPedido, tablaCilindros):
        gestionPrincipal.nombreJ.value = ""
        gestionPrincipal.apellidoJ.value = ""
        gestionPrincipal.cedulaJ.value = ""
        cantidadCi.value = None
        gestionPrincipal.telefonoJ.value = ""
        #gestionPrincipal.codigoTelefono.value = None
        gestionPrincipal.correoJ.value = ""
        #gestionPrincipal.tipoCorreo.value = None
        #gestionPrincipal.value = "V"

        gestionPrincipal.itemsCilindrosLista.clear()
        gestionPrincipal.datosCilindrosLista.clear()

        cantidadCi.value = 0

        gestionPrincipal.listaId.clear()

        gestionPrincipal.cartas.clear()
        cartasJefesFamilia.volverGenerarCartas(page, iDLiderCalle, tablaPedido, tablaCilindros)

        rutas.animar(gestionPrincipal.formulario, gestionPrincipal.contenedorInicio, gestionPrincipal.contenedorInicio, page)

    