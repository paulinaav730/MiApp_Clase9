import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Mi App - Gestos",
    page_icon="🖐️",
    layout="centered"
)

# ============================================================
# CONFIGURACIÓN
# ============================================================

MODEL_URL = "./model/model.json"
METADATA_URL = "./model/metadata.json"

# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f7f7f7;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.10);
    margin-bottom: 20px;
}

.direction {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# TÍTULO
# ============================================================

st.markdown(
    '<div class="title">🖐️ Reconocimiento de Gestos</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Mueve tu mano para indicar una dirección</div>',
    unsafe_allow_html=True
)

# ============================================================
# INSTRUCCIONES
# ============================================================

st.markdown("""
<div class="card">

### 🎯 Gestos disponibles

⬅️ **Izquierda**  
⬆️ **Arriba**  
➡️ **Derecha**

Coloca tu mano frente a la cámara y apunta hacia una de las tres direcciones.

</div>
""", unsafe_allow_html=True)

# ============================================================
# MODELO + CÁMARA
# ============================================================

html_code = f"""
<!DOCTYPE html>

<html>

<head>

<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest"></script>

<script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"></script>

<style>

body {{
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    text-align: center;
}}

#webcam-container {{
    display: flex;
    justify-content: center;
    margin-top: 10px;
}}

canvas {{
    border-radius: 15px;
    max-width: 100%;
}}

#resultado {{
    font-size: 38px;
    font-weight: bold;
    margin-top: 15px;
}}

#probabilidad {{
    font-size: 18px;
    margin-top: 5px;
}}

button {{
    background-color: #2563eb;
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 10px;
    font-size: 18px;
    cursor: pointer;
    margin: 10px;
}}

button:hover {{
    opacity: 0.85;
}}

.bar-container {{
    width: 90%;
    margin: 10px auto;
    text-align: left;
}}

.bar-label {{
    font-weight: bold;
    margin-bottom: 3px;
}}

.bar {{
    width: 100%;
    background: #eeeeee;
    border-radius: 10px;
    height: 18px;
    overflow: hidden;
}}

.fill {{
    height: 100%;
    width: 0%;
    transition: width 0.2s;
}}

#izquierda {{
    background: #ff8a00;
}}

#arriba {{
    background: #e91e63;
}}

#derecha {{
    background: #7c3aed;
}}

</style>

</head>

<body>

<button onclick="init()">📷 Activar cámara</button>

<div id="webcam-container"></div>

<div id="resultado">
    Esperando cámara...
</div>

<div id="probabilidad">
    Coloca tu mano frente a la cámara
</div>

<br>

<div class="bar-container">

    <div class="bar-label">
        ⬅️ Izquierda
    </div>

    <div class="bar">
        <div id="izquierda" class="fill"></div>
    </div>

</div>


<div class="bar-container">

    <div class="bar-label">
        ⬆️ Arriba
    </div>

    <div class="bar">
        <div id="arriba" class="fill"></div>
    </div>

</div>


<div class="bar-container">

    <div class="bar-label">
        ➡️ Derecha
    </div>

    <div class="bar">
        <div id="derecha" class="fill"></div>
    </div>

</div>


<script>

const URL = "{MODEL_URL.replace("model.json", "")}";

let model;
let webcam;
let maxPredictions;

async function init() {{

    document.getElementById("resultado").innerHTML =
        "⏳ Cargando modelo...";

    try {{

        const modelURL = URL + "model.json";
        const metadataURL = URL + "metadata.json";

        model = await tmImage.load(modelURL, metadataURL);

        maxPredictions = model.getTotalClasses();

        webcam = new tmImage.Webcam(
            400,
            400,
            true
        );

        await webcam.setup();

        await webcam.play();

        document
            .getElementById("webcam-container")
            .appendChild(webcam.canvas);

        document.getElementById("resultado").innerHTML =
            "🖐️ Cámara activa";

        window.requestAnimationFrame(loop);

    }} catch(error) {{

        console.error(error);

        document.getElementById("resultado").innerHTML =
            "❌ Error al activar la cámara";

        document.getElementById("probabilidad").innerHTML =
            error;

    }}

}}


async function loop() {{

    webcam.update();

    await predict();

    window.requestAnimationFrame(loop);

}}


async function predict() {{

    const prediction = await model.predict(
        webcam.canvas
    );

    let mejorClase = "";
    let mejorProbabilidad = 0;

    for (
        let i = 0;
        i < prediction.length;
        i++
    ) {{

        let nombre =
            prediction[i].className;

        let probabilidad =
            prediction[i].probability;

        let porcentaje =
            Math.round(probabilidad * 100);

        if (
            nombre.toLowerCase().includes("izquierda")
        ) {{

            document.getElementById("izquierda")
                .style.width = porcentaje + "%";

        }}

        if (
            nombre.toLowerCase().includes("arriba")
        ) {{

            document.getElementById("arriba")
                .style.width = porcentaje + "%";

        }}

        if (
            nombre.toLowerCase().includes("derecha")
        ) {{

            document.getElementById("derecha")
                .style.width = porcentaje + "%";

        }}

        if (
            probabilidad > mejorProbabilidad
        ) {{

            mejorProbabilidad =
                probabilidad;

            mejorClase =
                nombre;

        }}

    }}

    let porcentajeFinal =
        Math.round(
            mejorProbabilidad * 100
        );

    let emoji = "🖐️";

    if (
        mejorClase.toLowerCase().includes("izquierda")
    ) {{

        emoji = "⬅️";

    }}

    else if (
        mejorClase.toLowerCase().includes("arriba")
    ) {{

        emoji = "⬆️";

    }}

    else if (
        mejorClase.toLowerCase().includes("derecha")
    ) {{

        emoji = "➡️";

    }}

    document.getElementById("resultado").innerHTML =
        emoji + " " + mejorClase;

    document.getElementById("probabilidad").innerHTML =
        "Probabilidad: " +
        porcentajeFinal +
        "%";

}}

</script>

</body>

</html>
"""

components.html(
    html_code,
    height=750,
    scrolling=False
)

# ============================================================
# INFORMACIÓN
# ============================================================

st.markdown("---")

st.markdown("""
<div class="card">

### 🤖 ¿Cómo funciona?

La aplicación utiliza un modelo de inteligencia artificial
entrenado con **Teachable Machine**.

El modelo reconoce tres clases:

- ⬅️ Izquierda
- ⬆️ Arriba
- ➡️ Derecha

La cámara captura tu mano y el modelo calcula cuál de los
tres gestos reconoce con mayor probabilidad.

</div>
""", unsafe_allow_html=True)
