import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Mi App - Reconocimiento de Gestos",
    page_icon="🖐️",
    layout="centered"
)

# ============================================================
# MODELO DE TEACHABLE MACHINE
# ============================================================

MODEL_URL = (
    "https://cdn.jsdelivr.net/gh/"
    "paulinaav730/MiApp_Clase9@main/model/"
)

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
    margin-top: 20px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666666;
    margin-bottom: 25px;
}

.card {
    padding: 25px;
    border-radius: 18px;
    background-color: white;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.10);
    margin-bottom: 25px;
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
    '<div class="subtitle">Control mediante gestos de la mano</div>',
    unsafe_allow_html=True
)

# ============================================================
# INSTRUCCIONES
# ============================================================

st.markdown("""
<div class="card">

<h3>🎯 Gestos disponibles</h3>

<p>⬅️ <b>Izquierda</b></p>
<p>⬆️ <b>Arriba</b></p>
<p>➡️ <b>Derecha</b></p>

<p>
Coloca tu mano frente a la cámara y realiza uno de los
tres gestos que utilizaste para entrenar el modelo.
</p>

</div>
""", unsafe_allow_html=True)

# ============================================================
# HTML + JAVASCRIPT
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

button {{
    background: #2563eb;
    color: white;
    border: none;
    padding: 13px 28px;
    border-radius: 12px;
    font-size: 18px;
    cursor: pointer;
    margin-bottom: 15px;
}}

button:hover {{
    opacity: 0.85;
}}

#webcam-container {{
    display: flex;
    justify-content: center;
    margin-top: 10px;
}}

canvas {{
    border-radius: 18px;
    max-width: 100%;
}}

#resultado {{
    font-size: 38px;
    font-weight: bold;
    margin-top: 20px;
}}

#probabilidad {{
    font-size: 18px;
    color: #666;
    margin-top: 5px;
}}

.bar-container {{
    width: 90%;
    margin: 15px auto;
    text-align: left;
}}

.bar-label {{
    font-size: 17px;
    font-weight: bold;
    margin-bottom: 5px;
}}

.bar {{
    width: 100%;
    height: 20px;
    background: #eeeeee;
    border-radius: 10px;
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

<button onclick="init()">
    📷 Activar cámara
</button>

<div id="webcam-container"></div>

<div id="resultado">
    🖐️ Cámara apagada
</div>

<div id="probabilidad">
    Presiona "Activar cámara"
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

const MODEL_URL = "{MODEL_URL}";

let model;
let webcam;
let maxPredictions;


// ============================================================
// ACTIVAR CÁMARA
// ============================================================

async function init() {{

    document.getElementById("resultado").innerHTML =
        "⏳ Cargando modelo...";

    document.getElementById("probabilidad").innerHTML =
        "Espera un momento...";

    try {{

        const modelURL =
            MODEL_URL + "model.json";

        const metadataURL =
            MODEL_URL + "metadata.json";


        // Cargar modelo de Teachable Machine

        model = await tmImage.load(
            modelURL,
            metadataURL
        );

        maxPredictions =
            model.getTotalClasses();


        // Crear cámara

        webcam = new tmImage.Webcam(
            400,
            400,
            true
        );

        await webcam.setup();

        await webcam.play();


        document
            .getElementById("webcam-container")
            .innerHTML = "";

        document
            .getElementById("webcam-container")
            .appendChild(webcam.canvas);


        document.getElementById("resultado").innerHTML =
            "🖐️ Cámara activa";

        document.getElementById("probabilidad").innerHTML =
            "Haz uno de los gestos";


        window.requestAnimationFrame(loop);

    }}
    catch(error) {{

        console.error(error);

        document.getElementById("resultado").innerHTML =
            "❌ Error";

        document.getElementById("probabilidad").innerHTML =
            "No se pudo cargar el modelo.";

    }}

}}


// ============================================================
// CICLO DE PREDICCIÓN
// ============================================================

async function loop() {{

    webcam.update();

    await predict();

    window.requestAnimationFrame(loop);

}}


// ============================================================
// PREDICCIÓN
// ============================================================

async function predict() {{

    const prediction =
        await model.predict(webcam.canvas);


    let mejorClase = "";

    let mejorProbabilidad = 0;


    // Reiniciar barras

    document.getElementById("izquierda")
        .style.width = "0%";

    document.getElementById("arriba")
        .style.width = "0%";

    document.getElementById("derecha")
        .style.width = "0%";


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
            Math.round(
                probabilidad * 100
            );


        // -----------------------------
        // IZQUIERDA
        // -----------------------------

        if (
            nombre
                .toLowerCase()
                .includes("izquierda")
        ) {{

            document
                .getElementById("izquierda")
                .style.width =
                porcentaje + "%";

        }}


        // -----------------------------
        // ARRIBA
        // -----------------------------

        if (
            nombre
                .toLowerCase()
                .includes("arriba")
        ) {{

            document
                .getElementById("arriba")
                .style.width =
                porcentaje + "%";

        }}


        // -----------------------------
        // DERECHA
        // -----------------------------

        if (
            nombre
                .toLowerCase()
                .includes("derecha")
        ) {{

            document
                .getElementById("derecha")
                .style.width =
                porcentaje + "%";

        }}


        // -----------------------------
        // MEJOR RESULTADO
        // -----------------------------

        if (
            probabilidad >
            mejorProbabilidad
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
        mejorClase
            .toLowerCase()
            .includes("izquierda")
    ) {{

        emoji = "⬅️";

    }}

    else if (
        mejorClase
            .toLowerCase()
            .includes("arriba")
    ) {{

        emoji = "⬆️";

    }}

    else if (
        mejorClase
            .toLowerCase()
            .includes("derecha")
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


# ============================================================
# MOSTRAR APLICACIÓN
# ============================================================

components.html(
    html_code,
    height=760,
    scrolling=False
)

# ============================================================
# INFORMACIÓN
# ============================================================

st.markdown("---")

st.markdown("""
<div class="card">

<h3>🤖 Sobre el modelo</h3>

<p>
Esta aplicación utiliza un modelo de inteligencia artificial
entrenado mediante <b>Teachable Machine</b>.
</p>

<p>
El modelo fue entrenado para reconocer tres gestos:
</p>

<p>
⬅️ Izquierda &nbsp;&nbsp;
⬆️ Arriba &nbsp;&nbsp;
➡️ Derecha
</p>

</div>
""", unsafe_allow_html=True)
