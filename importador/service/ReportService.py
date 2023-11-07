# -*- coding: utf-8 -*-
import pandas as pd
import pymysql
import json
from datetime import datetime
import warnings

class ReportService:

    def loadData(self,filePath, tableName : str, dbName : str, skipRows, useColumns,properties : {}, renameColumns : {}, converters : []):
        filePath = filePath

        # Nombre de la tabla
        dbTable = tableName

        percentage = {}
        for convert in converters:
            percentage[convert] = self.convertToPercentage
            
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
             # Lee el archivo EXCEL con pandas
            df = pd.read_excel( filePath,  sheet_name=0, engine='openpyxl', skiprows=skipRows, usecols=useColumns, dtype=properties, converters=percentage)
        df = df.dropna(how='all') #elimina las filas nulas del dataframe
        df = df.filter(regex='^(?!Unnamed)') #elimina columnas sin nombre que se generan porque el excel tiene columnas combinadas
        # --- Elimina fila total y la que le sigue ---
        df = df.dropna(how='all')
        df.iloc[:, 0] = df.iloc[:, 0].astype(str)
        mask = (df.iloc[:, 0] == 'Total')
        if any(mask):
            index = df.index[mask][0]
            df = df.loc[:index - 1]
        df = df.loc[~(df.iloc[:, 0] == 'Total')]
        df.iloc[:, 0] = df.iloc[:, 0].replace('nan', '', regex=False)
        # --- * ---

        # Renombrar la columna        
        df.columns = df.columns.str.strip()
        df.rename(columns=renameColumns, inplace=True)


        # Formatear las columnas
        df = df.fillna(value='')
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace('\n', '')
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

        #print(df.columns)
        #exit()

        # Configurar la conexión a la base de datos
        properties = self.getProperties()
        conn = pymysql.connect(
            host=properties['DB_HOST'],
            database= dbName,
            user=properties['DB_USER'],
            password=properties['DB_PASSWORD'],
            port=3306
        )

        try:
            # Crear un cursor y comenzar una transacción
            cur = conn.cursor()
            cur.execute("START TRANSACTION;")

            sqlHeading = "`"+"`,`".join(df.columns)+"`"

            chunks = [df[i:i + 200] for i in range(0, df.shape[0], 200)]   
            
            for chunk in chunks:
                values = [tuple(row) for _, row in chunk.iterrows()]
                try:
                    # Ejecutar el comando INSERT INTO para cada grupo de 50 filas
                    consulta = f"""INSERT INTO {dbTable} ({sqlHeading}) VALUES ({', '.join(['%s'] * len(df.columns))});"""
                    cur.executemany(consulta, values)
                    conn.commit()
                    #print(f"Se insertaron con éxito {len(chunk)} filas")
                except Exception as e:
                    print("Ocurrió un error:", e)  
            
            print('Se ejecuto correctamente la consulta: ' + dbName + " / " + tableName)

        except Exception as e:
            # Revertir la transacción si hay un error            
            conn.rollback()    
            print("Hubo un error al importar la informacion: " + str(e) )
            return 400 
            
        finally:
            # Cerrar la conexión a la base de datos
            cur.close()
            conn.close()

        return 200
    
    def getProperties(self):
        config_data = None
        with open('./importador/config.json') as config_file:
            config_data = json.load(config_file)

        return config_data
    
    def convertToPercentage(self,x):
        return "{:.2f}%".format(x * 100)