import os
import pandas as pd
import streamlit as st
import plotly.express as px
from google import genai
from google.genai import types

# ------------------------------------------------------------------------------
# Configuración Inicial y Constantes
# ------------------------------------------------------------------------------
MODELO = "gemini-2.5-flash"
CSV_FILE = "inventario.csv"
COLUMNAS = ["nombre_producto", "cantidad", "precio"]

st.set_page_config(
    page_title="Gestión de Inventario",
    page_icon="📦",
    layout="wide"
)

# ------------------------------------------------------------------------------
# Funciones de Manejo del CSV y Persistencia
# ------------------------------------------------------------------------------
def cargar_inventario() -> pd.DataFrame:
    """Carga el inventario desde el archivo CSV. Si no existe, lo crea vacío."""
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=COLUMNAS)
        df.to_csv(CSV_FILE, index=False)
        return df
    try:
        df = pd.read_csv(CSV_FILE)
        # Asegurar tipos de datos correctos
        df["nombre_producto"] = df["nombre_producto"].astype(str)
        df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce").fillna(0).astype(int)
        df["precio"] = pd.to_numeric(df["precio"], errors="coerce").fillna(0.0).astype(float)
        return df
    except Exception:
        df = pd.DataFrame(columns=COLUMNAS)
        df.to_csv(CSV_FILE, index=False)
        return df

def guardar_inventario(df: pd.DataFrame):
    """Guarda el DataFrame en el archivo CSV."""
    df.to_csv(CSV_FILE, index=False)

def normalizar_nombre(nombre: str) -> str:
    """Elimina espacios extra para normalizar la comparación."""
    return nombre.strip()

# Inicializar sesión para el historial del chat
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

# Cargar datos al inicio
df_inventario = cargar_inventario()

# ------------------------------------------------------------------------------
# Barra Lateral (Sidebar) - Resumen Crítico de Stock
# ------------------------------------------------------------------------------
st.sidebar.title("📌 Almacén")
st.sidebar.markdown("---")
st.sidebar.subheader("⚠️ Stock Crítico (≤ 5 unids.)")

df_critico = df_inventario[df_inventario["cantidad"] <= 5]

if not df_critico.empty:
    for idx, row in df_critico.iterrows():
        st.sidebar.error(f"**{row['nombre_producto']}**: {row['cantidad']} unidades (Precio: ${row['precio']:.2f})")
else:
    st.sidebar.success("✅ Todo el stock se encuentra en niveles aceptables.")

st.sidebar.markdown("---")
st.sidebar.info("💡 Utiliza los formularios del panel central para modificar el inventario y el chat inferior para realizar consultas.")

# ------------------------------------------------------------------------------
# Panel Principal - Título y Resumen
# ------------------------------------------------------------------------------
st.title("📦 Sistema de Gestión de Inventario")
st.write("Bienvenido/a. Administra las entradas, salidas y modificaciones de productos de forma sencilla.")

# Visualización Gráfica del Stock
st.subheader("📊 Stock Actual en Almacén")
if not df_inventario.empty:
    fig = px.bar(
        df_inventario,
        x="nombre_producto",
        y="cantidad",
        text="cantidad",
        title="Cantidad Estática Disponible por Producto",
        labels={"nombre_producto": "Producto", "cantidad": "Cantidad disponible"},
        color="cantidad",
        color_continuous_scale="Blues"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No hay productos registrados en el inventario.")

st.markdown("---")

# ------------------------------------------------------------------------------
# Módulos de Operaciones (Formularios Tradicionales)
# ------------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📥 Ingresar Nuevo Producto", 
    "✏️ Modificar / Editar Stock", 
    "📤 Salida de Productos", 
    "📋 Consultar Inventario"
])

# ---- TAB 1: Ingresar Nuevo Producto ----
with tab1:
    st.subheader("Registrar un Nuevo Producto")
    with st.form("form_nuevo_producto", clear_on_submit=True):
        nuevo_nombre = st.text_input("Nombre del Producto")
        nueva_cantidad = st.number_input("Cantidad a ingresar", min_value=0, step=1, value=0)
        nuevo_precio = st.number_input("Precio por unidad", min_value=0.0, step=0.5, value=0.0)
        btn_ingresar = st.form_submit_button("Ingresar Producto")

    if btn_ingresar:
        nombre_clean = normalizar_nombre(nuevo_nombre)
        
        # Validaciones
        if not nombre_clean:
            st.error("❌ El nombre del producto no puede estar vacío.")
        elif nueva_cantidad <= 0 or nuevo_precio <= 0:
            st.error("❌ El producto no puede tener una cantidad o un precio menor o igual a 0.")
        else:
            # Comprobar si ya existe (normalización insensible a mayúsculas/minúsculas)
            existe = df_inventario[df_inventario["nombre_producto"].str.lower() == nombre_clean.lower()]
            if not existe.empty:
                st.error(f"❌ El producto '{nombre_clean}' ya existe. Utiliza la pestaña 'Modificar / Editar Stock' para agregar más unidades.")
            else:
                nuevo_registro = pd.DataFrame([{
                    "nombre_producto": nombre_clean,
                    "cantidad": int(nueva_cantidad),
                    "precio": float(nuevo_precio)
                }])
                df_inventario = pd.concat([df_inventario, nuevo_registro], ignore_index=True)
                guardar_inventario(df_inventario)
                st.success(f"✅ Producto '{nombre_clean}' agregado con éxito.")
                st.rerun()

