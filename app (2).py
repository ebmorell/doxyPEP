import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------
# PARÁMETROS GENERALES
# ---------------------------
N = 10000               # Tamaño poblacional
I0 = 500                # Infectados iniciales
S0 = N - I0             # Susceptibles iniciales
days = 365              # Duración de la simulación (1 año)
t = np.arange(0, days)  # Vector de tiempo

# Contactos y transmisión
contact_rate = 0.5  # contactos sexuales por persona y día

# Tasa de curación (1/duración media en días)
gamma = 1 / 14

# Eficacia de DoxyPEP por ITS
efficacies = {
    'clamidia': 0.85,
    'sífilis': 0.80,
    'gonorrea': 0.50
}

# Probabilidad de transmisión por ITS (por contacto)
transmission_probs = {
    'clamidia': 0.05,
    'sífilis': 0.04,
    'gonorrea': 0.06
}

# Reinfecciones externas diarias
external_infections = {
    'clamidia': 0.5,
    'sífilis': 0.2,
    'gonorrea': 0.4
}

# Parámetros de DoxyPEP
coverage = 0.5     # Proporción con acceso
adherence = 0.8    # Proporción que lo toma correctamente

# ---------------------------
# SIMULACIÓN PARA CADA ITS
# ---------------------------
results = {}

for disease in transmission_probs:
    S = np.zeros(days)
    I = np.zeros(days)
    S[0] = S0
    I[0] = I0

    # Tasa de transmisión ajustada por eficacia, cobertura y adherencia
    beta = (contact_rate * transmission_probs[disease]) / N
    effective_beta = beta * (1 - efficacies[disease] * coverage * adherence)

    for i in range(1, days):
        new_infections = effective_beta * S[i-1] * I[i-1] + external_infections[disease]
        recoveries = gamma * I[i-1]

        S[i] = S[i-1] - new_infections + recoveries
        I[i] = I[i-1] + new_infections - recoveries

        # Evitar valores negativos
        S[i] = max(S[i], 0)
        I[i] = max(I[i], 0)

    results[disease] = {
        'S': S,
        'I': I
    }

# ---------------------------
# GRÁFICOS
# ---------------------------
for disease in results:
    plt.figure(figsize=(8, 5))
    plt.plot(t, results[disease]['I'], label=f'Infectados - {disease.capitalize()}', color='red')
    plt.plot(t, results[disease]['S'], label=f'Susceptibles - {disease.capitalize()}', color='green')
    plt.title(f'Evolución de {disease.capitalize()} con DoxyPEP y reinfecciones')
    plt.xlabel('Días')
    plt.ylabel('Personas')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# ---------------------------
# TABLA RESUMEN FINAL
# ---------------------------
summary_data = {
    'ITS': [],
    'Infectados al inicio': [],
    'Infectados al final': []
}

for disease in results:
    summary_data['ITS'].append(disease)
    summary_data['Infectados al inicio'].append(int(results[disease]['I'][0]))
    summary_data['Infectados al final'].append(int(results[disease]['I'][-1]))

summary_df = pd.DataFrame(summary_data)
print("\nResumen final de la simulación:")
print(summary_df)


