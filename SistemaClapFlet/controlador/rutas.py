import pathlib

class rutas:
    rutaActual = pathlib.Path(__file__).parent.absolute()
    rutaActualArreglada = str(rutaActual)[:-12]

    #RUTAS DE LOS VIEW
    routeLogin = "/"
    routeRegistrar = "/register"
    routePrincipal = "/principal"
    routeRecuperar = "/recuperar"
    routeLiderPolitico = "/liderPolitico"

    #PARA CAMBIAR DE VIEW
    def enrutamiento(page, ruta):
        page.go(ruta)
    
    #PARA CAMBIAR DE CONTENEDORES EN LA VISTA DEL VIEW
    def animar(formulario, contenedor1, contenedor2, page):
        formulario.content = contenedor2 if formulario.content == contenedor1 else contenedor1
        page.update()