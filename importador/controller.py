# -*- coding: utf-8 -*-

import os
from util.email import Email
import json
import glob
from datetime import datetime
from service.ReportService import ReportService


mReport = ReportService()
properties = mReport.getProperties()

# Obtenemos el nombre del archivo
# filePath = r'/home/renovaciones/3ERIZA_RENOVACIONES_ALL.csv'
ROOT_PATH = properties['LOAD_PATH']

FILES_PATH = []
FILES_NOT_FOUND = []

jsonDataReports = './importador/reports.json'

with open(jsonDataReports, "r") as json_file:
    data = json.load(json_file)

    for platform in data['blindaje']:        
        # Extraemos la plataforma
        for campaign in data['blindaje'][str(platform)]:
            campana = campaign["campaign"]
                
            print('Campana : ' + campana)
            for reporte in campaign["reports"]:
                codigo = reporte["code"]
                properties = reporte["properties"]
                skipRows = reporte["skipRows"]
                useColumns = reporte["useColumns"]
                print("Reporte:", codigo)
                
                directoryPath = ROOT_PATH  + campana + "\\" +  platform + "\\" + codigo
                currentDate = datetime.now().strftime("%Y%m%d")
                #print(directoryPath)
                #currentDate = '20231030'

                # Patron de coincidencia para los nombres de archivo
                patron = f"*_{currentDate}_*"
                archivos_coincidentes = glob.glob(os.path.join(directoryPath, patron))
                #print(archivos_coincidentes)

                if(archivos_coincidentes):
                    
                    file = {
                        'name': campana + platform + "\\" + codigo + '\\' + patron,
                        'path' : archivos_coincidentes[0],
                        'table' : platform.lower() + '_' + codigo.lower(), # salesforce_1261mov1
                        'db': 'bd_claro_reportes_blindaje_' + campana.lower(),
                        'properties' : properties,
                        'skipRows': skipRows,
                        'usecolumns': useColumns
                    }
                    
                    FILES_PATH.append(file)
                else:
                    FILES_NOT_FOUND.append(campana +  platform + "\\" + codigo + '\\' + patron)

if( FILES_NOT_FOUND ):
    strFiles = '<br>'.join(FILES_NOT_FOUND)  
    print("No se encontraron archivos de reporte: " + strFiles)        
    email = Email('text')
    cc_email = {
        'cc_list' : ['soporte@qnextplus.com'],
        'bcc_list' : ['isac.delacruz@3eriza.pe']#,'michael.luque@3eriza.pe']
    }   
    email.send('Robotin - REPORTES','&#x274C; No se encontraron archivos de reporte: <br>' + strFiles,'luquemichael.92@gmail.com' ,cc_email)    
    exit()

for file in FILES_PATH:        
    result = mReport.loadData(file['path'], file['table'], file['db'], file['skipRows'], file['usecolumns'], 
                              file['properties']['dbType'], file['properties']['renameColumns'], file['properties']['converters'])

    if(result=='400'):
        email = Email('text')
        cc_email = {
            'cc_list' : ['soporte@qnextplus.com'],
            'bcc_list' : ['isac.delacruz@3eriza.pe','michael.luque@3eriza.pe']
        }   
        email.send('Robotin - REPORTES','&#x274C; Hubo un problema al importar los datos del archivo <strong>' + file['name'] + "</strong>",'luquemichael.92@gmail.com' ,cc_email) 

print("Se ejecuto correctamente todas las consultas del día ", currentDate)
exit()

#filePath = r'C:\Users\Usuario\Documents\carga\retencionesinbound\bicp\1392\retencionesInbound_bicp_1392_20230809_124738_385.xlsx'


