from flet import *
from controlador.mensajes import mensaje
from controlador.conexion import db

class caracteristicasCilindro:
    def nuevaCaracteristica(page, texto, caracteristica, metodoValidar, query, avisoDuplicado, mensajeExito, queryGuardar):
        alertNuevaCaracteristica = AlertDialog(
            content=Container(
                alignment=alignment.center,
                height=150,
                width=300,
                bgcolor="white",
                content=Column(
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        Text(texto),
                        caracteristica,
                    ]
                )
            ),
            actions=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        ElevatedButton("Guardar", on_click=lambda _:metodoValidar(page, alertNuevaCaracteristica, caracteristica, query, avisoDuplicado, mensajeExito, queryGuardar)),
                        ElevatedButton("Cancelar", on_click=lambda _:mensaje.cerrarAlert(page, alertNuevaCaracteristica))
                    ]
                )
            ]
        )

        page.dialog = alertNuevaCaracteristica
        alertNuevaCaracteristica.open = True

        page.update()

    def ValidarNuevaCaracteristica(page, alert, caracteristica, query, avisoDuplicado, mensajeExito, queryGuardar):

        if (caracteristica.value == "") or (len(caracteristica.value) < 3):
            if caracteristica.value == "":
                caracteristica.error_text = mensaje.campoFaltante
                page.update()
            if len(caracteristica.value) < 3:
                caracteristica.error_text = mensaje.minimoCaracteres(3)
                page.update()
        elif db.consultaConRetorno(query, [caracteristica.value,]):
            page.snack_bar = SnackBar(content=Text(avisoDuplicado))
            page.snack_bar.open = True
            page.update()
        else:
            db.consultaSinRetorno(queryGuardar, [caracteristica.value,])
            mensaje.cerrarAlert(page, alert)
            caracteristica.value = ""
            page.snack_bar = SnackBar(bgcolor="GREEN", content=Text(mensajeExito))
            page.snack_bar.open = True
            page.update()