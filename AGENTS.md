# AGENTS.md · Gestión de Inventario para Almacén

> Este fichero lo leen los agentes de programación (Copilot, Cursor, Codex, Gemini CLI y otros) antes de tocar vuestro código. Para Claude Code, cread un `CLAUDE.md` con una sola línea: `Sigue las instrucciones de AGENTS.md`. Para Gemini CLI, haced lo mismo con `GEMINI.md`.

## Qué es este proyecto

Una aplicación web interactiva en Python con Streamlit diseñada para ayudar a una vendedora de un pequeño almacén a gestionar el inventario de sus productos de forma sencilla, evitando errores manuales y facilitando consultas rápidas sobre el stock real mediante un chat de Inteligencia Artificial.

## Cómo está hecho

- Python 3.12.
- Interfaz: Streamlit (Ruta A).
- IA: API de Gemini con el SDK `google-genai`. El modelo está en la constante `MODELO` de `app.py`.
- Persistencia: Archivo local CSV (`inventario.csv`) con las columnas `nombre_producto`, `cantidad` y `precio`.
- Archivos: `app.py` (toda la app), `requirements.txt` (dependencias), `README.md` y `inventario.csv`.
- La especificación completa está en `/content/especificacion_v2.md`.

## Reglas

- La clave de la API va SIEMPRE en secretos (`st.secrets` en la ruta A). Nunca en el código, en el README ni en el chat.
- Cada llamada a la API de Gemini va dentro de un bloque `try/except` y muestra un mensaje amigable y claro para el usuario en caso de error o timeout.
- Textos de la interfaz en español, sencillos, cálidos, pensados para alguien sin conocimientos técnicos.
- Control estricto de ingresos: Bloquear transacciones (mostrar mensaje en rojo) si se intenta ingresar un producto duplicado o si los campos de precio y cantidad son menores o iguales a 0.
- Actualización de stock: Para productos existentes, se debe proveer la opción clara o botón "Modificar/Editar Stock" para sumarle cantidad o actualizar su precio.
- Control estricto de salidas: Bloquear transacciones (mostrar mensaje en rojo) si la cantidad a retirar excede el stock disponible.
- Normalización de nombres: Convertir o tratar de forma idéntica productos duplicados con variaciones de capitalización (ej. "Manzana" y "manzana" deben ser el mismo producto).
- Interacción de IA (Interpretación A): La vendedora solo interactúa mediante formularios estructurados tradicionales para ingresos, salidas y modificaciones de stock. El chat con Gemini es exclusivo para responder dudas del inventario basadas únicamente en los datos reales del archivo CSV.
- Alertas visuales: Las advertencias de productos con stock crítico (5 unidades o menos) deben estar siempre visibles en la barra lateral (sidebar) como un resumen en color destacado o rojo.
- Cambios pequeños: uno por petición. Al terminar, explica qué has cambiado y por qué.
- Si añades una librería, añádela también a `requirements.txt` y dilo.
- No uses datos personales reales. Para probar, inventa ejemplos.

## Cómo comprobar que funciona

- Ruta A: `streamlit run app.py` en local (con `.streamlit/secrets.toml`), o haz push y revisa la app en Streamlit Cloud.
- Casos de prueba (entrada -> lo que esperamos):
  1. Ingreso de nuevo producto (Manzana, 10 unidades, precio 100) -> Producto guardado en el CSV y visible en el gráfico estático.
  2. Intento de ingreso de producto duplicado -> Bloquea la acción y muestra mensaje destacado en rojo indicando que ya existe.
  3. Salida de producto superior al stock existente -> Bloquea la transacción y muestra mensaje de error en rojo.
  4. Cantidad o precio ingresados menores o iguales a 0 -> Impide el envío y muestra mensaje de advertencia en rojo.
  5. Producto con stock menor o igual a 5 unidades -> Se activa automáticamente una advertencia visual permanente en la barra lateral.
  6. Preguntar en el chat "¿Cuántos plátanos me quedan?" -> Gemini lee el contexto del CSV y responde amablemente con el valor real.
  7. Pregunta fuera de tema en el chat -> La app indica amablemente que solo puede responder preguntas sobre el inventario actual.

## Qué no hacer

- No borres ni reescribas el README sin preguntar.
- No cambies el modelo ni la arquitectura sin preguntar.
- No permitas transacciones negativas de stock ni omisiones de validaciones en los formularios.
