# Especificación · Gestion de Inventario

> Se requiere una aplicacion en Python con Streamlit el cual pueda manejar el inventario de un pequeño almacena que maneja productos, donde se debe ingresar productos, salida de productos y consulta de prodocutos con librerias de grafico pueda determinar cuantos productos dispongo en almacen. 
El gráfico muestra el stock absoluto actual de todos los productos del almacén de forma estática
Para manejar la persistencia de datos se debe utilizar un archivo csv maneje las columnas nombre_producto, cantidad y precio, que maneje los productos, solo responda basándose en los datos reales del CSV
El usuario interactúa únicamente con formularios tradicionales para ingresar/sacar productos, y usa un chat con Gemini exclusivo para consultar dudas sobre el inventario.
Para productos existen se debe añadir una opción o botón de "Modificar/Editar Stock asi se genera el ingreso
 
## 1. Problema y usuario

- **Quién tiene el problema: [Vendedora]
- **Cómo lo resuelve hoy: [a mano]
- **Qué le molesta de cómo lo hace hoy:** [errores, no encuentra la información]
- **Qué parte resuelve la IA:** [la vendedora interactua con un chat de lenguaje natural y se debe tener un menu desplegable con los productos]

## 2. Qué hace el producto

Máximo tres funcionalidades. Si hay más, van al apartado 8.

1. [Ingresa productos]
2. [Salida productos]
3. [Consulta de Inventario]

## 3. Entradas y salidas
[El usuario podra ingresar un producto, donde puede especificar nombre del producto, numero de productos a ingresar y precio. Como salida se debe disponer del inventarios y un grafico con los productos disponibles]

## 4. La pieza de IA

- **Opción elegida:** [API de un LLM (Gemini)]
- **Por qué:** [por acceso rapido y porque me acomoda]
- **Instrucciones para el modelo (system prompt):** [cómo debe comportarse, tono, qué no debe hacer]

## 5. Flujo del usuario

1. [ingresar al modulo de ingreso de producto e ingresar o sacar productos]
2. [usuario podra revisar el stock de productos y un grafico de apoyo visual]
3. [en caso que el producto este con un limite de stock de 5 unidades entregara una advertencia de productos con stock menor o igual a 5 esté siempre visible en la barra lateral (sidebar) como un resumen crítico]

## 6. Restricciones

- Coste cero: capa gratuita de la API y despliegue gratuito (ruta A).
- La clave de la API va en secretos, nunca en el código.
- Sin datos personales reales.
- Lenguaje sencillo, para alguien sin conocimientos técnicos.
- [Otras restricciones de vuestro problema]

## 7. Criterios de aceptación

La app está bien si:

| Entrada | Resultado esperado |
|---|---|
| [caso normal] | [qué debe pasar] |
| [caso límite: salida sin stock] | [se debe indicar en un mensaje en rojo no hay stock y bloquear transaccion] |
| [caso límite: ingreso duplicado] | [se debe indicar en un mensaje en rojo no producto ya existe y bloquear transaccion] |
| [caso límite: precio y cantiddad bajo 0] | [se debe indicar en un mensaje en rojo no producto tiene un precio 0 y no tiene stock, y se debe impedir el envio de la informacion] |
| [caso límite: nombres idénticos] | [se debe tratar como un producto] |
| [error: timeout] | [error en timeout] |


## 8. Fuera de alcance (por ahora)

- [Ideas que dejáis para después]

## 9. Despliegue

- **Ruta:** [A (Streamlit Community Cloud)]
- **Si trabajáis en equipo (opcional):** []