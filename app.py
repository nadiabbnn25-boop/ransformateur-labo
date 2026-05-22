import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration
st.set_page_config(page_title="Outil de Labo - Transformateur", layout="wide")
st.title("Exploitation Expérimentale du Transformateur")

# --- PARAMÈTRES FIXES ---
st.sidebar.header("Paramètres du modèle")
R1 = st.sidebar.number_input("Résistance Primaire R1 (Ω)", value=9.5)
R2 = st.sidebar.number_input("Résistance Secondaire R2 (Ω)", value=2.5)
P10 = st.sidebar.number_input("Pertes Fer à vide P10 (W)", value=8.0)

# --- TABLEAU DE SAISIE DYNAMIQUE ---
st.write("### Saisie des relevés de mesure")
st.write("Modifiez les valeurs du tableau ou ajoutez de nouvelles lignes en bas.")

# Données initiales (Vos relevés)
donnees_initiales = pd.DataFrame({
    "I1 (A)": [0.06, 0.19, 0.24, 0.37, 0.50, 0.64, 0.80, 0.86],
    "P1 (W)": [8.0, 38.0, 49.0, 73.0, 100.0, 119.0, 136.0, 140.0],
    "U2 (V)": [104.3, 102.0, 101.0, 96.0, 94.0, 87.0, 78.0, 72.0],
    "I2 (A)": [0.0, 0.29, 0.40, 0.64, 0.92, 1.18, 1.50, 1.65],
    "P2 (W)": [0.0, 30.0, 42.0, 67.0, 88.0, 104.0, 119.0, 120.0]
})

# Tableau modifiable par l'utilisateur (num_rows="dynamic" permet d'ajouter des lignes)
df_mesures = st.data_editor(donnees_initiales, num_rows="dynamic", use_container_width=True)

# --- CALCULS AUTOMATIQUES ---
# On convertit les colonnes en vecteurs NumPy pour les calculs
I1 = df_mesures["I1 (A)"].values
P1 = df_mesures["P1 (W)"].values
U2 = df_mesures["U2 (V)"].values
I2 = df_mesures["I2 (A)"].values
P2 = df_mesures["P2 (W)"].values

# Calcul du rendement (avec protection division par zéro)
eta_exp = np.zeros_like(P1, dtype=float)
masque_non_nul = P1 > 0
eta_exp[masque_non_nul] = (P2[masque_non_nul] / P1[masque_non_nul]) * 100

# Calcul des pertes
pertes_totales_exp = P1 - P2
pertes_joule_calc = (R1 * I1**2) + (R2 * I2**2)
pertes_estimees = P10 + pertes_joule_calc

# --- AFFICHAGE DES GRAPHIQUES ---
st.write("---")
st.write("### Analyse Graphique")

col1, col2 = st.columns(2)

with col1:
    st.write("**Rendement Expérimental**")
    fig1, ax1 = plt.subplots()
    ax1.plot(I2, eta_exp, '-o', color='#2563eb', linewidth=2, markersize=8)
    ax1.set_xlabel('Courant secondaire I2 (A)')
    ax1.set_ylabel('Rendement (%)')
    ax1.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig1)

with col2:
    st.write("**Comparaison des Pertes**")
    fig2, ax2 = plt.subplots()
    ax2.plot(I2, pertes_totales_exp, '-o', label='Pertes Totales (P1-P2)', markersize=8)
    ax2.plot(I2, pertes_estimees, '--s', label='Pertes Estimées (Modèle)', markersize=8)
    ax2.set_xlabel('Courant secondaire I2 (A)')
    ax2.set_ylabel('Pertes (W)')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig2)
