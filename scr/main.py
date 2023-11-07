from web_scraper import descargaReportes
from isdb import TablaValidacion
import datetime
import json
import time
import sqlite3

#Rango de fechas para descarga de Reportes ***** (ojo con el formato) *****
D0 =  datetime.date.today()
D_1 =  D0 + datetime.timedelta(days=-1)
inicio = '03/11/2023' #D_1.strftime("%d/%m/%Y") #'10/09/2023'
fin = D_1.strftime("%d/%m/%Y") #inicio #None #'11/09/2023'

username = "e8232991@claro.com.pe"
password = "3eriza2023**"

tablaValidacion = TablaValidacion()
tablaValidacion.crearBD()
tablaValidacion.crearTabla()
tablaValidacion.truncateTable()

descargaTotal = True

descarga = descargaReportes()
def logueo():
    descarga.login()
    descarga.iniciarSesion(username, password)
    inicioSesion = descarga.validaInicioSesion()

    while not inicioSesion:
        descarga.reiniciar()
        descarga.login()
        descarga.iniciarSesion(username, password)
        inicioSesion = descarga.validaInicioSesion()
    else:
        print('Inicio de Sesion Exitosa')
        pass

logueo()

fecD0 = False
contador_descargas = 1

# ===== I. App Mi Claro =====
campana = "AppMiClaro"
# 1. CNe_Nc
def app_claro_cne_nc():
    try:
        descarga.AppMiClaroCNeNc(inicio, fin)
        nombreAsignado = 'AppMiClaroCNeNc_SalesForce_'
        nombre = descarga.nombreReporte(nombreAsignado, inicio, fin, fecD0)
        destino = descarga.directoryPath + r'/carga\AppMiClaro\salesForce\CNe_Nc'
        descarga.renombrarReubicar(nombre, destino)

        datos=[(contador_descargas, campana, nombreAsignado, 1)]
        tablaValidacion.agregarVariosDatos(datos)

    except Exception as e:
        nombreAsignado = 'AppMiClaroCNeNc_SalesForce_'
        datos=[(contador_descargas, campana, nombreAsignado, 0)]
        tablaValidacion.agregarVariosDatos(datos)
        pass

app_claro_cne_nc()
ultimoRegistro = tablaValidacion.leerDatos()
descargo = ultimoRegistro[0][3]

while descargo == 0:
    tablaValidacion.deleteTable(contador_descargas)

    descarga.reiniciar()
    logueo()

    app_claro_cne_nc()
    ultimoRegistro = tablaValidacion.leerDatos()
    descargo = ultimoRegistro[0][3]
else:
    contador_descargas += 1
    pass

# 2. Retencion Postpago 
def app_claro_retencion_postpago():
    try:
        descarga.AppMiClaroRetencionPostpago(inicio, fin)
        nombreAsignado = 'AppMiClaroRetencionPostpago_SalesForce_'
        nombre = descarga.nombreReporte(nombreAsignado, inicio, fin, fecD0)
        destino = descarga.directoryPath + r'/carga\AppMiClaro\salesForce\Retencion_Postpago'
        descarga.renombrarReubicar(nombre, destino)

        datos=[(contador_descargas, campana, nombreAsignado, 1)]
        tablaValidacion.agregarVariosDatos(datos)

    except Exception as e:
        nombreAsignado = 'AppMiClaroRetencionPostpago_SalesForce_'
        datos=[(contador_descargas, campana, nombreAsignado, 0)]
        tablaValidacion.agregarVariosDatos(datos)
        pass

app_claro_retencion_postpago()
ultimoRegistro = tablaValidacion.leerDatos()
descargo = ultimoRegistro[0][3]

while descargo == 0:
    tablaValidacion.deleteTable(contador_descargas)

    descarga.reiniciar()
    logueo()

    app_claro_retencion_postpago()
    ultimoRegistro = tablaValidacion.leerDatos()
    descargo = ultimoRegistro[0][3]
else:
    contador_descargas += 1
    pass

# ===== II. Blindaje =====
campana = "blindaje"
# 1. blindaje_Reporte_Con_Hora
def blindaje_reporte_hora():
    try:
        descarga.blindajeReporteConHora(inicio, fin)
        nombreAsignado = 'blindajeReporteConHora_SalesForce_'
        nombre = descarga.nombreReporte(nombreAsignado, inicio, fin, fecD0)
        destino = descarga.directoryPath + r'/carga\blindaje\salesForce\blindaje_Reporte_Con_Hora'
        descarga.renombrarReubicar(nombre, destino)

        datos=[(contador_descargas, campana, nombreAsignado, 1)]
        tablaValidacion.agregarVariosDatos(datos)

    except Exception as e:
        nombreAsignado = 'blindajeReporteConHora_SalesForce_'
        datos=[(contador_descargas, campana, nombreAsignado, 0)]
        tablaValidacion.agregarVariosDatos(datos)
        pass

blindaje_reporte_hora()
ultimoRegistro = tablaValidacion.leerDatos()
descargo = ultimoRegistro[0][3]

while descargo == 0:
    tablaValidacion.deleteTable(contador_descargas)

    descarga.reiniciar()
    logueo()

    blindaje_reporte_hora()
    ultimoRegistro = tablaValidacion.leerDatos()
    descargo = ultimoRegistro[0][3]
else:
    contador_descargas += 1
    pass

