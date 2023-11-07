import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from twocaptcha import TwoCaptcha, NetworkException
from PIL import Image
from io import BytesIO
import pyautogui
import os
import glob
import shutil
import datetime
import random
import subprocess
import string
#para enviar email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class descargaReportes():
    def __init__(self):
        self.directoryPath = os.getcwd()
        self.defaultPathDownloads = self.directoryPath + r'\temp'
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("prefs", {
            "download.default_directory": self.defaultPathDownloads,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        # Para Ignorar los errores de certificado SSL (La conexion no es privada)
        self.options.add_argument("--ignore-certificate-errors")
        #self.pathDriver = "driver/chromedriver.exe"
        self.url = "https://claroperu.my.salesforce.com"
        #self.service = Service(self.pathDriver)
        self.driver = webdriver.Chrome(options=self.options)

    def reiniciar(self):
        self.__init__()
    
    def login(self):
        self.driver.get(self.url)
        time.sleep(5)

    def iniciarSesion(self, username, password):
        wait = WebDriverWait(self.driver, 60)
        sts = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@id='idp_section_buttons']//button[contains(@class, 'button')]")))
        sts.click()
        time.sleep(5)

        iniciarSesion = self.driver.find_element(By.NAME, 'loginfmt')
        iniciarSesion.send_keys(username)
        time.sleep(1)
        siguiente = self.driver.find_element(By.ID, 'idSIButton9')
        siguiente.click()
        time.sleep(5)

        ingresarPass = self.driver.find_element(By.NAME, 'passwd')
        ingresarPass.send_keys(password)
        time.sleep(1)
        siguiente = self.driver.find_element(By.ID, 'idSIButton9')
        siguiente.click()
        time.sleep(1)

        #idBtn_Back
        noMantenerSesion = self.driver.find_element(By.ID, 'idBtn_Back')
        noMantenerSesion.click()
        time.sleep(3)
    
    def cerrarSesion(self):
        logInImagen = self.driver.find_element(By.CLASS_NAME, 'uiImage')
        logInImagen.click()
        time.sleep(1)

        cerrarSesion = self.driver.find_element(By.XPATH, "//a[text()='Cerrar sesión']")
        cerrarSesion.click()
        time.sleep(1)
    
    def gameOver(self):
        self.driver.quit()
    
    def cantidadExcel(self):
        ruta_carpeta = self.defaultPathDownloads
        extension = '*.xlsx'
        patron_busqueda = os.path.join(ruta_carpeta, extension)
        archivos = glob.glob(patron_busqueda)
        cantidad_archivos = len(archivos)
        return cantidad_archivos
    
    # Funcion para obtener fechas
    def fecha(self, inicio = None, fin = None):
        if inicio is None:
            fechaActual = datetime.date.today()
            fechaSiguiente = fechaActual + datetime.timedelta(days=1)
        else:
            fechaActual = datetime.datetime.strptime(inicio, '%Y-%m-%d')
            if fin is None:
                fechaSiguiente = fechaActual + datetime.timedelta(days=1)
            else:
                fechaSiguiente = datetime.datetime.strptime(fin, '%Y-%m-%d')
            
        horaCero = datetime.time(0, 0, 0)
        fechaActualConHora = datetime.datetime.combine(fechaActual, horaCero)
        fechaSiguienteConHora = datetime.datetime.combine(fechaSiguiente, horaCero)
        formato = "%m/%d/%Y %H:%M:%S"
        formato2 = "%Y-%m-%d %H:%M:%S"
        
        faCH1 = fechaActualConHora.strftime(formato)
        fsCH1 = fechaSiguienteConHora.strftime(formato)
        faCH2 = fechaActualConHora.strftime(formato2)
        fsCH2 = fechaSiguienteConHora.strftime(formato2)
        faFormato1 = fechaActual.strftime("%m/%d/%Y")
        fsFormato1 = fechaSiguiente.strftime("%m/%d/%Y")
        fechaActual = fechaActual.strftime("%Y-%m-%d")
        fechaSiguiente = fechaSiguiente.strftime("%Y-%m-%d")
        fechahm = fechaActualConHora.strftime("%d/%m/%Y %H:%M")
        fechaShm = fechaSiguienteConHora.strftime("%d/%m/%Y %H:%M")
        fi = fechaActualConHora.strftime("%d/%m/%Y")
        ff = fechaSiguienteConHora.strftime("%d/%m/%Y")
        
        fechas = {"hoyH":faCH1, 'mañanaH': fsCH1, 
                'hoyH2': faCH2, 'mañanaH2': fsCH2,
                'hoy': fechaActual, 'mañana': fechaSiguiente, 
                'hoyF1': faFormato1, 'mañanaF1': fsFormato1,
                'hoyhm': fechahm, 'mañanahm': fechaShm,
                "hoy2":fi, "mañana2":ff
        }
        return fechas

    # Funcion que reubicará las descargas en sus respectivas carpetas
    def renombrarReubicar(self, nuevoNombre, carpetaDestino):
        # ruta_descargas = r"C:\Users\Usuario\Documents\terceriza\Robot\descargasPython\descargaRobotin"
        ruta_descargas = self.directoryPath + r'/temp'
        archivos_descargados = sorted(
            glob.glob(os.path.join(ruta_descargas, '*')), key=os.path.getmtime, reverse=True
        )
        # Comprobar si hay archivos descargados
        if len(archivos_descargados) > 0:
            ultimo_archivo = archivos_descargados[0]
            # Cambiar el nombre del archivo --1er argumento de la funcion
            nuevo_nombre = f'{nuevoNombre}.xlsx'
            carpeta_destino = carpetaDestino
            # Comprobar si la carpeta de destino existe, si no, crearla
            if not os.path.exists(carpeta_destino):
                os.makedirs(carpeta_destino)
            # Ruta completa del archivo de destino
            ruta_destino = os.path.join(carpeta_destino, nuevo_nombre)
            # Mover el archivo a la carpeta de destino con el nuevo nombre
            shutil.move(ultimo_archivo, ruta_destino)

    # Funcion que crea el nombre del reporte
    def nombreReporte(self, name, finicio, ffin, fechaD0 = True):
        f1 = datetime.datetime.strptime(finicio, "%d/%m/%Y")
        finicio = f1.strftime("%Y-%m-%d")
        
        if ffin == None:
            ffin = finicio
        else:
            f2 = datetime.datetime.strptime(ffin, "%d/%m/%Y")
            ffin = f2.strftime("%Y-%m-%d")
            pass
        
        if fechaD0:
            fechaHora = datetime.datetime.now()
            fecha = fechaHora.strftime("%Y%m%d_%H%M%S")
            aleatorio = str(random.randint(100, 999))
            nameFile = name + fecha + '_' + aleatorio
        else:
            if ffin == None:
                ffin = finicio
            else:
                pass
            h = datetime.datetime.now()
            hora = h.strftime('%H%M%S')
            fechan = datetime.datetime.strptime(ffin, '%Y-%m-%d')
            fechan = fechan + datetime.timedelta(days=1)
            fecha = fechan.strftime("%Y%m%d_")
            aleatorio = str(random.randint(100, 999))
            nameFile = name + fecha + hora + '_' + aleatorio
        
        return nameFile

    def validaInicioSesion(self):
        wait = WebDriverWait(self.driver, 30)
        logInImagen = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'uiImage')))
        if logInImagen:
            return True
        else:
            return False

    # --- 1. Funcion ReporteBlindaje ---
    def reporteBlindaje(self, fechaInicio, fechaFinal):
        wait = WebDriverWait(self.driver, 60)

        texto = f"Reporte Blindaje y (Retenciones)"
        inputBuscar = self.driver.find_element(By.XPATH, '//*[@id="oneHeader"]/div[2]/div[2]/div/button')
        inputBuscar.click()
        time.sleep(1)

        panel = self.driver.find_element(By.CSS_SELECTOR, '[class="panel-content scrollable"]')
        inputBox = panel.find_element(By.CSS_SELECTOR, '[class="slds-input"]')
        inputBox.clear()
        time.sleep(1)
        inputBox.send_keys(texto)
        time.sleep(1)
        inputBox.send_keys(Keys.RETURN)
        time.sleep(3)

        reporte = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'a[title="{texto}"]')))
        #reporte = driver.find_element(By.XPATH, f"//div[@aria-label='{texto}']")
        reporte.click()
        time.sleep(1)

        wait = WebDriverWait(self.driver, 10)
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="isView reportsReportBuilder"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isView")
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

        modificar = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Modificar']")))
        #modificar = driver.find_element(By.XPATH ,"//button[text()='Modificar']")
        modificar.click()
        time.sleep(2)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[title="Generador de informes"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isEdit")
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

        filtros = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Filtros']")))
        filtros.click()
        time.sleep(2)

        elementos_fecha_creacion = self.driver.find_elements(By.XPATH, "//span[text()='Fecha de creación']")
        # -----Fecha Inicio
        primer_elemento = elementos_fecha_creacion[1]
        primer_elemento.click()
        time.sleep(1)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(1)
        mayorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-5"]/a/span')
        mayorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Seleccionar una fecha']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaInicio)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        # -----Fecha Fin
        segundo_elemento = elementos_fecha_creacion[2]
        segundo_elemento.click()
        time.sleep(1)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(1)
        menorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-4"]/a/span')
        menorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Seleccionar una fecha']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaFinal)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        btnEjecutar = self.driver.find_element(By.XPATH, f"//button[text()='Ejecutar']")
        btnEjecutar.click()
        time.sleep(1)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "isView")))
        self.driver.switch_to.frame(iframe)

        totalRegistros = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Total de registros']")))
        time.sleep(1)

        #Descarga
        cantidadExcelinicial = self.cantidadExcel()
        btnDescargar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'slds-button_icon-border') and span[text()='Más acciones']]")
        btnDescargar.click()
        time.sleep(1)

        btnExportar = self.driver.find_element(By.XPATH, f"//a[span[text()='Exportar']]")
        btnExportar.click()
        time.sleep(1)

        #salir del iframe
        self.driver.switch_to.default_content()

        soloDetalles = self.driver.find_element(By.XPATH, "//span[text()='Solo detalles']")
        soloDetalles.click()
        time.sleep(1)

        formato = self.driver.find_element(By.CLASS_NAME, "slds-select")
        formato.click()
        time.sleep(1)
        formatoExcel = self.driver.find_element(By.XPATH, '//option[2]')
        formatoExcel.click()
        time.sleep(3)
        btnExportarFinal = self.driver.find_element(By.XPATH, "//span[@class='buttonLabel label bBody' and text()='Exportar']")
        btnExportarFinal.click()
        time.sleep(1)

        #Valida que la descarga concluya
        cantidadExcelFinal = cantidadExcelinicial
        while cantidadExcelFinal == cantidadExcelinicial:
            time.sleep(1)
            cantidadExcelFinal = self.cantidadExcel()
        else:
            pass
        time.sleep(2)
        self.driver.refresh()
        time.sleep(1)

    # --- Fin Funcion ReporteBlindaje ---

    # --- 2. Funcion App Mi Claro CNE Nc---
    def AppMiClaroCNeNc(self, fechaInicio, fechaFinal):
        wait = WebDriverWait(self.driver, 30)

        texto = f"Mi Claro - CNE + NC"
        inputBuscar = self.driver.find_element(By.XPATH, '//*[@id="oneHeader"]/div[2]/div[2]/div/button')
        inputBuscar.click()
        time.sleep(1)

        panel = self.driver.find_element(By.CSS_SELECTOR, '[class="panel-content scrollable"]')
        inputBox = panel.find_element(By.CSS_SELECTOR, '[class="slds-input"]')
        inputBox.clear()
        time.sleep(1)
        inputBox.send_keys(texto)
        time.sleep(1)
        inputBox.send_keys(Keys.RETURN)
        time.sleep(3)

        reporte = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'a[title="{texto}"]')))
        #reporte = driver.find_element(By.XPATH, f"//div[@aria-label='{texto}']")
        reporte.click()
        time.sleep(1)

        wait = WebDriverWait(self.driver, 60)
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="isView reportsReportBuilder"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isView")
        self.driver.switch_to.frame(iframe)
        time.sleep(5)
        

        modificar = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Modificar']")))
        #modificar = reportMain.find_element(By.XPATH ,"//button[text()='Modificar']")
        modificar.click()
        time.sleep(2)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[title="Generador de informes"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isEdit")
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

        filtros = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Filtros']")))
        filtros.click()
        time.sleep(2)

        elementos_fecha_creacion = self.driver.find_elements(By.XPATH, "//span[text()='Fecha de creación']")
        # -----Fecha Inicio
        primer_elemento = elementos_fecha_creacion[1]
        primer_elemento.click()
        time.sleep(1)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(1)
        mayorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-5"]/a/span')
        mayorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Seleccionar una fecha']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaInicio)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        # -----Fecha Fin
        segundo_elemento = elementos_fecha_creacion[2]
        segundo_elemento.click()
        time.sleep(1)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(1)
        menorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-4"]/a/span')
        menorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Introduzca una fecha relativa']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaFinal)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        btnEjecutar = self.driver.find_element(By.XPATH, f"//button[text()='Ejecutar']")
        btnEjecutar.click()
        time.sleep(1)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "isView")))
        self.driver.switch_to.frame(iframe)

        totalRegistros = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Total de registros']")))
        time.sleep(1)

        #Descarga
        cantidadExcelinicial = self.cantidadExcel()
        btnDescargar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'slds-button_icon-border') and span[text()='Más acciones']]")
        btnDescargar.click()
        time.sleep(1)

        btnExportar = self.driver.find_element(By.XPATH, f"//a[span[text()='Exportar']]")
        btnExportar.click()
        time.sleep(1)

        #salir del iframe
        self.driver.switch_to.default_content()

        soloDetalles = self.driver.find_element(By.XPATH, "//span[text()='Solo detalles']")
        soloDetalles.click()
        time.sleep(1)

        formato = self.driver.find_element(By.CLASS_NAME, "slds-select")
        formato.click()
        time.sleep(1)
        formatoExcel = self.driver.find_element(By.XPATH, '//option[2]')
        formatoExcel.click()
        time.sleep(3)
        btnExportarFinal = self.driver.find_element(By.XPATH, "//span[@class='buttonLabel label bBody' and text()='Exportar']")
        btnExportarFinal.click()
        time.sleep(1)

        #Valida que la descarga concluya
        cantidadExcelFinal = cantidadExcelinicial
        while cantidadExcelFinal == cantidadExcelinicial:
            time.sleep(1)
            cantidadExcelFinal = self.cantidadExcel()
        else:
            pass

        time.sleep(2)
        self.driver.refresh()
        time.sleep(1)

    # --- Fin App Mi Claro CNE NC---

    # --- 3. Funcion App Mi Claro Retención Postpago Mi Claro---
    def AppMiClaroRetencionPostpago(self, fechaInicio, fechaFinal):
        wait = WebDriverWait(self.driver, 30)

        texto = f"Retención Postpago Mi Claro"
        inputBuscar = self.driver.find_element(By.XPATH, '//*[@id="oneHeader"]/div[2]/div[2]/div/button')
        inputBuscar.click()
        time.sleep(1)

        panel = self.driver.find_element(By.CSS_SELECTOR, '[class="panel-content scrollable"]')
        inputBox = panel.find_element(By.CSS_SELECTOR, '[class="slds-input"]')
        inputBox.clear()
        time.sleep(1)
        inputBox.send_keys(texto)
        time.sleep(1)
        inputBox.send_keys(Keys.RETURN)
        time.sleep(3)

        reporte = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'a[title="{texto}"]')))
        #reporte = driver.find_element(By.XPATH, f"//div[@aria-label='{texto}']")
        reporte.click()
        time.sleep(1)

        wait = WebDriverWait(self.driver, 30)
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="isView reportsReportBuilder"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isView")
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

        modificar = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Modificar']")))
        #modificar = driver.find_element(By.XPATH ,"//button[text()='Modificar']")
        modificar.click()
        time.sleep(2)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[title="Generador de informes"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isEdit")
        self.driver.switch_to.frame(iframe)
        time.sleep(3)

        filtros = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Filtros']")))
        filtros.click()
        time.sleep(2)

        elementos_fecha_creacion = self.driver.find_elements(By.XPATH, "//span[text()='Fecha de creación']")
        # -----Fecha Inicio
        primer_elemento = elementos_fecha_creacion[2]
        primer_elemento.click()
        time.sleep(2)
        btnRango = self.driver.find_element(By.XPATH, "//button[@id='undefined-list']")
        btnRango.click()
        time.sleep(2)
        mayorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-5"]/a/span')
        mayorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Seleccionar una fecha']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaInicio)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        # -----Fecha Fin
        segundo_elemento = elementos_fecha_creacion[3]
        segundo_elemento.click()
        time.sleep(2)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(2)
        menorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-4"]/a/span')
        menorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Introduzca una fecha relativa']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaFinal)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        btnEjecutar = self.driver.find_element(By.XPATH, f"//button[text()='Ejecutar']")
        btnEjecutar.click()
        time.sleep(1)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "isView")))
        self.driver.switch_to.frame(iframe)

        #img carga datos slds-spinner
        # Esperar hasta que la imagen loading ya no esté visible tiempo maximo 300seg = 5 min
        #WebDriverWait(driver, 300).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "slds-spinner")))
        totalRegistros = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Seguimiento de ventas']")))
        time.sleep(1)

        #Descarga
        cantidadExcelinicial = self.cantidadExcel()
        btnDescargar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'slds-button_icon-border') and span[text()='Más acciones']]")
        btnDescargar.click()
        time.sleep(1)

        btnExportar = self.driver.find_element(By.XPATH, f"//a[span[text()='Exportar']]")
        btnExportar.click()
        time.sleep(1)

        #salir del iframe
        self.driver.switch_to.default_content()
        
        btnExportarFinal = self.driver.find_element(By.XPATH, "//span[@class='buttonLabel label bBody' and text()='Exportar']")
        btnExportarFinal.click()
        time.sleep(1)

        #Valida que la descarga concluya
        cantidadExcelFinal = cantidadExcelinicial
        while cantidadExcelFinal == cantidadExcelinicial:
            time.sleep(1)
            cantidadExcelFinal = self.cantidadExcel()
        else:
            pass  
        time.sleep(1)

    # --- Fin App Mi Claro Retención Postpago Mi Claro---

    # --- 4. Fucion Blindaje CNE: sql - CNE+NC -(WSP+BLINDAJE+CONTACTADOS) ---
    def blindajeCNE(self, fechaInicio, fechaFinal):
        wait = WebDriverWait(self.driver, 30)

        texto = f"sql - CNE+NC -(WSP+BLINDAJE+CONTACTADOS)"
        inputBuscar = self.driver.find_element(By.XPATH, '//*[@id="oneHeader"]/div[2]/div[2]/div/button')
        inputBuscar.click()
        time.sleep(1)

        panel = self.driver.find_element(By.CSS_SELECTOR, '[class="panel-content scrollable"]')
        inputBox = panel.find_element(By.CSS_SELECTOR, '[class="slds-input"]')
        inputBox.clear()
        time.sleep(1)
        inputBox.send_keys(texto)
        time.sleep(1)
        inputBox.send_keys(Keys.RETURN)
        time.sleep(3)

        reporte = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'a[title="{texto}"]')))
        #reporte = driver.find_element(By.XPATH, f"//div[@aria-label='{texto}']")
        reporte.click()
        time.sleep(1)

        wait = WebDriverWait(self.driver, 10)
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="isView reportsReportBuilder"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isView")
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

        modificar = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Modificar']")))
        #modificar = driver.find_element(By.XPATH ,"//button[text()='Modificar']")
        modificar.click()
        time.sleep(2)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[title="Generador de informes"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isEdit")
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

        filtros = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Filtros']")))
        filtros.click()
        time.sleep(2)

        elementos_fecha_creacion = self.driver.find_elements(By.XPATH, "//span[text()='Fecha de creación']")
        # -----Fecha Inicio
        primer_elemento = elementos_fecha_creacion[1]
        primer_elemento.click()
        time.sleep(1)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(1)
        mayorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-5"]/a/span')
        mayorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Introduzca una fecha relativa']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaInicio)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        # -----Fecha Fin
        segundo_elemento = elementos_fecha_creacion[2]
        segundo_elemento.click()
        time.sleep(1)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(1)
        menorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-4"]/a/span')
        menorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Introduzca una fecha relativa']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaFinal)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        btnEjecutar = self.driver.find_element(By.XPATH, f"//button[text()='Ejecutar']")
        btnEjecutar.click()
        time.sleep(1)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "isView")))
        self.driver.switch_to.frame(iframe)

        totalRegistros = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Total de registros']")))
        time.sleep(1)

        #Descarga
        cantidadExcelinicial = self.cantidadExcel()
        btnDescargar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'slds-button_icon-border') and span[text()='Más acciones']]")
        btnDescargar.click()
        time.sleep(1)

        btnExportar = self.driver.find_element(By.XPATH, f"//a[span[text()='Exportar']]")
        btnExportar.click()
        time.sleep(1)

        #salir del iframe
        self.driver.switch_to.default_content()

        soloDetalles = self.driver.find_element(By.XPATH, "//span[text()='Solo detalles']")
        soloDetalles.click()
        time.sleep(1)

        formato = self.driver.find_element(By.CLASS_NAME, "slds-select")
        formato.click()
        time.sleep(1)
        formatoExcel = self.driver.find_element(By.XPATH, '//option[2]')
        formatoExcel.click()
        time.sleep(3)
        btnExportarFinal = self.driver.find_element(By.XPATH, "//span[@class='buttonLabel label bBody' and text()='Exportar']")
        btnExportarFinal.click()
        time.sleep(1)

        #Valida que la descarga concluya
        cantidadExcelFinal = cantidadExcelinicial
        while cantidadExcelFinal == cantidadExcelinicial:
            time.sleep(1)
            cantidadExcelFinal = self.cantidadExcel()
        else:
            pass   
        time.sleep(1)

    # --- Fin Reporte 4 ---

    # --- 5. Fucion Blindaje sql- Retención Post (Cont-bli-wsp) ---
    def blindajeCE(self, fechaInicio, fechaFinal):
        wait = WebDriverWait(self.driver, 30)

        texto = f"sql- Retención Post (Cont-bli-wsp)"
        inputBuscar = self.driver.find_element(By.XPATH, '//*[@id="oneHeader"]/div[2]/div[2]/div/button')
        inputBuscar.click()
        time.sleep(1)

        panel = self.driver.find_element(By.CSS_SELECTOR, '[class="panel-content scrollable"]')
        inputBox = panel.find_element(By.CSS_SELECTOR, '[class="slds-input"]')
        inputBox.clear()
        time.sleep(1)
        inputBox.send_keys(texto)
        time.sleep(1)
        inputBox.send_keys(Keys.RETURN)
        time.sleep(3)

        reporte = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'a[title="{texto}"]')))
        #reporte = driver.find_element(By.XPATH, f"//div[@aria-label='{texto}']")
        reporte.click()
        time.sleep(1)

        wait = WebDriverWait(self.driver, 10)
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="isView reportsReportBuilder"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isView")
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

        modificar = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Modificar']")))
        #modificar = driver.find_element(By.XPATH ,"//button[text()='Modificar']")
        modificar.click()
        time.sleep(2)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[title="Generador de informes"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isEdit")
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

        filtros = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Filtros']")))
        filtros.click()
        time.sleep(2)

        elementos_fecha_creacion = self.driver.find_elements(By.XPATH, "//span[text()='Fecha de creación']")
        # -----Fecha Inicio
        primer_elemento = elementos_fecha_creacion[2]
        primer_elemento.click()
        time.sleep(1)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(1)
        mayorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-5"]/a/span')
        mayorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Introduzca una fecha relativa']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaInicio)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        # -----Fecha Fin
        segundo_elemento = elementos_fecha_creacion[3]
        segundo_elemento.click()
        time.sleep(1)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(1)
        menorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-4"]/a/span')
        menorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Introduzca una fecha relativa']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaFinal)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        btnEjecutar = self.driver.find_element(By.XPATH, f"//button[text()='Ejecutar']")
        btnEjecutar.click()
        time.sleep(1)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "isView")))
        self.driver.switch_to.frame(iframe)

        #img carga datos slds-spinner
        # Esperar hasta que la imagen loading ya no esté visible tiempo maximo 300seg = 5 min
        WebDriverWait(self.driver, 300).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, '[class="onboard-intro"]')))
        #totalRegistros = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Seguimiento de ventas']")))
        time.sleep(2)

        #Descarga
        cantidadExcelinicial = self.cantidadExcel()
        btnDescargar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'slds-button_icon-border') and span[text()='Más acciones']]")
        btnDescargar.click()
        time.sleep(1)

        btnExportar = self.driver.find_element(By.XPATH, f"//a[span[text()='Exportar']]")
        btnExportar.click()
        time.sleep(1)

        #salir del iframe
        self.driver.switch_to.default_content()
        
        btnExportarFinal = self.driver.find_element(By.XPATH, "//span[@class='buttonLabel label bBody' and text()='Exportar']")
        btnExportarFinal.click()
        time.sleep(1)

        #Valida que la descarga concluya
        cantidadExcelFinal = cantidadExcelinicial
        while cantidadExcelFinal == cantidadExcelinicial:
            time.sleep(1)
            cantidadExcelFinal = self.cantidadExcel()
        else:
            pass
  
        time.sleep(1)


    # --- Fin Reporte 5 ---

    # --- 6. Fucion Blindaje Consolidado Retención Postpago Out ---
    def ConsolidadoRetencionPOut(self, fechaInicio, fechaFinal):
        wait = WebDriverWait(self.driver, 30)

        texto = f"Consolidado Retención Postpago Out"
        inputBuscar = self.driver.find_element(By.XPATH, '//*[@id="oneHeader"]/div[2]/div[2]/div/button')
        inputBuscar.click()
        time.sleep(1)

        panel = self.driver.find_element(By.CSS_SELECTOR, '[class="panel-content scrollable"]')
        inputBox = panel.find_element(By.CSS_SELECTOR, '[class="slds-input"]')
        inputBox.clear()
        time.sleep(1)
        inputBox.send_keys(texto)
        time.sleep(1)
        inputBox.send_keys(Keys.RETURN)
        time.sleep(3)

        reporte = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'a[title="{texto}"]')))
        #reporte = driver.find_element(By.XPATH, f"//div[@aria-label='{texto}']")
        reporte.click()
        time.sleep(1)

        wait = WebDriverWait(self.driver, 30)
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="isView reportsReportBuilder"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isView")
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

        modificar = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Modificar']")))
        #modificar = driver.find_element(By.XPATH ,"//button[text()='Modificar']")
        modificar.click()
        time.sleep(2)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[title="Generador de informes"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isEdit")
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

        #filtros = driver.find_element(By.XPATH, "//h2[text()='Filtros']")
        filtros = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Filtros']")))
        filtros.click()
        time.sleep(2)

        elementos_fecha_creacion = self.driver.find_elements(By.XPATH, "//span[text()='Fecha de creación']")
        # -----Fecha Inicio
        primer_elemento = elementos_fecha_creacion[2]
        primer_elemento.click()
        time.sleep(1)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(1)
        mayorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-5"]/a/span')
        mayorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Introduzca una fecha relativa']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaInicio)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        # -----Fecha Fin
        segundo_elemento = elementos_fecha_creacion[3]
        segundo_elemento.click()
        time.sleep(1)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(1)
        menorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-4"]/a/span')
        menorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Introduzca una fecha relativa']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaFinal)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        btnEjecutar = self.driver.find_element(By.XPATH, f"//button[text()='Ejecutar']")
        btnEjecutar.click()
        time.sleep(1)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "isView")))
        self.driver.switch_to.frame(iframe)

        #WebDriverWait(driver, 300).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "slds-spinner")))
        totalRegistros = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Seguimiento de ventas']")))
        time.sleep(1)

        #Descarga
        cantidadExcelinicial = self.cantidadExcel()
        btnDescargar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'slds-button_icon-border') and span[text()='Más acciones']]")
        btnDescargar.click()
        time.sleep(1)

        btnExportar = self.driver.find_element(By.XPATH, f"//a[span[text()='Exportar']]")
        btnExportar.click()
        time.sleep(1)

        #salir del iframe
        self.driver.switch_to.default_content()
        
        btnExportarFinal = self.driver.find_element(By.XPATH, "//span[@class='buttonLabel label bBody' and text()='Exportar']")
        btnExportarFinal.click()
        time.sleep(1)

        #Valida que la descarga concluya
        cantidadExcelFinal = cantidadExcelinicial
        while cantidadExcelFinal == cantidadExcelinicial:
            time.sleep(1)
            cantidadExcelFinal = self.cantidadExcel()
        else:
            pass
  
        time.sleep(1)

    # --- Fin Reporte 6 ---

    # --- 7. Fucion Blindaje Reporte con hora - Blindaje ---
    def blindajeReporteConHora(self, fechaInicio, fechaFinal):
        wait = WebDriverWait(self.driver, 30)

        texto = f"Reporte con hora - Blindaje"
        inputBuscar = self.driver.find_element(By.XPATH, '//*[@id="oneHeader"]/div[2]/div[2]/div/button')
        inputBuscar.click()
        time.sleep(1)

        panel = self.driver.find_element(By.CSS_SELECTOR, '[class="panel-content scrollable"]')
        inputBox = panel.find_element(By.CSS_SELECTOR, '[class="slds-input"]')
        inputBox.clear()
        time.sleep(1)
        inputBox.send_keys(texto)
        time.sleep(1)
        inputBox.send_keys(Keys.RETURN)
        time.sleep(3)

        reporte = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'a[title="{texto}"]')))
        #reporte = driver.find_element(By.XPATH, f"//div[@aria-label='{texto}']")
        reporte.click()
        time.sleep(1)

        wait = WebDriverWait(self.driver, 30)
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="isView reportsReportBuilder"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isView")
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

        modificar = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Modificar']")))
        #modificar = driver.find_element(By.XPATH ,"//button[text()='Modificar']")
        modificar.click()
        time.sleep(2)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[title="Generador de informes"]')))
        #iframe = driver.find_element(By.CLASS_NAME, "isEdit")
        self.driver.switch_to.frame(iframe)
        time.sleep(1)

        #filtros = driver.find_element(By.XPATH, "//h2[text()='Filtros']")
        filtros = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Filtros']")))
        filtros.click()
        time.sleep(2)

        elementos_fecha_creacion = self.driver.find_elements(By.XPATH, "//span[text()='Fecha de creación']")
        # -----Fecha Inicio
        primer_elemento = elementos_fecha_creacion[1]
        primer_elemento.click()
        time.sleep(1)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(1)
        mayorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-5"]/a/span')
        mayorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Introduzca una fecha relativa']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaInicio)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        # -----Fecha Fin
        segundo_elemento = elementos_fecha_creacion[2]
        segundo_elemento.click()
        time.sleep(1)
        btnRango = self.driver.find_element(By.XPATH, '//*[@id="undefined-list"]')
        btnRango.click()
        time.sleep(1)
        menorque = self.driver.find_element(By.XPATH, '//*[@id="undefined-list-item-4"]/a/span')
        menorque.click() 
        time.sleep(1)
        inputFecha = self.driver.find_element(By.XPATH, f"//input[@placeholder='Introduzca una fecha relativa']")
        inputFecha.clear()
        time.sleep(1)
        inputFecha.send_keys(fechaFinal)
        time.sleep(1)
        btnAplicar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'filter-apply')]")
        btnAplicar.click()
        time.sleep(1)

        btnEjecutar = self.driver.find_element(By.XPATH, f"//button[text()='Ejecutar']")
        btnEjecutar.click()
        time.sleep(1)

        self.driver.switch_to.default_content()
        iframe = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "isView")))
        self.driver.switch_to.frame(iframe)

        #WebDriverWait(driver, 300).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "slds-spinner")))
        totalRegistros = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Total de registros']")))
        time.sleep(1)

        #Descarga
        cantidadExcelinicial = self.cantidadExcel()
        btnDescargar = self.driver.find_element(By.XPATH, "//button[contains(@class, 'slds-button_icon-border') and span[text()='Más acciones']]")
        btnDescargar.click()
        time.sleep(1)

        btnExportar = self.driver.find_element(By.XPATH, f"//a[span[text()='Exportar']]")
        btnExportar.click()
        time.sleep(1)

        #salir del iframe
        self.driver.switch_to.default_content()
        
        soloDetalles = self.driver.find_element(By.XPATH, "//span[text()='Solo detalles']")
        soloDetalles.click()
        time.sleep(1)

        formato = self.driver.find_element(By.CLASS_NAME, "slds-select")
        formato.click()
        time.sleep(1)
        formatoExcel = self.driver.find_element(By.XPATH, '//option[2]')
        formatoExcel.click()
        time.sleep(3)
        btnExportarFinal = self.driver.find_element(By.XPATH, "//span[@class='buttonLabel label bBody' and text()='Exportar']")
        btnExportarFinal.click()
        time.sleep(1)

        #Valida que la descarga concluya
        cantidadExcelFinal = cantidadExcelinicial
        while cantidadExcelFinal == cantidadExcelinicial:
            time.sleep(1)
            cantidadExcelFinal = self.cantidadExcel()
        else:
            pass
  
        time.sleep(1)

    # --- Fin Reporte 7 ---

#descarga = descargaReportes()