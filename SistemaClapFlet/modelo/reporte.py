from fpdf import FPDF
from flet import *
from datetime import datetime
from controlador.conexion import db
from controlador.mensajes import mensaje
from controlador.rutas import rutas
from modelo.consultas import consulta
import pathlib

import os
import shutil
#ACOMODAR SI NO HAY CARPETA REPORTES CREARLA
class Pdf(FPDF):
    def __init__(self):
        self.Header()

    def Header(self):

        self.idPedidos = []
        self.idPedidos.clear()
        resultadoPrecios = db.consultaConRetorno(consulta.obtenerCostosCilindros)
        
        #------------------Definir tipo de hoja----------------
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.add_page()

        #---------------------Insertar Logo-------------------------------

        self.pdf.image(rf"{rutas.rutaActualArreglada}\img\clap.png", x = 45, y = 5, w = 120, h = 35)
        self.pdf.rect(x = 0, y = 45, w = 210, h = 0)

        #---------------------Título del Pdf---------------------------
        self.fecha = datetime.today().strftime('%d-%m-%Y')
        self.pdf.set_font("Times", "B", 25)
        self.pdf.set_y(55)
        self.pdf.cell(w = 0, h = 15, txt = "Reporte de cilindros", align = "C", border = 0, fill = 0, ln=1)
        self.pdf.set_font("Times", "U", 12)
        self.pdf.multi_cell(w = 0, h = 10, txt = f"{mensaje.datosUsuarioLista[0][1]} {mensaje.datosUsuarioLista[0][2]}", align = "C", border = 0, fill = 0)
        self.pdf.multi_cell(w = 0, h = 10, txt = f"{mensaje.datosUsuarioLista[0][3]}", align = "C", border = 0, fill = 0)
        self.pdf.multi_cell(w = 0, h = 10, txt = f"Altagracia de Orituco {self.fecha}", border = 0, align = "C", fill = 0)
        self.pdf.multi_cell(w = 0, h = 10, txt = f"Precio Unitario:       Pequeñas={resultadoPrecios[0][0]}Bs    Medianas={resultadoPrecios[1][0]}Bs    Regulares={resultadoPrecios[2][0]}Bs    Grandes={resultadoPrecios[3][0]}Bs", align = "C", border = 0, fill = 0)
        
        self.Body()

    def Body(self):

        #---------------------Tabla-------------------------------
        self.pdf.set_font("Times", "", 14)
        self.pdf.set_y(115)
        self.pdf.set_fill_color(r = 239, g = 71, b = 71)
        self.pdf.cell(w = 27, h = 15, txt = "Cédula", border = 1, align = "C", fill = 1)
        self.pdf.cell(w = 27, h = 15, txt = "Nombre", border = 1, align = "C", fill = 1)
        self.pdf.cell(w = 27, h = 15, txt = "Apellido", border = 1, align = "C", fill = 1)
        self.pdf.cell(w = 27, h = 15, txt = "Empresa", border = 1, align = "C", fill = 1)
        self.pdf.cell(w = 27, h = 15, txt = "Pico", border = 1, align = "C", fill = 1) 
        self.pdf.cell(w = 27, h = 15, txt = "Tamaño", border = 1, align = "C", fill = 1) 
        self.pdf.multi_cell(w = 27, h = 15, txt = "Agregado", border = 1, align = "C", fill = 1)

        #----------------------------------Lista-------------------------------------
        
        c = 0

        contP = 0
        contM = 0
        contR = 0
        contG = 0

        valorP = 0
        valorM = 0
        valorR = 0
        valorG = 0

        totalP = 0
        totalM = 0
        totalG = 0
        totalR = 0

        self.informacion = db.consultaConRetorno(consulta.obtenerJornadaArchivo, [mensaje.datosUsuarioLista[0][0],])
        
        #-----------------------------Cliclo For-----------------------------------------
        for ids, ci, nom, ape, emp, pic, tamn, cos, fech in self.informacion:

            if(c%2==0):self.pdf.set_fill_color(r = 209, g = 209, b = 209)
            else:self.pdf.set_fill_color(r = 255, g = 255, b = 255)

            self.pdf.cell(w = 27, h = 10, txt = str(ci), border = "TBL", align = "C", fill = 1)
            self.pdf.cell(w = 27, h = 10, txt = str(nom), border = "TBL", align = "C", fill = 1)
            self.pdf.cell(w = 27, h = 10, txt = str(ape), border = "TBL", align = "C", fill = 1)
            self.pdf.cell(w = 27, h = 10, txt = str(emp), border = "TBL", align = "C", fill = 1)
            self.pdf.cell(w = 27, h = 10, txt = str(pic), border = "TBL", align = "C", fill = 1)
            self.pdf.cell(w = 27, h = 10, txt = str(tamn), border = "TBL", align = "C", fill = 1)
            self.pdf.multi_cell(w = 27, h = 10, txt = str(fech), border = "TBL", align = "C", fill = 1)

            if tamn == "Pequeña":
                contP = contP + 1
                totalP = valorP + cos
                valorP = totalP

            elif tamn == "Mediana":
                contM = contM + 1
                totalM = valorM + cos
                valorM = totalM

            elif tamn == "Regular":
                contR = contR + 1
                totalR = valorR + cos
                valorR = totalR

            elif tamn == "Grande":
                contG = contG + 1
                totalG = valorG + cos
                valorG = totalG

            c+=1 

            self.idPedidos.append(ids) 

        totalVenta = totalP + totalM + totalR + totalG
        self.pdf.multi_cell(w = 0, h = 10, txt = f"Cantidad:       Pequeñas={contP}    Medianas={contM}    Regulares={contR}    Grandes={contG} Monto Total: {totalVenta}Bs", align = "C", border = 0, fill = 2)

        self.pdf.multi_cell(w = 0, h = 10, txt = f"Observaciones:", align = "C", border = 0, fill = 3)

        self.Footer()

    def Footer(self):
        rutaActual = pathlib.Path(__file__).parent.absolute()
        nombreArchivo = f'jornada_venta_de_gas_{mensaje.datosUsuarioLista[0][1]}_{self.fecha}.pdf'
        rutaEscritorio = os.path.join(os.path.join(os.environ['USERPROFILE']), rf'Desktop\Reportes')

        self.fecha = datetime.today().strftime('%d-%m-%Y')

        if os.path.exists(rutaEscritorio) == True:
            pass
        else:
            os.mkdir(rutaEscritorio)

        #--------------------------Pie de pagina------------------------------------

        self.pdf.output(rf'{rutaActual}\Reportes\{nombreArchivo}')
        self.pdf.output(rf'{rutaEscritorio}\{nombreArchivo}')

        db.consultaSinRetorno(consulta.guardarRutasArchivos, [rf'{rutaActual}\Reportes\{nombreArchivo}', self.fecha])
        resultadoIdArchivo = db.consultaConRetorno(consulta.obtenerIdArchivo, [rf"{rutaActual}\Reportes\{nombreArchivo}", self.fecha])

        
        for i in self.idPedidos:
            db.consultaSinRetorno(consulta.asignarIdArchivo, [resultadoIdArchivo[0][0], i])
        self.idPedidos.clear()