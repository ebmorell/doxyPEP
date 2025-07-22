import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Título y descripción
st.title("Simulador del impacto de DoxyPEP en la transmisión de ITS")
st.write("Esta herramienta permite modelar la evolución de ITS en una población de riesgo, ajustando parámetros como eficacia de DoxyPEP, cobertura, y contactos sexuales.")

# Entradas del usuario
population = st.number_input("Tamaño de la población", value=10000, min_value=1000)
initial_infected = st.slider("Infectados iniciales", 1, population, 500)
contact_rate = st.slider("Contactos sexuales por persona/día", 0.1, 5.0, 0.5)
transmission_prob = st.slider("Probabilidad de transmisión por contacto", 0.01, 0.5, 0.05)
doxypep_efficacy = st.slider("Eficacia de DoxyPEP", 0.0, 1.0, 0.70)
doxypep_coverage = st.slider("Cobertura de DoxyPEP", 0.0, 1.0, 0.50)
days = st.slider("Duración de la simulación (días)", 30, 1095, 365)

# Parámetros del modelo
beta = (contact_rate * transmission_prob) / population
gamma = 1 / 14  # Duración media de infección: 14 días
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

# Resultados
st.subheader("Resultados de la simulación")
fig, ax = plt.subplots()
ax.plot(I, label="Infectados")
ax.plot(S, label="Susceptibles")
ax.set_xlabel("Días")
ax.set_ylabel("Personas")
ax.set_title("Evolución de ITS con intervención DoxyPEP")
ax.legend()
st.pyplot(fig)
