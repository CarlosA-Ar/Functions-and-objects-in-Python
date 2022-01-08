"""
Proyecto 02. Análisis de las opciones que conformarían la base para crear la 
estrategia operativa de "Synergy Logistics".

Carlos Avila Argüello
EmTech

Recomendación a quien leerá el código: plegar las pestañas (si usas Spyder)
para el mejor entendimiento. La estructura del código está básicamente dividida
en tres partes, cada una contiene el código para obtener resultados que nos faciliten
decidir qué opción(opciones) es(son) mejor(es).
"""
#%% Importar los módulos que usaré para el análisis
# Para trabajar con dataframes:
import pandas as pd # pd es el alias de pandas
import numpy as np # para poder realizar operaciones entre columnas
# Para trabajar con gráficas:
import seaborn as sns
import matplotlib.pyplot as plt

#%% Importar los datos:
# Leer el csv...
synergy_dataframe = pd.read_csv('synergy_logistics_database.csv', 
                                index_col=0, # ...donde cada renglón se indexe 
                                # con el id de la tabla,
                                encoding='utf-8', # se lean los caractetres 
                                # especiales sin problemas y
                                parse_dates=[5]) # se indique que la columna
                                # 6 deben ser consideradas como fechas.

#%% Opción 1. Enfque en las rutas
# Obtener tablas que contengan:
    # Nombre de la ruta que se recorre (país origen -> país destino).
    # Número de veces que se ha recorrido esa ruta.
    # Monto acumulado en esa ruta.
    
# 1. Obtener los tríos únicos de synergy_dataframe:
opcion1 = synergy_dataframe.groupby(by=['year',
                                        'direction',
                                        'origin',
                                        'destination'])
# 2. Describir (estadísticamente) el valor total de las importaciones
# o exportaciones de la tabla anterior.
opcion1_total = opcion1.describe()['total_value']
# Obtener en particular, cuantas importaciones / exportaciones se han hecho en
# esas rutas en cada año así como el valor medio de importación / exportación
resumen_opcion1 = opcion1_total[['mean', 'count']]

# A partir de lo anterior, obtener una lista del total de exportaciones.
mean = resumen_opcion1.iloc[:,0].tolist()
count = resumen_opcion1.iloc[:,1].tolist()
total = np.array(mean)*np.array(count)

# Añadir al cuadro resumen, el total y quitar la media
resumen_opcion1.insert(2, # que se ponga la columna en el índice 2 
                       "total", # que el nombre de la columna sea "total"
                       total) # que los datos de la columna sean de la lista "total"
resumen_opcion1 = resumen_opcion1.drop(['mean'], # quitamos la columna que se llama "mean" 
                     axis = 1) # con este número se indica que se quite "la columna"

# Volver a la serie del renglón inmediato anterior, en data frame con respecto
# a uno o varios índices
resumen_opcion1 = resumen_opcion1.reset_index()

# Ordenar los resultados de mayor a menor valor total en grupos anuales
resumen_opcion1 = resumen_opcion1.sort_values(['year', 'total', 'count'],ascending = False)

# Hacer la extracción de los primeros 10 valores para cada año, 
# hacer una función que nos devuelva un diccionario con dos tablas cada una de 
# las cuales contiene las primeras 10 rutas con respecto al valor total de 
# 1. exp: exportacion y 2. imp: importacion.
def tener_resumen_opcion1(anio):
    datos_anio = resumen_opcion1[(resumen_opcion1['year'] == anio)].copy()
    exports_anio = datos_anio[(resumen_opcion1['direction'] == 'Exports')].copy().head(10)
    imports_anio = datos_anio[(resumen_opcion1['direction'] == 'Imports')].copy().head(10)
    return {'exp': exports_anio, 'imp': imports_anio}

# Generamos un archivo de excel donde cada hoja contendrá el dataframe con las
# primeras 10 rutas usadas en un año, ya sea para importación o exportación.
# Esto con el objetivo de graficar los resultados.
escrito = pd.ExcelWriter('resultados_por_rutas.xlsx')

for anio in range(2015, 2020 + 1):
    # Escribir una hoja para las exportaciones de cada año
    tener_resumen_opcion1(anio)['exp'].to_excel(escrito,'Exportación' + str(anio))
    # Escribir una hoja para las importaciones de cada año
    tener_resumen_opcion1(anio)['imp'].to_excel(escrito,'Importación' + str(anio))

# Guardamos el excel con las 12 hojas
escrito.save()

# Ver los resultados en el reporte. Pueden ser consultados con el siguiente código comentado:
"""
resultados_opcion1_exp = []
resultados_opcion1_imp = []
for anio in rango(2015,2020+1):
    resultados_opcion1_exp.append(tener_resumen_opcion1(anio)['exp'])
    resultados_opcion1_imp.append(tener_resumen_opcion1(anio)['imp'])
Para ver la tabla de resultados de las rutas con mayor ganancia en exportaciones
del año 2015:
    print(resultados_opcion1_exp[0])
"""
#%% Opción 2. Enfoque en los transportes
# Obtener una gráfica que presente la evolución de las ventas a lo largo del tiempo
# por medio de transporte.

