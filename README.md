# ¿Con base en qué diseño una estrategia operativa qeu incremente mis ingresos?
**EmTech**
_Avila Argüello Carlos_

## Objetivo.
Obtener la mejor o mejores opciones que formarán la base para crear una estrategia operativa para una empresa que es intermediaria en las exportaciones e importaciones.

## Posibles decisiones.
Las tres opciones existentes tienen enfoques en:
1. Las rutas (país de origen y destino).
2. El medio de transporte (mar, aire, etc.)
3. El país.

## Datos con los que se cuenta.
La base de datos considerada se encuentra en [este repositorio](https://github.com/emtechinstitute/data-science-proyecto2/blob/master/synergy_logistics_database.csv), dicha base contiene los datos:
- ID
- Importación o Exportación: variable dicotómica.
- Origen:
    - Desde la perspectiva de la Exportación, el origen es el nombre del país que realizó la exportación.
    - Desde la perspectiva de la Importación, el origen es el nombre del país que importó, es decir, el país al cual llegaron los productos.
- Destino:
    - Desde la perspectiva de la Exportación, el destino es el nombre del país al cuál llegaron los productos exportados, es decir, el país que importó.
    - Desde la perspectiva de la Importación, el destino es el nombre del país del cual se obtuvieron los productos importados, es decir, el país que exportó.
- Año de exportación/importación.
- Fecha exacta de la importación/exportación.
- Producto. Nombre del producto que se importó/exportó.
- Modo de transporte (carro, aire, mar).
- Compañía: nombre de la compañía a la cual pertenecen los productos.
Monto importado/exportado.

## Variables a considerar.
Se considerará la frecuencia y monto como ejes de cada opción. Es decir, 
1. El número de veces que: 
  - Se usa una ruta
  - Se usa un medio de transporte
  - Un país importa o exporta.
2. El monto total obtenido por:
  - Cada ruta usada.
  - Cada medio de transporte.
  - Cada país importador o exportador.

_Notas: dada la base de datos, es factible hacer un estudio de series de tiempo para determinar cuál de las tres estrategias tiene una predicción más favorable para las ganancias de las empresas involucradas para el 2021. Esto permitiría que haya un conocimiento más sólido en la base de la estrategía operativa._
_Dado el tiempo para la entrega del proyecto, me limito por ahora (sin demeritar) a un estudio descriptivo de estadística clásica._
