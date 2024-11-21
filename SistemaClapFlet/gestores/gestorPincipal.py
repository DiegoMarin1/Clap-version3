from flet import  Container, Text, SnackBar, Dropdown, dropdown, border_radius, border, CrossAxisAlignment, Column, FontWeight, TextButton, AlertDialog, DataRow, DataCell, Row, icons, IconButton
from controlador.conexion import db
from controlador.rutas import rutas
from controlador.mensajes import mensaje, validaciones
from modelo.modelPrincipal import jefeFamiliar, lider, cilindro
from modelo.consultas import consulta
from controlador.cartas import cartas
#from controlador.crudCilindros import crudCilindros

from modelo.reporte import Pdf

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
    crud = None

    def obtenerWidget(formulario, nombre, apellido, cedula, ubicacion, telefono, correo, columnaCards, tituloAgregarJefes, tituloCilindroSeleccionado, 
    tituloCilindroPropietario, titulo, contenedorInicio, contenedorReporte, contenedorHistorial, contenedorPerfilJefe, contenedorPerfilLider, 
    formularioJefe, formularioCilindro, contenedorJefeFamilia, tablaJornadaPrincipal, nombreLi, apellidoLi, cedulaLi, ubicacionLi, telefonoLi, 
    correoLi, textoSlider, tablaLlenarHistorial, tablaSeleccionarHistorial, appbar, crud):
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
        gestionPrincipal.crud = crud

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
                    DataCell(Row(controls=[IconButton(icon=icons.EDIT, tooltip="Editar Cilindro", on_click=lambda _, idss=idss: gestionPrincipal.crud.abrirEditarCilindro(idss, nombre, cedulaIdentidad)), IconButton(icon=icons.DELETE, tooltip="Eliminar Cilindro", on_click=lambda _, idss=idss: gestionPrincipal.crud.abrirEliminarCilindro(idss, nombre, cedulaIdentidad))]))
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
                    DataCell(Row(controls=[IconButton(icon=icons.CANCEL, tooltip="Quitar", on_click=lambda _, idPedido=idPedido: gestionPrincipal.crud.eliminarJornadaJefe(idPedido, nombre, cedulaIdentidad))]))
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

    def diriguirAnadirCilindro():
        gestionPrincipal.crud.abrirAnadirCilindro(cedulaIdentidad)

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

class archivoPdf:
    #LIMPIAN LOS CONTENEDORES ANTES DE CARGAR LA INFORAMCION
    def volverGenerarArchivo(instancia):
        instancia.volverGenerarArchivos(consulta.obtenerIdArchivos, mensaje.datosUsuarioLista[0][0])

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

    