from datetime import datetime
from controlador.conexion import db
from modelo.consultas import consulta
import pathlib

class mensaje:
    datosUsuarioLista = []
    
    #GENERAL
    campoFaltante = "Campo vacio, por favor rellenelo para continuar"
    derechosAutores = "Creado por: Diego Marin, Marco Bandrez, Joel Seco"
    nombre = "Nombre"
    apellido = "Apellido"
    tipo = "Tipo"
    cedula = "Cedula"
    codigoTelefono = "Codigo"
    nTelefono = "N telefono"
    tipoCorreo = "Correo"
    correo = "Direccion"
    cerrarSeccion = "Cerrar sesion"
    bienvenida = "Bienvenido"
    inicio = "Inicio"
    reporte = "Reporte"
    historial = "Historial"
    perfil = "Perfil"
    regresarBtn = "Regresar"

    empresa = "Empresa"
    tamano = "Tamaño"
    pico = "Pico"
    acciones = "Accion"
    idColumnas = "id"

    def minimoCaracteres(cantidad):
        return rf"Minimo {cantidad} caracteres"

    #LOGIN
    usuarioNoEncontrado = "El usuario no esta registrado"
    crearCuenta = "Crear cuenta"
    registrate = "No se encuentra registrado?"
    inicioSeccion = "Iniciar Sesión"
    recuperarContrasena = "Olvido su contrasena?"
    ingresaContrasena = "Ingrese su contraseña"
    ingresaUsuario = "Ingrese su usuario"
    usuarioBloqueado = "Tu usuario se encuentra bloqueado"
    bloqueado = "El usuario a sido bloqueado por medidas de seguridad"
    def intentosBloqueo(intento):
        return rf"La contraseña no coincide con el usuario, tiene 3 intentos antes de bloquear la cuenta y lleva {intento} intento"

    #PRINCIPAL
    tituloComunidad = "Mi Comunidad"
    mensajeSinJefesFamilia = "No tienes a ningun Jefe de Familia resgistrado, pusla agregar para añadir a los jefes familiares"
    cantidadCilindros = "Cantidad de cilindros"

    #LIDER POLITICO
    anadirNuevaEmpresa = "Añade una nueva empresa"
    anadirNuevoPico = "Añade un nuevo tipo de pico"
    anadidoEmpresa = "La empresa se guardo correctamente"
    empresaDuplicada = "Esta Empresa ya esta registrada"
    picoDuplicado = "Esta Tamaño ya esta registrada"
    anadidoPico = "El nuevo tipo de pico se guardo correctamente"
    nombreEditadoFinal = "El nombre se modifico correctamente"
    apellidoEditadoFinal = "El apellido se modifico correctamente"
    telefonoInvalido = "numero de telefono invalido"
    telefonoRegistrado = "Esta numero de telefono ya esta registrado"
    telefonoGuardado = "El numero de telefono se modifico correctamente"
    correoRegistrado = "Esta correo ya esta registrado"
    correoInvalido = "Correo invalido, muy corto"
    correoGuardado = "El correo se modifico correctamente"


    def salir(page, indicator):
        fechaS = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        db.consultaSinRetorno(consulta.guardarSalidaBitacora, [fechaS, mensaje.datosUsuarioLista[0][5], mensaje.datosUsuarioLista[0][4]])
        page.go("/")
        mensaje.cambiarPagina(indicator, 5.5)
        mensaje.datosUsuarioLista.clear()

    #QUITAR MENSAJES DE ERRORES QUE APARECEN EN LO CAMPOS DE TEXTO CUANDO SE INTRODUCEN DATOS MALOS
    def quitarError(page, textfield):
        textfield.error_text = None
        page.update()

    #CIERRA MENSAJES DE ALERTA EN EL PROGRAMA
    def cerrarAlert(page, alert):
        alert.open = False
        page.update()

    #PARA MOVER LA BARRA DEL INDICADOR DEL SLIDER
    def cambiarPagina(indicador, y):
        indicador.offset.y = y
        indicador.update()

    def cambiarTitulo(page, widget, titulo):
        widget.value = titulo
        page.update()

    def validarNumeros(campo, pagee):
        digitos = campo.value

        if digitos.isdigit():
            pass
        else:
            for i in digitos:
                if i not in "0123456789":
                    digitos = digitos.replace(i, "", 1)

            campo.value = digitos
            pagee.update()

    def validarAlfanumeros(campo, pagee):
        digitos = campo.value

        if digitos.isdigit():
            pass
        else:
            for i in digitos:
                if i not in "0123456789 qwertyuiopasdfghjklzxcvbnmñQWERTYUIOPASDFGHJKLZXCVBNMÑ":
                    digitos = digitos.replace(i, "", 1)

            campo.value = digitos
            pagee.update()

    def validarNombres(campo, pagee):
        digitos = campo.value

        if digitos.isalpha():
            pass
        else:
            for i in digitos:
                if i not in "qwertyuiopasdfghjklzxcvbnmñQWERTYUIOPASDFGHJKLZXCVBNMÑ,":
                    digitos = digitos.replace(i, "", 1)

            campo.value = digitos
            pagee.update()

    def validarCorreo(campo, pagee):
        digitos = campo.value

        if digitos.isspace():
            for i in digitos:
                if i in r" @!#$%^&*()_-=+][}{\|';:<>/?`~":
                    digitos = digitos.replace(i, "", 1)

                    campo.value = digitos
                    pagee.update()
        else:
            for i in digitos:
                if i in r" @!#$%^&*()_-=+][}{\|';:<>/?`~":
                    digitos = digitos.replace(i, "", 1)

            campo.value = digitos
            pagee.update()

    def validarEspacio(campo, pagee):
        digitos = campo.value

        if digitos.isspace():
            for i in digitos:
                if i in " ":
                    digitos = digitos.replace(i, "", 1)

                    campo.value = digitos
                    pagee.update()
        else:
            for i in digitos:
                if i in " ":
                    digitos = digitos.replace(i, "", 1)

            campo.value = digitos
            pagee.update()