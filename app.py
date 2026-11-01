import os
import pandas as pd
import plotly.express as px
import streamlit as st
from google import genai

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Inventario - Almacén",
    page_icon="📦",
    layout="wide",
)

CSV_FILE = "inventario.csv"
COLUMNAS = ["nombre_producto", "cantidad", "precio"]


# Funciones de persistencia y datos
def cargar_inventario():
  if os.path.exists(CSV_FILE):
    try:
      df = pd.read_csv(CSV_FILE)
      for col in COLUMNAS:
        if col not in df.columns:
          df[col] = 0 if col != "nombre_producto" else ""
      return df
    except Exception:
      return pd.DataFrame(columns=COLUMNAS)
  else:
    df = pd.DataFrame(columns=COLUMNAS)
    df.to_csv(CSV_FILE, index=False, encoding="utf-8")
    return df


def guardar_inventario(df):
  df.to_csv(CSV_FILE, index=False, encoding="utf-8")


# Inicializar estado de datos
if "df_inventario" not in st.session_state:
  st.session_state.df_inventario = cargar_inventario()

df = st.session_state.df_inventario

# --- BARRA LATERAL (SIDEBAR): Alertas de stock crítico y navegación ---
st.sidebar.title("📦 Menú y Alertas")
menu = st.sidebar.radio(
    "Seleccione una opción",
    ["Inventario y Gráfico", "Ingresar Producto", "Salida / Modificar Stock", "Asistente IA (Gemini)"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("🚨 Resumen Crítico (Stock ≤ 5)")

if not df.empty:
  stock_critico = df[df["cantidad"] <= 5]
  if not stock_critico.empty:
    for _, row in stock_critico.iterrows():
      st.sidebar.markdown(
          f"🔴 **{row['nombre_producto']}**: <span style='color:red; font-weight:bold;'>{row['cantidad']} un.</span>",
          unsafe_allow_html=True,
      )
  else:
    st.sidebar.success("No hay productos en stock crítico.")
else:
  st.sidebar.info("El inventario está vacío.")

# --- MÓDULO 1: Inventario y Gráfico Estático ---
if menu == "Inventario y Gráfico":
  st.title("📊 Consulta de Inventario y Stock Actual")
  st.write("Visualiza el stock absoluto actual de todos los productos del almacén.")

  if df.empty:
    st.warning("El inventario está actualmente vacío. Agrega productos desde el menú lateral.")
  else:
    st.dataframe(df, use_container_width=True)

    st.subheader("Gráfico de Stock Absoluto")
    fig = px.bar(
        df,
        x="nombre_producto",
        y="cantidad",
        title="Stock Actual por Producto",
        labels={"nombre_producto": "Producto", "cantidad": "Cantidad en Stock"},
        text="cantidad",
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# --- MÓDULO 2: Ingreso de Productos ---
elif menu == "Ingresar Producto":
  st.title("➕ Ingresar Nuevo Producto")
  st.write("Agrega un nuevo producto al almacén asegurándote de que no esté duplicado.")

  with st.form("form_ingreso"):
    nombre_input = st.text_input("Nombre del Producto")
    cantidad_input = st.number_input("Cantidad", min_value=0, step=1)
    precio_input = st.number_input("Precio ($)", min_value=0.0, step=100.0)
    submitted = st.form_submit_button("Guardar Producto")

    if submitted:
      nombre_norm = nombre_input.strip()
      if not nombre_norm:
        st.error("❌ El nombre del producto no puede estar vacío.")
      elif cantidad_input <= 0 or precio_input <= 0:
        st.markdown(
            "<p style='color:red;'>❌ Error: El producto tiene un precio 0 y no tiene stock, o los valores son menores o iguales a 0.</p>",
            unsafe_allow_html=True,
        )
      else:
        if not df.empty and any(df["nombre_producto"].str.lower() == nombre_norm.lower()):
          st.markdown(
              "<p style='color:red;'>❌ Error: El producto ya existe en el inventario.</p>",
              unsafe_allow_html=True,
          )
        else:
          nuevo_registro = pd.DataFrame(
              [{"nombre_producto": nombre_norm, "cantidad": int(cantidad_input), "precio": float(precio_input)}]
          )
          st.session_state.df_inventario = pd.concat([df, nuevo_registro], ignore_index=True)
          guardar_inventario(st.session_state.df_inventario)
          st.success(f"✅ ¡Realizado! El producto '{nombre_norm}' fue ingresado exitosamente con {cantidad_input} unidades.")

# --- MÓDULO 3: Salida y Modificación de Stock ---
elif menu == "Salida / Modificar Stock":
  st.title("🔄 Salida y Modificación de Stock")
  st.write("Registra salidas de productos o modifica el stock y precio de productos existentes.")

  if df.empty:
    st.warning("No hay productos registrados en el inventario.")
  else:
    tab1, tab2 = st.tabs(["Salida de Productos", "Modificar / Editar Stock o Precio"])

    with tab1:
      st.subheader("Registrar Retiro o Salida")
      prod_salida = st.selectbox("Seleccione el producto", df["nombre_producto"].tolist(), key="sel_salida")
      cant_a_retirar = st.number_input("Cantidad a retirar", min_value=1, step=1, key="cant_retirar")

      if st.button("Procesar Salida"):
        idx = df[df["nombre_producto"] == prod_salida].index[0]
        stock_actual = int(df.loc[idx, "cantidad"])

        if cant_a_retirar > stock_actual:
          st.markdown(
              "<p style='color:red;'>❌ No hay stock suficiente para realizar esta salida.</p>",
              unsafe_allow_html=True,
          )
        else:
          df.loc[idx, "cantidad"] = stock_actual - int(cant_a_retirar)
          guardar_inventario(df)
          st.success(f"✅ ¡Realizado! Salida registrada con éxito. Stock actual de '{prod_salida}': {df.loc[idx, 'cantidad']} unidades.")

    with tab2:
      st.subheader("Actualizar Stock o Precio Existente")
      prod_mod = st.selectbox("Seleccione el producto a modificar", df["nombre_producto"].tolist(), key="sel_mod")
      idx_mod = df[df["nombre_producto"] == prod_mod].index[0]

      stock_actual_val = int(df.loc[idx_mod, "cantidad"])
      precio_actual_val = float(df.loc[idx_mod, "precio"])

      nueva_cantidad = st.number_input(
          "Nueva cantidad total en almacén", min_value=0, value=stock_actual_val, step=1, key="mod_cant"
      )
      nuevo_precio = st.number_input(
          "Nuevo precio ($)", min_value=0.0, value=precio_actual_val, step=100.0, key="mod_precio"
      )

      if st.button("Guardar Cambios"):
        if nueva_cantidad <= 0 or nuevo_precio <= 0:
          st.markdown(
              "<p style='color:red;'>❌ Error: La cantidad y el precio deben ser mayores a 0.</p>",
              unsafe_allow_html=True,
          )
        else:
          df.loc[idx_mod, "cantidad"] = int(nueva_cantidad)
          df.loc[idx_mod, "precio"] = float(nuevo_precio)
          guardar_inventario(df)
          st.success(f"✅ ¡Realizado! El producto '{prod_mod}' ha sido actualizado correctamente.")

# --- MÓDULO 4: Asistente IA (Gemini) ---
elif menu == "Asistente IA (Gemini)":
  st.title("💬 Asistente de Consulta de Inventario (Gemini)")
  st.write("Haz preguntas sobre el stock actual de tu almacén de forma natural.")

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt_usuario := st.chat_input("Ej: ¿Cuánto Miel Negro 500ml me queda?"):
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    with st.chat_message("user"):
      st.markdown(prompt_usuario)

    with st.chat_message("assistant"):
      with st.spinner("Consultando el inventario..."):
        try:
          if "GEMINI_API_KEY" not in st.secrets:
            st.error("⚠️ Falta configurar `GEMINI_API_KEY` en los secretos de Streamlit.")
          else:
            from google import genai
            
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            csv_data_string = df.to_csv(index=False)
            system_instruction = (
                "Eres un asistente amigable y útil para una vendedora de un pequeño almacén. "
                "Tu único trabajo es responder preguntas sobre el inventario basándote EXCLUSIVAMENTE "
                "en los datos reales del archivo CSV proporcionados a continuación. "
                "Si te preguntan algo fuera del inventario, indica amablemente que solo puedes responder dudas sobre el stock actual. "
                f"\n\nDatos actuales del inventario:\n{csv_data_string}"
            )

            # Modelo actualizado a models/gemini-3.5-flash-lite
            response = client.models.generate_content(
                model="models/gemini-3.5-flash-lite",
                contents=system_instruction + "\n\nPregunta: " + prompt_usuario
            )

            respuesta_ia = response.text
            st.markdown(respuesta_ia)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})

        except Exception as e:
          error_str = str(e).lower()
          if "quota" in error_str or "resource_exhausted" in error_str or "429" in error_str:
            st.warning(
                "⚠️ **Límite diario de Gemini alcanzado:** Has superado temporalmente las consultas gratuitas permitidas por Google. "
                "Los formularios y el inventario siguen funcionando con normalidad."
            )
          else:
            st.error(f"❌ Ocurrió un inconveniente al consultar con el asistente: {e}")