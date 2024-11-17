from flet import SnackBar, Text
from time import sleep
from datetime import datetime
from controlador.conexion import db
from controlador.mensajes import mensaje
from controlador.rutas import rutas
from modelo.consultas import consulta

#CORREGIR LA VALIDACION QUE CUANDO EL USUARIO ESTE BLOQUEADO NO SIGA APARECIENDO EL MENSAJE DE INTENTOS FAC|LLIDOS ASI SE INTRODUZCA LA CONTRASENA MALA

class gestionLogin:
    intentos = 0

    def camposVacios(page, usuario, contrasena):

            if (usuario.value == "") or (contrasena.value == ""):
                if usuario.value == "":
                    usuario.error_text = mensaje.campoFaltante
                    page.update()

                if contrasena.value == "":
                    contrasena.error_text = mensaje.campoFaltante
                    page.update()
        
            else:
                gestionLogin.acceso(page, usuario, contrasena)

        
    def acceso(page, usuario, contrasena):
        
        #SE HACE LA CONSULTA
        resultado = db.consultaConRetorno(consulta.nivelUser, [usuario.value, contrasena.value])
        resultadoBloqueoUser = db.consultaConRetorno(consulta.bloqueoUser, [usuario.value,])
        resultadoBloqueoContra = db.consultaConRetorno(consulta.bloqueoContra, [contrasena.value, usuario.value])

        #SUMAR INTENTO DE BLOQUEO
        if (bool(resultadoBloqueoUser) == True) and (bool(resultadoBloqueoContra) == False): gestionLogin.bloqueoUsuario(page, usuario)

        #DENEGAR ACCESO A USURIAOS BLOQUEADOS
        elif db.consultaConRetorno(consulta.userBloqueado, [usuario.value,]):
            page.snack_bar = SnackBar(content=Text(mensaje.usuarioBloqueado), bgcolor="RED")
            page.snack_bar.open = True
            page.update()

        elif resultado:        
            fechaE = datetime.today().strftime('%Y-%m-%d %H:%M:%S') 
            gestionLogin.datosUsuario(usuario.value, fechaE)
            idUsuario = mensaje.datosUsuarioLista[0][4]

            if resultado[0][0] == 1:
                rutas.enrutamiento(page, rutas.routeLiderPolitico)
            if resultado[0][0] == 2:    
                rutas.enrutamiento(page, rutas.routePrincipal)
            
            db.consultaSinRetorno(consulta.guardarEntradaBitacora, [fechaE, idUsuario])
            gestionLogin.intentos = 0

        else:
            page.snack_bar = SnackBar(content=Text(mensaje.usuarioNoEncontrado))
            page.snack_bar.open = True
            page.update()

    def bloqueoUsuario(page, usuario):
        
        if gestionLogin.intentos == 3:
            db.consultaSinRetorno(consulta.bloquearUsuario, [usuario.value,])
            gestionLogin.intentos = 0
            page.snack_bar = SnackBar(content=Text(mensaje.bloqueado), bgcolor="RED")
            page.snack_bar.open = True
            page.update()
        else:
            gestionLogin.intentos = gestionLogin.intentos + 1
            page.snack_bar = SnackBar(content=Text(mensaje.intentosBloqueo(gestionLogin.intentos)))
            page.snack_bar.open = True
            page.update()

    def datosUsuario(usuario, fecha):    
        for ids, nom, ape, ubi, userId in db.consultaConRetorno(consulta.obtenerDatosUsuario, [usuario,]):
            mensaje.datosUsuarioLista.append([ids, nom, ape, ubi, userId, fecha])