# Copiar los datos en una tabla para no modificar los originales
datos2 = synergy_dataframe.copy()
# Obtener para cada año, los meses en número, luego guardar ese dato para cada
# trnasacción (importación / exportación) y guardar esos datos en una nueva columna
datos2['anio_mes'] = datos2['date'].dt.strftime('%Y-%m')
# Agrupar los datos por mes (y por año) así como por medio de transporte.
datos_anio_mes = datos2.groupby(['anio_mes', 'transport_mode'])
# Para los datos agrupados, obtenemos las veces que se repote el valor total y 
# la suma. En forma de dataframe y siendo los índices, parte de la tabla.
frecuencia2 = datos_anio_mes.count()['total_value'].to_frame().reset_index()
total2 = datos_anio_mes.sum()['total_value'].to_frame().reset_index()
# Para cada mes, se obtiene el transporte para cada uno de los cuales, 
# se obtiene la frecuencia (número de veces que se usa ese transporte) y el total.
frecuencia2 = frecuencia2.pivot('anio_mes', 'transport_mode', 'total_value')
total2 = total2.pivot('anio_mes', 'transport_mode', 'total_value')
# Usar el módulo seaborn para generar una gráfica con la frecuencia del tranporte
# y otra con la ganancia por su uso:
#sns.lineplot(data=frecuencia2)
sns.lineplot(data=total2)
plt.xticks(rotation = 60, ticks = None, labels = None)

sns.lineplot(data=frecuencia2)
plt.xticks(rotation = 60, ticks = None, labels = None)

#%% Opción 3. Enfoque en los países
# Obtener dos tablas (.csv´s), ambas contienen:
    # Nombre del país.
    # Número de veces que se repite ese país en la base.
    # Monto que se emitió por país.
# Las tablas serán diferentes porque una se enfocará en el país que importa
# y la otra en el país que exporta.

# 1. Obtener los dúos únicos de synergy_dataframe:
opcion3 = synergy_dataframe.groupby(by=['year',
                                        'origin'])
# 2. Describir (estadísticamente) el valor total de los movimientos
# de la tabla anterior.
opcion3 = opcion3.describe()['total_value']
# Obtener en particular, cuantas operaciones se han hecho en estos países
# cada año así como el valor medio de operación
resumen_opcion3 = opcion3[['mean', 'count']]

# A partir de lo anterior, obtener una lista del total de exportaciones.
mean3 = resumen_opcion3.iloc[:,0].tolist()
count3 = resumen_opcion3.iloc[:,1].tolist()
total3 = np.array(mean3)*np.array(count3)

# Añadir al cuadro resumen, el total y quitar la media
resumen_opcion3.insert(2, # que se ponga la columna en el índice 2 
                       "total", # que el nombre de la columna sea "total"
                       total3) # que los datos de la columna sean de la lista "total"
resumen_opcion3 = resumen_opcion3.drop(['mean'], # quitamos la columna que se llama "mean" 
                     axis = 1) # con este número se indica que se quite "la columna"

# Volver a la serie del renglón inmediato anterior, en data frame con respecto
# a uno o varios índices
resumen_opcion3 = resumen_opcion3.reset_index()

# Ordenar los resultados de mayor a menor valor total en grupos anuales
resumen_opcion3 = resumen_opcion3.sort_values(['year', 'total', 'count'],
                                              ascending = False)

# Hacer la extracción de los primeros países para cada año, 
# hacer una función que nos devuelva una tabla que contiene los principales
# países que generan el 80% de los ingrersos en cada año.
def tener_resumen_opcion3(anio):
    datos = resumen_opcion3[(resumen_opcion3['year'] == anio)].copy()
    # Poner una columna del porcentaje que representa cada país en cuanto
    # al total de ingresos.
    datos.insert(4, "prop_por_pais", datos["total"]/sum(datos["total"])*100)
    #Llenar un dataframe con los datos que generen el 80% de ingreso
    prop_acumulada = 0
    resumen = pd.DataFrame()
    for i in range(datos.shape[0]):
        if prop_acumulada <= 80:
            resumen = resumen.append(datos.iloc[i,:], ignore_index=True)
            prop_acumulada += datos.iloc[i, 4]
    return resumen

# Generamos un archivo de excel donde cada hoja contendrá el dataframe con los
# principales países que representen hasta el 80% de los ingresos por cada año.
escrito1 = pd.ExcelWriter('resultados_por_pais.xlsx')
for anio in range(2015, 2020 + 1):
    # Escribir una hoja para las exportaciones de cada año
    tener_resumen_opcion3(anio).to_excel(escrito1,'Países ' + str(anio))

# Guardamos el excel con las 6 hojas
escrito1.save()

# Ver los resultados en el reporte. Pueden ser consultados con el siguiente código comentado:
"""
resultados_opcion3 = []
for anio in rango(2015,2020+1):
    resultados_opcion3.append(tener_resumen_opcion3(anio))
Para ver la tabla de resultados de los países con mayor ganancia en el año 2015:
print(resultados_opcion3[0])
"""