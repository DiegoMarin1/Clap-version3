import sqlite3
from modelo.consultas import consulta
import pathlib

class db:
    def conectar():
        try:
            rutaActual = pathlib.Path(__file__).parent.absolute()
            dbname = rutaBD = rf"{rutaActual}\dbclap.db"
            miConexion = sqlite3.connect(dbname)
            cursor = miConexion.cursor()
            return miConexion, cursor
        except:
            print("Ocurrio un error en la conexion con la base de datos")

#LOGIN
    def accesoSistema(user, contra):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.nivelUser, [user, contra])
        miConexion.commit()
        return cursor.fetchall()

    def bloqueoUser(user):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.bloqueoUser, [user,])
        miConexion.commit()
        return cursor.fetchall()

    def bloqueoContra(user, contra):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.bloqueoContra, [contra, user])
        miConexion.commit()
        return cursor.fetchall()

    def confirmarAccesoUsuario(user, contra):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.bloqueoContra, [contra, user])
        miConexion.commit()

    def obtenerDatosUsuario(user):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerDatosUsuario, [user,])
        miConexion.commit()
        return cursor.fetchall()

    def guardarEntradaBitacora(fecha, idUsuario):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarEntradaBitacora, [fecha, idUsuario])
        miConexion.commit()

    def bloquearUsuario(usuario):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.bloquearUsuario, [usuario,])
        miConexion.commit()
    
    def denegarAccesoUsuarioBloquado(usuario):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.userBloqueado, [usuario,])
        miConexion.commit()
        return cursor.fetchall()

    def guardarSalidaBitacora(fechaSalida, fechaEntrada, userId):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarSalidaBitacora, [fechaSalida, fechaEntrada, userId])
        miConexion.commit()

#REGISTRO USUARIO
    def verificarCorreo(correo):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarCorreo, [correo,])
        miConexion.commit()
        return cursor.fetchall()

    def verificarCedula(cedula):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verficarCedula, [cedula,])
        miConexion.commit()
        return cursor.fetchall()

    def verificarTelefono(telefono):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verficarNumero, [telefono,])
        miConexion.commit()
        return cursor.fetchall()

    def verificarUbicacion(ubicacion):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verficarUbicacion, [ubicacion,])
        miConexion.commit()
        return cursor.fetchall()

    def verificarNombreUsuario(nombreUsuario):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarNombreUsuario, [nombreUsuario,])
        miConexion.commit()
        return cursor.fetchall()

    def llenarPreguntas():
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.llenarPreguntas)
        miConexion.commit()
        return cursor.fetchall()

    def obtenerIdPregunta(pregunta):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerIdPregunta, [pregunta,])
        miConexion.commit()
        return cursor.fetchall()

    def guardarRespuesta(respuesta, idPregunta):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarRespuesta, [respuesta, idPregunta])
        miConexion.commit()

    def obtenerIdRespuesta(idPregunta, respuesta):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerIdRespuesta, [idPregunta, respuesta])
        miConexion.commit()
        return cursor.fetchall()

    def guardarLider(nombre, apellido, cedula, telefono, correo, ubicacion):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarLider, [nombre, apellido, cedula, telefono, correo, ubicacion])
        miConexion.commit()

    def obtenerIdLider(cedula):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerIdLider, [cedula,])
        miConexion.commit()
        return cursor.fetchall()
    
    def guardarUsuario(user, contra, respuestaId, liderId, nivelUser):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarUsuario, [user, contra, respuestaId, liderId, nivelUser])
        miConexion.commit()

#RECUPERAR USUARIO
    def verificarPreguntaRecuperar(cedula):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarCedulaRecuperar, [cedula,])
        miConexion.commit()
        return cursor.fetchall()

    def verificarRespuestaRecuperar(cedula):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarRespuesta, [cedula,])
        miConexion.commit()
        return cursor.fetchall()

    def obtenerIdCedulaRecuperar(cedula):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerIdCedulaRecuperar, [cedula,])
        miConexion.commit()
        return cursor.fetchall()

    def guardarCambiosContrasena(contrasena, cedula):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarCambiosContrasena, [contrasena, cedula])
        miConexion.commit()

#GENERACION DE CARTAS
    def verificarJefesFamiliaCartas(idUsuario):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarJefesFamiliaCartas, [idUsuario,])
        miConexion.commit()
        return cursor.fetchall()

    def obtenerInfoJefesFamiliaCartas(idUsuario):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerInfoJefesFamiliaCartas, [idUsuario,])
        miConexion.commit()
        return cursor.fetchall()