# 2. blindaje_Retenciones
def blindaje_retenciones():
    try:
        descarga.reporteBlindaje(inicio, fin)
        nombreAsignado = 'blindaje_Retenciones_SalesForce_'
        nombre = descarga.nombreReporte(nombreAsignado, inicio, fin, fecD0)
        destino = descarga.directoryPath + r'/carga\blindaje\salesForce\blindaje_Retenciones'
        descarga.renombrarReubicar(nombre, destino)

        datos=[(contador_descargas, campana, nombreAsignado, 1)]
        tablaValidacion.agregarVariosDatos(datos)

    except Exception as e:
        nombreAsignado = 'blindaje_Retenciones_SalesForce_'
        datos=[(contador_descargas, campana, nombreAsignado, 0)]
        tablaValidacion.agregarVariosDatos(datos)
        pass

blindaje_retenciones()
ultimoRegistro = tablaValidacion.leerDatos()
descargo = ultimoRegistro[0][3]

while descargo == 0:
    tablaValidacion.deleteTable(contador_descargas)

    descarga.reiniciar()
    logueo()

    blindaje_retenciones()
    ultimoRegistro = tablaValidacion.leerDatos()
    descargo = ultimoRegistro[0][3]
else:
    contador_descargas += 1
    pass

# 3. CE
def blindaje_ce():
    try:
        descarga.blindajeCE(inicio, fin)
        nombreAsignado = 'Ce_RetencionPost(Cont-bli-wsp)_SalesForce_'
        nombre = descarga.nombreReporte(nombreAsignado, inicio, fin, fecD0)
        destino = descarga.directoryPath + r'/carga\blindaje\salesForce\CE'
        descarga.renombrarReubicar(nombre, destino)

        datos=[(contador_descargas, campana, nombreAsignado, 1)]
        tablaValidacion.agregarVariosDatos(datos)

    except Exception as e:
        nombreAsignado = 'Ce_RetencionPost(Cont-bli-wsp)_SalesForce_'
        datos=[(contador_descargas, campana, nombreAsignado, 0)]
        tablaValidacion.agregarVariosDatos(datos)
        pass

blindaje_ce()
ultimoRegistro = tablaValidacion.leerDatos()
descargo = ultimoRegistro[0][3]

while descargo == 0:
    tablaValidacion.deleteTable(contador_descargas)

    descarga.reiniciar()
    logueo()

    blindaje_ce()
    ultimoRegistro = tablaValidacion.leerDatos()
    descargo = ultimoRegistro[0][3]
else:
    contador_descargas += 1
    pass

# 4. CNE_NC
def blindaje_cne_nc():
    try:
        descarga.blindajeCNE(inicio, fin)
        nombreAsignado = 'Cne_Nc_(WSP+BLINDAJE+CONTACTADOS)_SalesForce_'
        nombre = descarga.nombreReporte(nombreAsignado, inicio, fin, fecD0)
        destino = descarga.directoryPath + r'/carga\blindaje\salesForce\CNE_NC'
        descarga.renombrarReubicar(nombre, destino)

        datos=[(contador_descargas, campana, nombreAsignado, 1)]
        tablaValidacion.agregarVariosDatos(datos)

    except Exception as e:
        nombreAsignado = 'Cne_Nc_(WSP+BLINDAJE+CONTACTADOS)_SalesForce_'
        datos=[(contador_descargas, campana, nombreAsignado, 0)]
        tablaValidacion.agregarVariosDatos(datos)
        pass

blindaje_cne_nc()
ultimoRegistro = tablaValidacion.leerDatos()
descargo = ultimoRegistro[0][3]

while descargo == 0:
    tablaValidacion.deleteTable(contador_descargas)

    descarga.reiniciar()
    logueo()

    blindaje_cne_nc()
    ultimoRegistro = tablaValidacion.leerDatos()
    descargo = ultimoRegistro[0][3]
else:
    contador_descargas += 1
    pass

# 5. Cons_Ret_Post_out
def blindaje_cons_ret_post_out():
    try:
        descarga.ConsolidadoRetencionPOut(inicio, fin)
        nombreAsignado = 'ConsolidadoRetencionPostpagoOut_SalesForce_'
        nombre = descarga.nombreReporte(nombreAsignado, inicio, fin, fecD0)
        destino = descarga.directoryPath + r'/carga\blindaje\salesForce\Cons_Ret_Post_out'
        descarga.renombrarReubicar(nombre, destino)

        datos=[(contador_descargas, campana, nombreAsignado, 1)]
        tablaValidacion.agregarVariosDatos(datos)

    except Exception as e:
        nombreAsignado = 'ConsolidadoRetencionPostpagoOut_SalesForce_'
        datos=[(contador_descargas, campana, nombreAsignado, 0)]
        tablaValidacion.agregarVariosDatos(datos)
        pass

blindaje_cons_ret_post_out()
ultimoRegistro = tablaValidacion.leerDatos()
descargo = ultimoRegistro[0][3]

while descargo == 0:
    tablaValidacion.deleteTable(contador_descargas)

    descarga.reiniciar()
    logueo()

    blindaje_cons_ret_post_out()
    ultimoRegistro = tablaValidacion.leerDatos()
    descargo = ultimoRegistro[0][3]
else:
    contador_descargas += 1
    pass

descarga.cerrarSesion()
descarga.gameOver()
print("Descarga Exitosa")

