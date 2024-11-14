from flet import *
import flet as flet
from flet_route import Routing, path

from views.login import login
from views.register import register
from views.principal import principal
from views.recuperar import recuperar
from views.liderPolitico import liderPolitico


def main(page:Page):
    rutas = [
        path(url="/", 
        clear=True,
        view=login().view),

        path(url="/register", 
        clear=True,
        view=register().view),
    
        path(url="/recuperar", 
        clear=True, 
        view=recuperar().view), 

        path(url="/principal", 
        clear=True,
        view=principal().view),

        path(url="/liderPolitico",
        clear=True,
        view=liderPolitico().view) 
    ]

    Routing(page=page, app_routes=rutas)
    page.go(page.route)

flet.app(target=main)