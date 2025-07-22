import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Simulador DoxyPEP ITS", layout="centered")

st.title("📉 Simulador del impacto de DoxyPEP en ITS")
st.markdown("Este simulador permite visualizar el efecto de la profilaxis postexposición con doxiciclina (DoxyPEP) sobre la transmisión de ITS en una población de riesgo, considerando eficacia, cobertura, adherencia y reinfecciones.")

# Parámetros globales
N = st.number_input("Tamaño poblacional", 1000, 100000, value=10000)
days = st.slider("Duración de la simulación (días)", 30, 1095, value=365)
initial_infected = st.slider("Infectados iniciales", 0, N, value=500)

contact_rate = st.slider("Contactos sexuales por persona/día", 0.1, 5.0, value=0.5)
adherence = st.slider("Adherencia a DoxyPEP", 0.0, 1.0, value=0.8)
coverage = st.slider("Cobertura poblacional de DoxyPEP", 0.0, 1.0, value=0.5)

gamma = 1 / 14  # recuperación: media 14 días

# ITS específicas
st.subheader("🔬 Parámetros específicos de ITS")

its = {
    'clamidia': {
        'trans_prob': st.number_input("Prob. transmisión - Clamidia", 0.01, 0.5, 0.05),
        'efficacy': st.slider("Eficacia DoxyPEP - Clamidia", 0.0, 1.0, value=0.85),
        'reinfections': st.slider("Reinfecciones diarias - Clamidia", 0.0, 10.0, 0.5)
    },
    'sífilis': {
        'trans_prob': st.number_input("Prob. transmisión - Sífilis", 0.01, 0.5, 0.04),
        'efficacy': st.slider("Eficacia DoxyPEP - Sífilis", 0.0, 1.0, value=0.80),
        'reinfections': st.slider("Reinfecciones diarias - Sífilis", 0.0, 10.0, 0.2)
    },
    'gonorrea': {
        'trans_prob': st.number_input("Prob. transmisión - Gonorrea", 0.01, 0.5, 0.06),
        'efficacy': st.slider("Eficacia DoxyPEP - Gonorrea", 0.0, 1.0, value=0.50),
        'reinfections': st.slider("Reinfecciones diarias - Gonorrea", 0.0, 10.0, 0.4)
    }
}

# Simulación
t = np.arange(0, days)
summary_data = []

for disease, params in its.items():
    S = np.zeros(days)
    I = np.zeros(days)
    S[0] = N - initial_infected
    I[0] = initial_infected

    beta = (contact_rate * params['trans_prob']) / N
    effective_beta = beta * (1 - params['efficacy'] * coverage * adherence)

    for i in range(1, days):
        new_infections = effective_beta * S[i-1] * I[i-1] + params['reinfections']
        recoveries = gamma * I[i-1]
        S[i] = max(S[i-1] - new_infections + recoveries, 0)
        I[i] = max(I[i-1] + new_infections - recoveries, 0)

    # Gráfica
    st.subheader(f"📈 Evolución: {disease.capitalize()}")
    fig, ax = plt.subplots()
    ax.plot(t, I, label="Infectados", color="red")
    ax.plot(t, S, label="Susceptibles", color="green")
    ax.set_xlabel("Días")
    ax.set_ylabel("Personas")
    ax.set_title(f"Evolución de {disease.capitalize()}")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    summary_data.append({
        'ITS': disease,
        'Infectados al inicio': int(I[0]),
        'Infectados al final': int(I[-1])
    })

# Tabla resumen
st.subheader("📊 Resumen final")
summary_df = pd.DataFrame(summary_data)
st.dataframe(summary_df)


