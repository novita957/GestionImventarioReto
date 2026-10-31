# [Gestion de Inventario Almacen Inteligente]

**Enlace a la app:** https://gestionimventarioreto-gzbfgt7j733fzsm9zbjfyl.streamlit.app/
**Autor/a:** Andres Novoa

## Pitch

[La vendedora de un pequeño almacén de barrio gestiona su inventario a mano, lo que le provoca constantes errores de stock y pérdida de información sobre lo que realmente tiene disponible. Esta aplicación web en Streamlit automatiza por completo el registro de entradas y salidas de mercancía a través de formularios intuitivos y seguros. La Inteligencia Artificial de Gemini actúa como un asistente experto al que la vendedora puede preguntarle de forma natural sobre el estado de sus productos sin necesidad de entender de hojas de cálculo. Durante las pruebas, confirmamos que una interfaz limpia con alertas automáticas de stock mínimo evita la escasez de productos críticos. En el futuro, planeamos integrar estadísticas predictivas que le sugieran qué productos comprar segùn la temporada.]

## El problema

[La vendedora del almacén realiza todo el control de stock anotando en un cuaderno cada venta y cada llegada de mercadería. Este método manual consume mucho tiempo, es propenso a errores humanos de cálculo y dificulta encontrar rápidamente la disponibilidad o el precio de un artículo específico ante una consulta de un cliente. Resolver este problema es fundamental para evitar la pérdida de ventas por falta de mercadería y optimizar el capital de trabajo del negocio, permitiendo un control transparente, rápido y sin complicaciones.]

## Qué hace la app

[El usuario (la vendedora) puede realizar las siguientes acciones paso a paso:

Ingreso de Productos: Registra productos nuevos especificando su nombre, cantidad inicial y precio a través de un formulario dedicado con validaciones en tiempo real.
Modificación de Stock: Si un producto ya existe en el almacén, puede reabastecerlo fácilmente usando la opción dedicada para actualizar sus cantidades y precios sin duplicar registros.
Salida de Productos: Da salida a productos vendidos seleccionándolos desde un menú desplegable, lo que previene errores de escritura, descontando de forma automática las unidades del stock.
Monitoreo de Inventario: Visualiza una tabla con todo el inventario consolidado y un gráfico de barras estático para identificar de forma rápida qué productos tienen mayor disponibilidad.
Alertas de Stock Bajo: Revisa de manera constante la barra lateral de la app, donde se muestra un panel crítico destacado en color rojo con aquellos productos que tengan 5 o menos unidades disponibles.
Consulta Inteligente: Interactúa con un chat interactivo donde puede escribir libremente preguntas sobre su stock (ej. "¿cuál es el precio de la leche y cuántas unidades me quedan?") y recibir respuestas inmediatas basadas estrictamente en la realidad del inventario.]

## La pieza de IA

- **Qué usa:** [API de Gemini (gemini-2.5-flash-lite) mediante el SDK oficial de Python google-genai con un prompt de sistema restrictivo que le provee el archivo CSV actual como contexto ónico en cada mensaje.]
- **Por qué esa opción:** [Ofrece un procesamiento del lenguaje natural sumamente rápido, adaptado a la capa gratuita del servicio, ideal para brindar respuestas instantáneas a la vendedora sin agregar costes de infraestructura.]
- **Qué pasa si falla:** [El sistema está protegido por bloques de excepción (try/except). Si la API experimenta problemas de timeout o falta de cuota, la app despliega un aviso claro e instructivo en la interfaz para la vendedora, garantizando que los formularios convencionales de entrada/salida y las tablas sigan funcionando normalmente sin interrumpir la operación del almacén]

## Cómo la he construido

- **Herramientas:** [Gemini en Colab, Copilot, Cursor, Claude Code, Codex, Gemini CLI…]
- **Fichero de contexto del agente:** [AGENTS.md]
- **Prompts clave:** [1) Actúa como un asistente de almacén amigable y sencillo. Tu ùnico objetivo es responder preguntas de la vendedora basándote ùnicamente en el siguiente inventario que te adjunto en formato texto: [inventario_csv]. No inventes datos ni asumas información que no esté en este texto.
2) Si la pregunta de la vendedora está fuera del contexto del inventario del almacén (por ejemplo, preguntas generales, recetas o tareas que no competen a la gestión de productos), responde amablemente que solo estás capacitado para asistir con las dudas del inventario del almacén.
3) Si el usuario te saluda o agradece, mantén una conversación cordial y breve, recordándole de manera servicial que estás listo para informarle sobre el estado de sus productos."]
- **Qué delegué al agente y qué revisé a mano:** [ Delegué al agente la generación de la estructura inicial del chat en Streamlit y la integración de la llamada a la API de Gemini usando el SDK actualizado. Revisé minuciosamente a mano las funciones de validación de entradas de stock para asegurar de forma estricta que no se admitan números menores o iguales a cero y que se bloqueen efectivamente las transacciones de salida cuando no hay stock suficiente]

## Prueba y mejora

| Quién la probó         | Qué probó           | Qué pasó                       | Qué cambié                                          |
| Luis Rodas (Compañero) | Ingreso de producto | Pudo ingresar un producto en 0 | Le agregue un validador que no permita producto en 0|


## Ejecutar en local (opcional)

```bash
pip install -r requirements.txt
# Ruta A: poned la clave en .streamlit/secrets.toml y ejecutad
streamlit run app.py
# Ruta B: exportad la clave y ejecutad
export GEMINI_API_KEY="…" && python app.py
```

## Capturas

[La app funcionando, la app ante un caso límite, un momento de vuestro trabajo con la IA y la prueba. Sin ninguna clave a la vista.]