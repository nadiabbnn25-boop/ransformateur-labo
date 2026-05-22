import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="PFE Transformateur", layout="wide")
st.title("Étude, simulation et optimisation des pertes et du rendement d’un transformateur de puissance")

onglets = st.tabs(["⚡ Mode Industriel (Théorie)", "🔬 Mode Laboratoire (Expérimental)"])

# ==========================================
# ONGLET 1 : MODE INDUSTRIEL
# ==========================================
with onglets[0]:
    st.header("Simulation d'un Transformateur de Puissance")
    
    st.info("**Plaque signalétique :** 100 kVA | 20 kV / 400 V | 50 Hz")

    # ====================== WIDGETS EN PREMIER ======================
    col1, col2, col3, col4 = st.columns(4)
    Sn = col1.number_input("Puissance Nominale Sn (VA)", value=100000, step=10000)
    P0 = col2.number_input("Pertes Fer P0 (W)", value=500, step=50)
    Pcc = col3.number_input("Pertes Joule Pcc (W)", value=1500, step=100)
    cos_phi = col4.slider("Facteur de puissance (cos φ)", 
                          min_value=0.5, 
                          max_value=1.0, 
                          value=0.8, 
                          step=0.05)

    # ====================== CALCULS (juste après les widgets) ======================
    beta = np.arange(0.0, 1.55, 0.05)
    beta_opt = np.sqrt(P0 / Pcc) if Pcc > 0 else 0.0

    P_utile = beta * Sn * cos_phi
    Pj = (beta ** 2) * Pcc
    Pfer = np.full_like(beta, P0)
    P_tot = Pfer + Pj

    eta = 100 * P_utile / (P_utile + P0 + Pj + 1e-9)

    # Rendement au point optimal
    P_utile_opt = beta_opt * Sn * cos_phi
    eta_max = 100 * P_utile_opt / (P_utile_opt + 2 * P0 + 1e-9)

    # ====================== AFFICHAGE ======================
    st.success(f"**β optimal = {beta_opt:.3f}** | **Rendement maximal = {eta_max:.2f}%** (pour cos φ = {cos_phi:.2f})")

    # Debug : pour vérifier que le curseur fonctionne
    st.caption(f"Valeur actuelle du curseur cos φ = **{cos_phi:.2f}**")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("Bilan des Pertes")
        fig1, ax1 = plt.subplots()
        ax1.plot(beta, Pfer, 'r--', label='Pertes fer')
        ax1.plot(beta, Pj, 'b-.', label='Pertes Joule')
        ax1.plot(beta, P_tot, 'k-', linewidth=2, label='Pertes Totales')
        ax1.axvline(x=beta_opt, color='black', linestyle='--', label=f'β opt = {beta_opt:.3f}')
        ax1.set_xlabel('Taux de charge (β)')
        ax1.set_ylabel('Pertes (W)')
        ax1.legend()
        ax1.grid(True)
        st.pyplot(fig1)
        plt.close(fig1)

    with col_g2:
        st.subheader("Rendement selon cos φ")
        fig2, (ax2, ax_zoom) = plt.subplots(2, 1, figsize=(7, 8))

        for c, color, lw in zip([0.7, cos_phi, 1.0], ['red', 'navy', 'green'], [1.5, 3.0, 1.5]):
            P_u = beta * Sn * c
            eta_c = 100 * P_u / (P_u + P0 + Pcc * beta**2 + 1e-9)
            style = '-' if abs(c - cos_phi) < 0.01 else '--'
            ax2.plot(beta, eta_c, color=color, linewidth=lw, linestyle=style, 
                    label=f"cos(φ) = {c:.2f}")
            ax_zoom.plot(beta, eta_c, color=color, linewidth=lw, linestyle=style, 
                        label=f"cos(φ) = {c:.2f}")

        for ax in (ax2, ax_zoom):
            ax.axvline(x=beta_opt, color='black', linestyle='--', label='β optimal')
            ax.set_xlabel('Taux de charge (β)')
            ax.set_ylabel('Rendement (%)')
            ax.legend()
            ax.grid(True)

        ax2.set_ylim(0, 105)
        ax_zoom.set_ylim(65, 100)
        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    # ====================== ANALYSE ======================
    col_analyse1, col_analyse2 = st.columns(2)
    with col_analyse1:
        st.subheader("Analyse de l'optimisation")
        st.write(f"""
        Le point optimal est atteint pour **β = {beta_opt:.3f}**.  
        À ce point :
        - Pertes fer = Pertes Joule
        - Rendement maximal = **{eta_max:.2f} %** (avec cos φ = {cos_phi:.2f})
        - Un cos φ plus élevé améliore fortement le rendement.
        """)
        st.info("💡 Chargez le transformateur proche de β = {:.3f} pour avoir le meilleur rendement.".format(beta_opt))
