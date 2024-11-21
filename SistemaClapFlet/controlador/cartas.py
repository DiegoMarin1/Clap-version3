from flet import *
from controlador.conexion import db

class cartas:
    def __init__(self, page, iDLiderCalle, tablaPedido, tablaCilindros, funcion, consulta, lista):
        self.page = page
        self.iDLiderCalle = iDLiderCalle
        self.tablaPedido = tablaPedido
        self.tablaCilindros = tablaCilindros
        self.funcion = funcion
        self.consulta = consulta
        self.lista = lista

    def generarCards(self):
        for ids, nom, ape, ci in db.consultaConRetorno(self.consulta, [self.iDLiderCalle,]):
            self.lista.append(
                Container(
                    bgcolor="RED",
                    height=150,
                    width=250,
                    padding=padding.all(7),
                    border_radius=border_radius.all(20),
                    on_click=lambda _, ids=ids, nom=nom: self.funcion(ids, self.page, nom, self.tablaCilindros, self.tablaPedido), 
                    content=Column(
                        controls=[
                            Text(f"{nom} {ape}", style=TextThemeStyle.TITLE_LARGE, color="WHITE"),
                            Text(f"{ci}", style=TextThemeStyle.TITLE_MEDIUM, color="WHITE"),
                        ]
                    )
                )
            )
            self.page.update()
        return self.lista