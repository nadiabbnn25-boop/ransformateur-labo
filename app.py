import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="PFE Transformateur", layout="wide")
st.title("Étude, simulation et optimisation des pertes et du rendement d’un transformateur de puissance")

# Création des deux onglets
onglets = st.tabs(["⚡ Mode Industriel (Théorie)", "🔬 Mode Laboratoire (Expérimental)"])

# ==========================================
# ONGLET 1 : MODE INDUSTRIEL
# ==========================================
with onglets[0]:
    st.header("Simulation d'un Transformateur de Puissance")
    
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        st.image("https://i.postimg.cc/wxJcNW7K/shema-transfo.png", caption="Principe de fonctionnement", width=500)
    
    st.info("**Plaque signalétique :** 100 kVA | 20 kV / 400 V | 50 Hz")
    
    col_param1, col_param2, col_param3, col_param4 = st.columns(4)
    Sn = col_param1.number_input("Puissance Nominale Sn (VA)", value=100000, step=10000)
    P0 = col_param2.number_input("Pertes Fer P0 (W)", value=500, step=50)
    Pcc = col_param3.number_input("Pertes Joule Pcc (W)", value=1500, step=100)
    cos_phi = col_param4.slider("Facteur de puissance (cos φ)", 0.5, 1.0, 0.8)

    # Calculs théoriques
    beta = np.arange(0, 1.55, 0.05)
    beta_opt = np.sqrt(P0 / Pcc) if Pcc > 0 else 0
    P2 = beta * Sn * cos_phi
    Pj = (beta**2) * Pcc
    Pfer = np.full_like(beta, P0)
    P_tot = Pfer + Pj
    
    st.success(f"Rendement maximal théorique : **β optimal = {beta_opt:.3f}**")

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
    st.write("#### Rendement pour différents cos(φ)")

    fig2, ax2 = plt.subplots()

    # Liste des facteurs de puissance
    cos_values = [0.6, 0.8, 1.0]
    couleurs = ['r', 'g', 'b']

    for cosv, c in zip(cos_values, couleurs):

        # Puissance utile
        P2 = beta * Sn * cosv

        # Rendement
        eta = 100 * P2 / (P2 + P0 + Pj + 1e-9)

        # Tracé
        ax2.plot(
            beta,
            eta,
            linewidth=2,
            color=c,
            label=f'cos(φ) = {cosv}'
        )

    # Ligne β optimal
    ax2.axvline(
        x=beta_opt,
        color='k',
        linestyle='--',
        label='β optimal'
    )

    ax2.set_xlabel('Taux de charge (β)')
    ax2.set_ylabel('Rendement (%)')
    ax2.set_ylim(0, 105)

    ax2.legend()
    ax2.grid(True)

    st.pyplot(fig2)
 # =========================
# Graphe Zoom Rendement
# =========================
col_zoom1, col_zoom2 = st.columns(2)

with col_zoom2:

    st.write("#### Zoom sur le rendement maximal")

    fig_zoom, ax_zoom = plt.subplots()

    for cosv, c in zip(cos_values, couleurs):

        P2 = beta * Sn * cosv
        eta = 100 * P2 / (P2 + P0 + Pj + 1e-9)

        ax_zoom.plot(
            beta,
            eta,
            linewidth=2,
            color=c,
            label=f'cos(φ) = {cosv}'
        )

    ax_zoom.axvline(
        x=beta_opt,
        color='k',
        linestyle='--',
        label='β optimal'
    )

    ax_zoom.set_xlabel('Taux de charge (β)')
    ax_zoom.set_ylabel('Rendement (%)')

    # Zoom vertical
    ax_zoom.set_ylim(70, 100)

    ax_zoom.grid(True)
    ax_zoom.legend()

    fig_zoom.tight_layout()

    st.pyplot(fig_zoom)
# ==========================================
# ONGLET 2 : MODE LABORATOIRE
# ==========================================
with onglets[1]:
    st.header("Exploitation Expérimentale")
    R1, R2, P10 = 9.5, 2.5, 8.0
    donnees = pd.DataFrame({
        "I1 (A)": [0.06, 0.19, 0.24, 0.37, 0.50, 0.64, 0.80, 0.86],
        "P1 (W)": [8.0, 38.0, 49.0, 73.0, 100.0, 119.0, 136.0, 140.0],
        "U2 (V)": [104.3, 102.0, 101.0, 96.0, 94.0, 87.0, 78.0, 72.0],
        "I2 (A)": [0.0, 0.29, 0.40, 0.64, 0.92, 1.18, 1.50, 1.65],
        "P2 (W)": [0.0, 30.0, 42.0, 67.0, 88.0, 104.0, 119.0, 120.0]
    })
    df = st.data_editor(donnees, use_container_width=True)
    
    col_g3, col_g4, col_g5 = st.columns(3)
    with col_g3:
        fig3, ax3 = plt.subplots(); ax3.plot(df["I2 (A)"], (df["P2 (W)"]/df["P1 (W)"])*100, '-o')
        ax3.set(xlabel='I2 (A)', ylabel='Rendement (%)'); ax3.grid(True); st.pyplot(fig3)
    with col_g4:
        fig5, ax5 = plt.subplots(); ax5.plot(df["I2 (A)"], df["U2 (V)"], '-o', color='red')
        ax5.set(xlabel='I2 (A)', ylabel='U2 (V)'); ax5.grid(True); st.pyplot(fig5)
    with col_g5:
        fig4, ax4 = plt.subplots(); ax4.plot(df["I2 (A)"], df["P1 (W)"]-df["P2 (W)"], label='Mesuré')
        ax4.plot(df["I2 (A)"], P10 + (R1*df["I1 (A)"]**2 + R2*df["I2 (A)"]**2), '--', label='Estimé')
        ax4.set(xlabel='I2 (A)', ylabel='Pertes (W)'); ax4.legend(); ax4.grid(True); st.pyplot(fig4)