# ---- TAB 2: Modificar / Editar Stock ----
with tab2:
    st.subheader("Modificar Stock o Precio de Producto Existente")
    if df_inventario.empty:
        st.info("No hay productos disponibles para modificar.")
    else:
        opciones_productos = df_inventario["nombre_producto"].tolist()
        producto_sel = st.selectbox("Selecciona el producto a modificar", opciones_productos)
        
        # Obtener valores actuales
        fila_actual = df_inventario[df_inventario["nombre_producto"] == producto_sel].iloc[0]
        
        with st.form("form_modificar_stock"):
            st.write(f"**Valores actuales:** Cantidad: {fila_actual['cantidad']} | Precio: ${fila_actual['precio']:.2f}")
            cant_sumar = st.number_input("Cantidad a AÑADIR al stock actual", min_value=0, step=1, value=0)
            nuevo_precio_mod = st.number_input("Nuevo Precio (dejar en el valor actual si no desea cambiarlo)", min_value=0.0, value=float(fila_actual['precio']), step=0.5)
            btn_modificar = st.form_submit_button("Guardar Cambios")

        if btn_modificar:
            if nuevo_precio_mod <= 0:
                st.error("❌ El precio debe ser mayor a 0.")
            else:
                idx = df_inventario[df_inventario["nombre_producto"] == producto_sel].index[0]
                df_inventario.at[idx, "cantidad"] += int(cant_sumar)
                df_inventario.at[idx, "precio"] = float(nuevo_precio_mod)
                guardar_inventario(df_inventario)
                st.success(f"✅ Stock de '{producto_sel}' actualizado exitosamente.")
                st.rerun()

# ---- TAB 3: Salida de Productos ----
with tab3:
    st.subheader("Registrar Salida de Productos")
    if df_inventario.empty:
        st.info("No hay productos disponibles para registrar salidas.")
    else:
        opciones_salida = df_inventario["nombre_producto"].tolist()
        prod_salida = st.selectbox("Selecciona el producto a retirar", opciones_salida, key="select_salida")
        fila_salida = df_inventario[df_inventario["nombre_producto"] == prod_salida].iloc[0]
        
        with st.form("form_salida_producto"):
            st.write(f"**Stock disponible actual:** {fila_salida['cantidad']} unidades")
            cant_retirar = st.number_input("Cantidad a retirar", min_value=1, step=1, value=1)
            btn_salida = st.form_submit_button("Confirmar Salida")

        if btn_salida:
            if cant_retirar > fila_salida["cantidad"]:
                st.error("❌ No hay suficiente stock disponible para realizar esta transacción.")
            else:
                idx = df_inventario[df_inventario["nombre_producto"] == prod_salida].index[0]
                df_inventario.at[idx, "cantidad"] -= int(cant_retirar)
                guardar_inventario(df_inventario)
                st.success(f"✅ Se retiraron {cant_retirar} unidad(es) de '{prod_salida}'.")
                st.rerun()

# ---- TAB 4: Consultar Inventario Completo ----
with tab4:
    st.subheader("Tabla Completa de Inventario")
    st.dataframe(df_inventario, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------------------------
# Asistente Virtual (Chat con Gemini API - SDK google-genai)
# ------------------------------------------------------------------------------
st.subheader("💬 Asistente de Consulta de Inventario (Gemini)")
st.write("Haz preguntas sobre el stock actual de tu almacén.")

# Renderizar historial de chat previa
for msg in st.session_state["chat_messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("Ejemplo: ¿Cuántas manzanas me quedan?")

if user_query:
    # Registrar mensaje del usuario
    st.session_state["chat_messages"].append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Preparar el contexto real basado en el CSV actual
    datos_csv_str = df_inventario.to_string(index=False)
    
    system_instruction = f"""
    Eres un asistente virtual amable y servicial para una vendedora de un pequeño almacén.
    Tu única función es responder dudas sobre la disponibilidad, stock y precios del inventario basándote ÚNICAMENTE en la siguiente tabla de datos real extraída del sistema:

    {datos_csv_str}

    Reglas estrictas de comportamiento:
    1. Responde de forma sencilla, clara y cálida.
    2. Si te preguntan por un producto que no está en la tabla, indica amablemente que no existe en el inventario.
    3. Si la pregunta no tiene relación con el inventario o la consulta de productos, indica educadamente que solo puedes ayudar a responder preguntas sobre el inventario actual del almacén.
    4. NUNCA inventes productos ni cantidades que no estén presentes en los datos de la tabla.
    """

    with st.chat_message("assistant"):
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            respuesta_error = "⚠️ No se encontró la clave API de Gemini (`GEMINI_API_KEY`). Por favor configúrala en los secretos de Streamlit."
            st.error(respuesta_error)
            st.session_state["chat_messages"].append({"role": "assistant", "content": respuesta_error})
        else:
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model=MODELO,
                    contents=user_query,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2
                    )
                )
                
                if response.text:
                    respuesta_texto = response.text
                else:
                    respuesta_texto = "No pude obtener una respuesta válida en este momento."
                
                st.markdown(respuesta_texto)
                st.session_state["chat_messages"].append({"role": "assistant", "content": respuesta_texto})

            except Exception as e:
                error_msg = "Lo siento, ha ocurrido un inconveniente al consultar con el asistente. Por favor, intenta de nuevo en unos momentos."
                st.error(error_msg)
                st.session_state["chat_messages"].append({"role": "assistant", "content": error_msg})