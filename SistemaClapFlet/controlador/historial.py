from flet import *
from flet import AlertDialog, Column, Text, border_radius, ScrollMode, ElevatedButton, DataRow, DataCell, SnackBar
from controlador.mensajes import mensaje
from controlador.conexion import db
from modelo.consultas import consulta

import os
import shutil

class historial:
    def __init__(self, page, tablaLlenarHistorial, tablaSeleccionarHistorial):
        self.page = page
        self.tablaLlenarHistorial = tablaLlenarHistorial
        self.tablaSeleccionarHistorial = tablaSeleccionarHistorial

        self.contenido = []
        self.bitacoraLista = []
        self.his = []

    #CARGAR LOS DATOS DE LAS JORNADAS
    def abrirHistorial(self, fechaa, idss):
        self.tablaLlenarHistorial.rows.clear()
        self.tablaLlenarHistorial.rows = self.llenarHistroial(idss)

        alertHistorial = AlertDialog(
            modal=True,
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
                                self.tablaLlenarHistorial,
                            ]
                        )
                    ),
                ]
            ),
            actions=[ElevatedButton("Descargar Pdf", on_click=lambda _:self.descargarArchivo(alertHistorial, idss)), ElevatedButton("Regresar", on_click=lambda _:mensaje.cerrarAlert(self.page, alertHistorial))]
        )

        self.page.dialog = alertHistorial
        alertHistorial.open = True

        self.page.update()

    #EXTRAER DE DATOS EL CONTENEDOR DEL HISTORIAL
    def llenarHistroial(self, ids):
        resultado = db.consultaConRetorno(consulta.obtenerHistorial, [ids,])

        for idss, cii, nom, ape, empresa, tamano, pico , fecha in resultado:
            self.contenido.append(DataRow(
                color="WHITE",
                cells=[
                    DataCell(Text(f"{cii}")),
                    DataCell(Text(f"{nom}")),
                    DataCell(Text(f"{ape}")),
                    DataCell(Text(f"{empresa}")),
                    DataCell(Text(f"{tamano}")),
                    DataCell(Text(f"{pico}")),
                    DataCell(Text(f"{fecha}")),
                ],
            ),
            )

            self.page.update()

        return self.contenido
    
    #SECCION DE ARCHIVOS
    def volverGenerarArchivos(self, query, parametro):
        self.bitacoraLista.clear()
        self.tablaSeleccionarHistorial.rows.clear()
        self.tablaSeleccionarHistorial.rows = self.generarArchivos(query, parametro)

        self.page.update()

    def generarArchivos(self, query, parametro):
        coun = 1
        resultadoId = db.consultaConRetorno(query, [parametro,])

        for idss in resultadoId:

            datos = db.consultaConRetorno(consulta.obtenerFechasJornadas, [idss[0],])

            self.bitacoraLista.append([datos[0][0], datos[0][1]])

        for fecha, ids in self.bitacoraLista:
            self.his.append(DataRow(
                color="WHITE",
                cells=[
                    DataCell(Text(f"Jornada {coun}")),
                    DataCell(Text(f"{fecha}")),
                ],
                on_select_changed=lambda _, fecha = fecha, ids = ids: [self.abrirHistorial(fecha, ids)]
            ),
            )
            coun = coun + 1

            self.page.update()

        return self.his

    def descargarArchivo(self, alertt, ids):

        origen = db.consultaConRetorno(consulta.origenRutaArchivo, [ids,])
        destino = os.path.join(os.path.join(os.environ['USERPROFILE']), rf'Desktop\Reportes')

        rutaEscritorio = os.path.join(os.path.join(os.environ['USERPROFILE']), rf'Desktop\Reportes')

        if os.path.exists(rutaEscritorio) == True:
            pass
        else:
            os.mkdir(rutaEscritorio)

        shutil.copy(origen[0][0], destino)

        mensaje.cerrarAlert(self.page, alertt)
        self.page.snack_bar = SnackBar(content=Text("El PDF se descargo correctamente, puede visualizarlo en la caperta Reportes ubicada en el escritorio"), bgcolor="GREEN")
        self.page.snack_bar.open = True
        self.page.update()