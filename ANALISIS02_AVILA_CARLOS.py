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
# Obtener una tabla que contiene:
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
# esas rutas en cada año así como el valor de importación / exportación
resumean_opcion1 = opcion1_total[['mean', 'count']] total = mean*count
print(resumean_opcion1)
# Ordenar los resultados de mayor a menor
resumen_opcion1_m = resumean_opcion1.sort_values(ascending=False)

# Volver a la serie del renglón inmediato anterior, en data frame con respecto
# a uno o varios índices
resumen_opcion1 = resumen_opcion1_m.to_frame().reset_index()
# Hacemos una gráfica de barras que considere el nombre de los productos,
# el medio de transporte y el promedio de ventas
"""g = sns.barplot(x='product', y='mean', data=resumen_opcion1.head(8), hue='transport_mode')
plt.show()"""



#%% Opción 2. Enfoque en los transportes
# Obtener una tabla (.csv) que contiene:
    # Nombre del transporte usado.
    # Número de veces que se ha usado ese transporte.
    # Monto acumulado que se ha obtenido con el uso de ese transporte.


#%% Opción 3. Enfoque en los países
# Obtener dos tablas (.csv´s), ambas contienen:
    # Nombre del país.
    # Número de veces que se repite ese país en la base.
    # Monto que se emitió por país.
# Las tablas serán diferentes porque una se enfocará en el país que importa
# y la otra en el país que exporta.
