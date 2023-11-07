from web_scraper import descargaReportes
import datetime
import json
import time
import sqlite3
from isdb import TablaValidacion

fecha_inicio = datetime.datetime(2023, 10, 12)
fecha_fin = datetime.datetime(2023, 10, 26)
lista_fechas = []
inicio = fecha_inicio.strftime('%Y-%m-%d')

while fecha_inicio <= fecha_fin:
    lista_fechas.append(fecha_inicio.strftime('%Y-%m-%d'))
    fecha_inicio += datetime.timedelta(days=1)

tablaValidacion = TablaValidacion()
tablaValidacion.crearBD()
tablaValidacion.crearTabla()
tablaValidacion.truncateTable()

descargaTotal = True


username = "isac.delacruz@3eriza.pe"
password = "47935979"

descarga = descargaReportes()
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

while descargaTotal:
    for fecha in lista_fechas:
        try:
            #Rango de fechas para descarga de Reportes
            D0 =  datetime.date.today()
            D_1 =  D0 + datetime.timedelta(days=-1)
            inicio = str(fecha) #'2023-08-04'
            fin = inicio #None#'2023-08-08'

            # 1. ReclamoOperacionesV1
            fecD0 = False
            descarga.reclamosOperacionV1(inicio, fin)
            nombreAsignado = 'lineaUno_reclamosOperacionesV1_'
            nombre = descarga.nombreReporte(nombreAsignado, inicio, fin, fecD0)
            destino = descarga.directoryPath + r'/carga\lineaUno\lineaUno\reclamosOperacionesV1'
            descarga.renombrarReubicar(nombre, destino)

            datos=[(fecha, 1)]
            tablaValidacion.agregarVariosDatos(datos)
        except Exception as e:
            datos=[(fecha, 0)]
            tablaValidacion.agregarVariosDatos(datos)
            pass

        ultimoRegistro = tablaValidacion.leerDatos()
        descargo = ultimoRegistro[0][1]

        while descargo == 0:
            tablaValidacion.deleteTable(fecha)

            descarga.reiniciar()
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
            
            try:
                #Rango de fechas para descarga de Reportes
                D0 =  datetime.date.today()
                D_1 =  D0 + datetime.timedelta(days=-1)
                inicio = str(fecha) #'2023-08-04'
                fin = inicio #None#'2023-08-08'

                # 1. ReclamoOperacionesV1
                fecD0 = False
                descarga.reclamosOperacionV1(inicio, fin)
                nombreAsignado = 'lineaUno_reclamosOperacionesV1_'
                nombre = descarga.nombreReporte(nombreAsignado, inicio, fin, fecD0)
                destino = descarga.directoryPath + r'/carga\lineaUno\lineaUno\reclamosOperacionesV1'
                descarga.renombrarReubicar(nombre, destino)

                datos=[(fecha, 1)]
                tablaValidacion.agregarVariosDatos(datos)
            except Exception as e:
                datos=[(fecha, 0)]
                tablaValidacion.agregarVariosDatos(datos)
                pass

            ultimoRegistro = tablaValidacion.leerDatos()
            descargo = ultimoRegistro[0][1]
        else:
            pass

        ultimoRegistro = tablaValidacion.leerDatos()
        ultimaFechaInsertada = ultimoRegistro[0][0]

        if ultimaFechaInsertada != lista_fechas[-1]:
            descargaTotal = True
        else:
            descargaTotal = False

descarga.cerrarSesion()



