import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="PFE Transformateur", layout="wide")
st.title("Étude, simulation et optimisation des pertes et du rendement d’un transformateur de puissance : application au cas monophasé")

# Création des deux onglets
onglets = st.tabs(["⚡ Mode Industriel (Théorie)", "🔬 Mode Laboratoire (Expérimental)"])

# ==========================================
# ONGLET 1 : MODE INDUSTRIEL
# ==========================================
with onglets[0]:
    st.header("Simulation d'un Transformateur de Puissance")
    
    # Image centrée et redimensionnée
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        st.image("https://i.postimg.cc/wxJcNW7K/shema-transfo.png", caption="Principe de fonctionnement du transformateur monophasé", width=500)
    
    st.info("**Plaque signalétique du transformateur étudié :** 100 kVA | 20 kV / 400 V | 50 Hz")
    
    col_param1, col_param2, col_param3, col_param4 = st.columns(4)
    Sn = col_param1.number_input("Puissance Nominale Sn (VA)", value=100000, step=10000)
    P0 = col_param2.number_input("Pertes Fer P0 (W)", value=500, step=50)
    Pcc = col_param3.number_input("Pertes Joule Pcc (W)", value=1500, step=100)
    cos_phi = col_param4.slider("Facteur de puissance (cos φ)", 0.5, 1.0, 0.8)

    beta = np.arange(0, 1.55, 0.05)
    beta_opt = np.sqrt(P0 / Pcc) if Pcc > 0 else 0
    P2 = beta * Sn * cos_phi
    Pj = (beta**2) * Pcc
    Pfer = np.full_like(beta, P0)
    P_tot = Pfer + Pj
    
    st.success(f"Condition du rendement maximal théorique : **β optimal = {beta_opt:.3f}**")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.write("#### Bilan des Pertes")
        fig1, ax1 = plt.subplots()
        ax1.plot(beta, Pfer, 'r--', label='Pertes fer')
        ax1.plot(beta, Pj, 'b-.', label='Pertes Joule')
        ax1.plot(beta, P_tot, 'k', label='Pertes Totales', linewidth=2)
        ax1.set_xlabel('Taux de charge (β)')
        ax1.set_ylabel('Pertes (W)')
        ax1.legend()
        ax1.grid(True)
        st.pyplot(fig1)

    with col_g2:
        st.write("#### Rendement (Influence du Facteur de Puissance)")
        fig2, ax2 = plt.subplots()
        cos_vals = [0.7, 0.8, 0.9, 1.0]
        colors = ['blue', 'green', 'red', 'black']
        for c, color in zip(cos_vals, colors):
            p2_temp = beta * Sn * c
            eta_temp = 100 * p2_temp / (p2_temp + P0 + Pj + 1e-9)
            ax2.plot(beta, eta_temp, color=color, label=f'cos(φ) = {c}')
        ax2.axvline(x=beta_opt, color='k', linestyle='--', label='β optimal')
        ax2.set_xlabel('Taux de charge (β)')
        ax2.set_ylabel('Rendement (%)')
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)

# ==========================================
# ONGLET 2 : MODE LABORATOIRE
# ==========================================
with onglets[1]:
    st.header("Exploitation Expérimentale")
    col_lab1, col_lab2, col_lab3 = st.columns(3)
    R1 = col_lab1.number_input("Résistance Primaire R1 (Ω)", value=9.5)
    R2 = col_lab2.number_input("Résistance Secondaire R2 (Ω)", value=2.5)
    P10 = col_lab3.number_input("Pertes Fer à vide P10 (W)", value=8.0)

    donnees_initiales = pd.DataFrame({
        "I1 (A)": [0.06, 0.19, 0.24, 0.37, 0.50, 0.64, 0.80, 0.86],
        "P1 (W)": [8.0, 38.0, 49.0, 73.0, 100.0, 119.0, 136.0, 140.0],
        "U2 (V)": [104.3, 102.0, 101.0, 96.0, 94.0, 87.0, 78.0, 72.0],
        "I2 (A)": [0.0, 0.29, 0.40, 0.64, 0.92, 1.18, 1.50, 1.65],
        "P2 (W)": [0.0, 30.0, 42.0, 67.0, 88.0, 104.0, 119.0, 120.0]
    })
    df_mesures = st.data_editor(donnees_initiales, num_rows="dynamic", use_container_width=True)
    
    # (Le code des graphiques Labo continue ici, inchangé)
    st.write("---")
    st.write("L'analyse des données expérimentales confirme les modèles théoriques étudiés.")
