import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Título
st.title("Simulador del impacto de DoxyPEP en la transmisión de ITS")

# Entradas
population = st.number_input("Tamaño de la población", value=10000, min_value=1000)
initial_infected = st.slider("Infectados iniciales", 1, population, 500)
contact_rate = st.slider("Contactos sexuales por persona/día", 0.1, 5.0, 0.5)
transmission_prob = st.slider("Probabilidad de transmisión por contacto", 0.01, 0.5, 0.05)
doxypep_efficacy = st.slider("Eficacia de DoxyPEP", 0.0, 1.0, 0.70)
doxypep_coverage = st.slider("Cobertura de DoxyPEP", 0.0, 1.0, 0.50)
days = st.slider("Duración de la simulación (días)", 30, 1095, 365)

# Parámetros del modelo
beta = (contact_rate * transmission_prob) / population
gamma = 1 / 14  # Duración media infección
effective_beta = beta * (1 - doxypep_efficacy * doxypep_coverage)

# Inicialización
S = np.zeros(days)
I = np.zeros(days)
S[0] = population - initial_infected
I[0] = initial_infected

# Simulación
for i in range(1, days):
    new_infections = effective_beta * S[i-1] * I[i-1]
    recoveries = gamma * I[i-1]
    S[i] = S[i-1] - new_infections + recoveries
    I[i] = I[i-1] + new_infections - recoveries

# Gráfico
st.subheader("Resultados de la simulación")
fig, ax = plt.subplots()
ax.plot(range(days), I, label="Infectados", color='red')
ax.plot(range(days), S, label="Susceptibles", color='green')
ax.set_xlabel("Días")
ax.set_ylabel("Personas")
ax.set_title("Evolución de ITS con intervención DoxyPEP")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Tabla resumen
st.subheader("Evolución del número de infectados en días clave")
interval = days // 10
checkpoints = list(range(0, days, interval))
resumen = pd.DataFrame({
    "Día": checkpoints,
    "Infectados": [int(I[i]) for i in checkpoints],
    "Susceptibles": [int(S[i]) for i in checkpoints]
})
st.dataframe(resumen)