#FORMULARIO DE JEFES DE FAMILIA Y CILINDROS
    def verificarCedulaJefesFamilia(cedula):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarCedulaJefesFamilia, [cedula,])
        miConexion.commit()
        return cursor.fetchall()

    def verificarTelefonoJefesFamilia(telefono):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarTelefonoJefesFamilia, [telefono,])
        miConexion.commit()
        return cursor.fetchall()
    
    def verificarCorreoJefesFamilia(correo):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarCorreoJefesFamilia, [correo,])
        miConexion.commit()
        return cursor.fetchall()

    def obtenerEmpresas():
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerEmpresas)
        miConexion.commit()
        return cursor.fetchall()

    def obtenerTamanos():
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerTamanos)
        miConexion.commit()
        return cursor.fetchall()

    def obtenerPicos():
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerPicos)
        miConexion.commit()
        return cursor.fetchall()

    def guardarJefeFamilia(arregloCedula, nombre, apellido, arregloTelefono, arregloCorreo, iDLiderCalle):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarJefeFamilia, [arregloCedula, nombre, apellido, arregloTelefono, arregloCorreo, iDLiderCalle])
        miConexion.commit()

    def obtenerIdJefeFamilia(cedula):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerIdJefeFamilia, [cedula,])
        miConexion.commit()
        return cursor.fetchall()

    def obtenerIdEmpresa(empresa):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerIdEmpresa, [empresa,])
        miConexion.commit()
        return cursor.fetchall()

    def obtenerIdTamano(tamano):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerIdTamano, [tamano,])
        miConexion.commit()
        return cursor.fetchall()

    def obtenerIdPico(pico):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerIdPico, [pico,])
        miConexion.commit()
        return cursor.fetchall()

    def guardarCilindros(empresaId, picoId, tamanoId, idJefeFamiliar, fecha):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarCilindros, [empresaId, picoId, tamanoId, idJefeFamiliar, fecha])
        miConexion.commit()

    def obtenerCilindrosJefeFamilia(idJefeFamilia):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerCilindrosJefeFamilia, [idJefeFamilia,])
        miConexion.commit()
        return cursor.fetchall()

    def quitarCilindrosRepetidos(idJefeFamilia):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerCilindrosRepetidos, [idJefeFamilia,])
        miConexion.commit()
        return cursor.fetchall()

    def mostrarCilindrosJefeFamilia(idJefeFamilia):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.mostrarCilindrosJefeFamilia, [idJefeFamilia,])
        miConexion.commit()
        return cursor.fetchall()

    def guardarCilindrosPedidos(idCilindro, fechaPedido):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarCilindrosPedidos, [idCilindro, fechaPedido])
        miConexion.commit()

    #CRUD CILINDRO
    def eliminarCilindro(idCilindro):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.eliminarCilindro, [idCilindro,])
        miConexion.commit()

    def editarCilindro(idCilindro):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.editarCilindro, [idCilindro,])
        miConexion.commit()
        return cursor.fetchall()

    def guardarCambioCilindro(empresa, pico, tamano, idCilindro):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarCambioCilindro, [empresa, pico, tamano, idCilindro])
        miConexion.commit()

    def eliminarCilindroJornadaJefe(idCilindro):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.eliminarCilindroJornadaJefe, [idCilindro,])
        miConexion.commit()
        
    def mostrarDatosJefe(idJefeFamilia):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.mostrarDatosJefe, [idJefeFamilia,])
        miConexion.commit()
        return cursor.fetchall()

    #ACTUALIZAR DATOS DE PERSONAS
    def actualizarNombreJefe(nombre, idJefeFamilia):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.actualizarNombreJefe, [nombre, idJefeFamilia])
        miConexion.commit()

    def actualizarApellidoJefe(apellido, idJefeFamilia):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.actualizarApellidoJefe, [apellido, idJefeFamilia])
        miConexion.commit()

    def verificarCorreoEditar(correo):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarCorreoEditar, [correo,])
        miConexion.commit()
        return cursor.fetchall()

    def actualizarCorreoJefe(correo, idJefeFamilia):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.actualizarCorreoJefe, [correo, idJefeFamilia])
        miConexion.commit()

    def verificarTelefonoEditar(telefono):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarTelefonoEditar, [telefono,])
        miConexion.commit()
        return cursor.fetchall()

    def actualizarTelefonoJefe(telefono, idJefeFamilia):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.actualizarTelefonoJefe, [telefono, idJefeFamilia])
        miConexion.commit()

    def obtenerReportesPedidos(idJefeFamilia):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerReportesPedidos, [idJefeFamilia,])
        miConexion.commit()
        return cursor.fetchall()

    def eliminarCilindroJornada(idJefeFamilia):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.eliminarCilindroJornada, [idJefeFamilia,])
        miConexion.commit()

    def mostrarDatosLider(iDLiderCalle):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.mostrarDatosLider, [iDLiderCalle,])
        miConexion.commit()
        return cursor.fetchall()

    def actualizarNombreLider(nombre, idLiderCalle):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.actualizarNombreLider, [nombre, idLiderCalle])
        miConexion.commit()

    def actualizarApellidoLider(apellido, idLiderCalle):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.actualizarApellidoLider, [apellido, idLiderCalle])
        miConexion.commit()
    
    def verificarTelefonoLider(telefono):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarTelefonoLider, [telefono,])
        miConexion.commit()
        return cursor.fetchall()

    def actualizarTelefonoLider(telefono, idLiderCalle):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.actualizarTelefonoLider, [telefono, idLiderCalle])
        miConexion.commit()

    def verificarCorreoLider(correo):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarCorreoLider, [correo,])
        miConexion.commit()
        return cursor.fetchall()

    def actualizarCorreoLider(correo, idLiderCalle):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.actualizarCorreoLider, [correo, idLiderCalle])
        miConexion.commit()

    def verificarGeneracion(idLiderCalle, fecha):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarGeneracion, [idLiderCalle, fecha])
        miConexion.commit()
        return cursor.fetchall()

    def verificarPedidos(idLiderCalle):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarPedidos, [idLiderCalle,])
        miConexion.commit()
        return cursor.fetchall()

    def obtenerCostosCilindros():
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerCostosCilindros)
        miConexion.commit()
        return cursor.fetchall()

    def obtenerJornadaArchivo(idLiderCalle):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerJornadaArchivo, [idLiderCalle,])
        miConexion.commit()
        return cursor.fetchall()

    def guardarRutasArchivos(ruta, fecha):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarRutasArchivos, [ruta, fecha])
        miConexion.commit()

    def obtenerIdArchivo(ruta, fecha):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerIdArchivo, [ruta, fecha])
        miConexion.commit()
        return cursor.fetchall()

    def asignarIdArchivo(idArchivo, idPedido):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.asignarIdArchivo, [idArchivo, idPedido])
        miConexion.commit()

    def obtenerHistorial(idArchivo):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerHistorial, [idArchivo,])
        miConexion.commit()
        return cursor.fetchall()

    def obtenerIdArchivos(IdLiderCalle):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerIdArchivos, [IdLiderCalle,])
        miConexion.commit()
        return cursor.fetchall()

    def obtenerFechasJornadas(idArchivos):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerFechasJornadas, [idArchivos,])
        miConexion.commit()
        return cursor.fetchall()

    def origenRutaArchivo(idArchivo):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.origenRutaArchivo, [idArchivo,])
        miConexion.commit()
        return cursor.fetchall()

    def obtenerDatosLiderPolitico(idLiderPolitico):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerDatosLiderPolitico, [idLiderPolitico,])
        miConexion.commit()
        return cursor.fetchall()

    def obtenerTodosUsuarios():
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerTodosUsuarios)
        miConexion.commit()
        return cursor.fetchall()

    def obtenerDatosUsuarioLideresCalle(idUsuario):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerDatosUsuarioLideresCalle, [idUsuario,])
        miConexion.commit()
        return cursor.fetchall()

    def actualizarEstatusUsuario(estatus, idUsuario):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.actualizarEstatusUsuario, [estatus, idUsuario])
        miConexion.commit()

    def actualizarPrecios(precio, idTamano):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.actualizarPrecios, [precio, idTamano])
        miConexion.commit()

    def verificarEmpresa(empresa):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarEmpresa, [empresa,])
        miConexion.commit()
        return cursor.fetchall()

    def guardarEmpresaNueva(empresa):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarEmpresaNueva, [empresa,])
        miConexion.commit()

    def verificarPico(pico):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.verificarPico, [pico,])
        miConexion.commit()
        return cursor.fetchall()

    def guardarPicoNuevo(pico):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.guardarPicoNuevo, [pico,])
        miConexion.commit()

    def extraerBitacora(ci):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.extraerBitacora, [ci,])
        miConexion.commit()
        return cursor.fetchall()

    def obtenerArchivosId(ci):
        miConexion, cursor = db.conectar()
        cursor.execute(consulta.obtenerArchivosId, [ci,])
        miConexion.commit()
        return cursor.fetchall()
