from flet import *

class historial:
    #CARGAR LOS DATOS DE LAS JORNADAS
    def abrirHistorial(page, fechaa, idss):
        gestionPrincipal.tablaLlenarHistorial.rows.clear()
        gestionPrincipal.tablaLlenarHistorial.rows = historial.llenarHistroial(page, idss)

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
                                gestionPrincipal.tablaLlenarHistorial,
                            ]
                        )
                    ),
                ]
            ),
            actions=[ElevatedButton("Descargar Pdf", on_click=lambda _:archivos.descargarArchivo(page, alertHistorial, idss)), ElevatedButton("Regresar", on_click=lambda _:mensaje.cerrarAlert(page, alertHistorial))]
        )

        page.dialog = alertHistorial
        alertHistorial.open = True

        page.update()

    #EXTRAER DE DATOS EL CONTENEDOR DEL HISTORIAL
    def llenarHistroial(page, ids):
        resultado = db.consultaConRetorno(consulta.obtenerHistorial, [ids,])

        for idss, cii, nom, ape, empresa, tamano, pico , fecha in resultado:
            gestionPrincipal.contenido.append(DataRow(
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

            page.update()

        return gestionPrincipal.contenido