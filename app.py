import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="PFE Transformateur", layout="wide")
st.title("Étude, simulation et optimisation des pertes et du rendement")

onglets = st.tabs(["⚡ Mode Industriel (Théorie)", "🔬 Mode Laboratoire (Expérimental)"])

# --- ONGLET 1 : INDUSTRIEL ---
with onglets[0]:
    c1, c2, c3, c4 = st.columns(4)
    Sn = c1.number_input("Sn (VA)", value=100000)
    P0 = c2.number_input("P0 (W)", value=500)
    Pcc = c3.number_input("Pcc (W)", value=1500)
    cos_phi = c4.slider("cos φ (Curseur)", 0.5, 1.0, 0.8)

    beta = np.linspace(0.0, 1.5, 100)
    beta_opt = np.sqrt(P0 / Pcc)

    # Fig 1 : Pertes
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(beta, [P0]*len(beta), 'b--', label='Pertes fer')
    ax1.plot(beta, Pcc * beta**2, 'c-.', label='Pertes Joule')
    ax1.plot(beta, P0 + Pcc * beta**2, 'k', label='Totales')
    ax1.set(title="Bilan des Pertes"); ax1.legend(); ax1.grid(True)
    st.pyplot(fig1)

    # Fig 2 : Rendement (Analyse à gauche, Graphique à droite)
    col_gauche, col_droite = st.columns([1, 2])
    with col_gauche:
        st.subheader("Analyse de l'optimisation")
        st.write(f"Le point optimal est atteint pour **β = {beta_opt:.3f}**. "
                 "À ce point, les pertes fer égales les pertes Joule. Un cos(φ) élevé "
                 "maximise le rendement.")
        st.info("💡 Travaillez proche de β_opt pour minimiser les pertes.")
    with col_droite:
        st.write("#### Zoom sur le rendement (60-105%)")
        fig_zoom, ax_zoom = plt.subplots(figsize=(6, 3.5))
        for c in sorted(list(set([0.7, cos_phi, 1.0]))):
            P_utile = Sn * beta * c
            eta = 100 * P_utile / (P_utile + P0 + (Pcc * beta**2) + 1e-9)
            if abs(c - cos_phi) < 0.001:
                ax_zoom.plot(beta, eta, color='navy', linewidth=2.0, label=f'cosφ={c:.2f}')
            elif c == 0.7:
                ax_zoom.plot(beta, eta, color='red', linestyle='--', linewidth=1.2, label='cosφ=0.7')
            else:
                ax_zoom.plot(beta, eta, color='green', linestyle=':', linewidth=1.2, label='cosφ=1.0')
        ax_zoom.axvline(x=beta_opt, color='k', linestyle='-', linewidth=0.8, label='β opt')
        ax_zoom.set_ylim(60, 105) # Le fameux zoom qui commence à 60
        ax_zoom.set(xlabel='β', ylabel='η (%)'); ax_zoom.grid(True); ax_zoom.legend(fontsize='x-small')
        fig_zoom.tight_layout(); st.pyplot(fig_zoom)

# --- ONGLET 2 : LABORATOIRE ---
with onglets[1]:
    df = pd.DataFrame({"I2 (A)": [0.0, 0.29, 0.40, 0.64, 0.92, 1.18, 1.50, 1.65], 
                       "P1 (W)": [8.0, 38.0, 49.0, 73.0, 100.0, 119.0, 136.0, 140.0],
                       "P2 (W)": [0.0, 30.0, 42.0, 67.0, 88.0, 104.0, 119.0, 120.0],
                       "U2 (V)": [104.3, 102.0, 101.0, 96.0, 96.0, 87.0, 78.0, 72.0]})
    for i, titre in enumerate(["Rendement expérimental", "Caractéristique U2(I2)", "Pertes totales"]):
        fig, ax = plt.subplots(figsize=(8, 3))
        if i == 0: ax.plot(df["I2 (A)"], (df["P2 (W)"]/df["P1 (W)"])*100, 'o-'); ax.set(ylabel="η (%)")
        elif i == 1: ax.plot(df["I2 (A)"], df["U2 (V)"], 'ro-'); ax.set(ylabel="U2 (V)")
        else: ax.plot(df["I2 (A)"], df["P1 (W)"]-df["P2 (W)"], 'ko-'); ax.set(ylabel="Pertes (W)")
        ax.set(title=titre, xlabel='I2 (A)'); ax.grid(True); st.pyplot(fig)
        ax4.set(xlabel='I2 (A)', ylabel='Pertes (W)'); ax4.legend(); ax4.grid(True); st.pyplot(fig4)
