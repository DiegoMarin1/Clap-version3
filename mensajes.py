from datetime import datetime
from controlador.conexion import db
from modelo.consultas import consulta
import pathlib
from flet import *

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
    def cambiarNombreTitulo(mensaje):
        return f"Cilindros de {mensaje}"

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

class validaciones:
    #CONDICIONES
    condicionAlfanum = r"^[0-9A-Za-z]*$"
    condicionEspacio = r"^[^\s]+$"
    
    def validarCampos(page, campo, min):
        if not campo.value:
            campo.error_text = mensaje.campoFaltante
            page.update()
            return False
        elif len(campo.value) < min:
            campo.error_text = mensaje.minimoCaracteres(min)
            page.update()
            return False
    
    def validarConsultas(page, consulta, parametros, mensaje):
        if db.consultaConRetorno(consulta, parametros):
            page.snack_bar = SnackBar(content=Text(mensaje))
            page.snack_bar.open = True
            page.update()
            return False