import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Reconocimiento de Gestos",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 2rem;
    }

    .titulo {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitulo {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .resultado {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
    }

    .gesto {
        font-size: 42px;
        font-weight: bold;
    }

    .confianza {
        font-size: 20px;
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TÍTULO
# ============================================================

st.markdown(
    '<div class="titulo">🤖 Reconocimiento de Gestos</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Aplicación de Visión Artificial con Teachable Machine'
    '</div>',
    unsafe_allow_html=True
)


st.divider()


# ============================================================
# CARGAR MODELO
# ============================================================

@st.cache_resource
def cargar_modelo():
    return load_model("keras_model.h5")


try:
    model = cargar_modelo()

except Exception as e:

    st.error("❌ No se pudo cargar el modelo.")

    st.write(
        "Verifica que el archivo `keras_model.h5` "
        "esté en el repositorio."
    )

    st.stop()


# ============================================================
# CLASES
# ============================================================

clases = {
    0: {
        "nombre": "IZQUIERDA",
        "emoji": "⬅️"
    },

    1: {
        "nombre": "ARRIBA",
        "emoji": "⬆️"
    },

    2: {
        "nombre": "DERECHA",
        "emoji": "➡️"
    }
}


# ============================================================
# INFORMACIÓN
# ============================================================

st.info(
    """
    📷 Coloca tu mano frente a la cámara y toma una fotografía.

    El modelo analizará la imagen y determinará si corresponde
    a uno de los tres gestos entrenados:
    
    ⬅️ Izquierda | ⬆️ Arriba | ➡️ Derecha
    """
)


# ============================================================
# CÁMARA
# ============================================================

foto = st.camera_input("📷 Toma una fotografía")


# ============================================================
# PROCESAMIENTO
# ============================================================

if foto is not None:

    # --------------------------------------------------------
    # ABRIR IMAGEN
    # --------------------------------------------------------

    imagen = Image.open(foto).convert("RGB")

    st.subheader("📸 Imagen capturada")

    st.image(
        imagen,
        use_container_width=True
    )


    # --------------------------------------------------------
    # REDIMENSIONAR
    # --------------------------------------------------------

    imagen_modelo = imagen.resize((224, 224))


    # --------------------------------------------------------
    # CONVERTIR A NUMPY
    # --------------------------------------------------------

    imagen_array = np.asarray(imagen_modelo)


    # --------------------------------------------------------
    # NORMALIZAR
    # --------------------------------------------------------

    imagen_normalizada = (
        imagen_array.astype(np.float32) / 127.0
    ) - 1


    # --------------------------------------------------------
    # PREPARAR DATOS
    # --------------------------------------------------------

    datos = np.ndarray(
        shape=(1, 224, 224, 3),
        dtype=np.float32
    )

    datos[0] = imagen_normalizada


    # --------------------------------------------------------
    # PREDICCIÓN
    # --------------------------------------------------------

    prediccion = model.predict(
        datos,
        verbose=0
    )


    # --------------------------------------------------------
    # OBTENER CLASE CON MAYOR PROBABILIDAD
    # --------------------------------------------------------

    indice = int(
        np.argmax(prediccion[0])
    )

    confianza = float(
        prediccion[0][indice]
    )


    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    gesto = clases.get(
        indice,
        {
            "nombre": "DESCONOCIDO",
            "emoji": "❓"
        }
    )


    st.divider()

    st.subheader("🤖 Resultado del modelo")


    # --------------------------------------------------------
    # MOSTRAR RESULTADO
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="resultado">

            <div class="gesto">
                {gesto["emoji"]} {gesto["nombre"]}
            </div>

            <div class="confianza">
                Confianza:
                <strong>{confianza * 100:.2f}%</strong>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # BARRA DE CONFIANZA
    # --------------------------------------------------------

    st.progress(
        confianza
    )


    # --------------------------------------------------------
    # TODAS LAS PREDICCIONES
    # --------------------------------------------------------

    st.subheader("📊 Probabilidad por clase")


    for i, probabilidad in enumerate(prediccion[0]):

        if i in clases:

            nombre = clases[i]["nombre"]
            emoji = clases[i]["emoji"]

            st.write(
                f"{emoji} {nombre}: "
                f"{probabilidad * 100:.2f}%"
            )

            st.progress(
                float(probabilidad)
            )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()

st.caption(
    "Proyecto de Clase 9 — Aplicaciones con Visión Artificial"
)

st.caption(
    "Modelo entrenado con Google Teachable Machine"
)
