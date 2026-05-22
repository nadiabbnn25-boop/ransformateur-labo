import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration
st.set_page_config(page_title="PFE Transformateur", layout="wide")
st.title("Étude, simulation et optimisation des pertes et du rendement d'un transformateur")

# Création des onglets (C'est ici que 'onglets' est défini !)
onglets = st.tabs(["⚡ Mode Industriel (Théorie)", "🔬 Mode Laboratoire (Expérimental)"])

# --- MODE INDUSTRIEL ---
with onglets[0]:
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        st.image("https://i.postimg.cc/wxJcNW7K/shema-transfo.png", width=500)
    
    c1, c2, c3, c4 = st.columns(4)
    Sn = c1.number_input("Sn (VA)", value=100000)
    P0 = c2.number_input("P0 (W)", value=500)
    Pcc = c3.number_input("Pcc (W)", value=1500)
    cos_phi = c4.slider("cos φ", 0.5, 1.0, 0.8)

    beta = np.linspace(0.01, 1.5, 100)
    
    # Graphique 1 : Pertes
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(beta, [P0]*len(beta), 'r--', label='Pertes fer')
    ax1.plot(beta, Pcc * beta**2, 'b-.', label='Pertes Joule')
    ax1.plot(beta, P0 + Pcc * beta**2, 'k', label='Totales')
    ax1.set(xlabel='β', ylabel='Pertes (W)', title="Bilan des Pertes"); ax1.legend(); ax1.grid(True)
    st.pyplot(fig1)

    # Graphique 2 : Rendement avec les 3 courbes
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    for c in [0.7, 0.85, 1.0]:
        eta = 100 * (beta * Sn * c) / ((beta * Sn * c) + P0 + (Pcc * beta**2) + 1e-9)
        style = '-' if c == cos_phi else '--'
        ax2.plot(beta, eta, style, linewidth=2, label=f'cosφ={c}')
    ax2.set(xlabel='β', ylabel='η (%)', title="Rendement (3 facteurs de puissance)"); ax2.set_ylim(0, 105); ax2.grid(True); ax2.legend()
    st.pyplot(fig2)

# --- MODE LABORATOIRE ---
with onglets[1]:
    st.header("Exploitation Expérimentale")
    df = pd.DataFrame({
        "I2 (A)": [0.0, 0.29, 0.40, 0.64, 0.92, 1.18, 1.50, 1.65],
        "P1 (W)": [8.0, 38.0, 49.0, 73.0, 100.0, 119.0, 136.0, 140.0],
        "P2 (W)": [0.0, 30.0, 42.0, 67.0, 88.0, 104.0, 119.0, 120.0],
        "U2 (V)": [104.3, 102.0, 101.0, 96.0, 94.0, 87.0, 78.0, 72.0]
    })
    st.dataframe(df)
    
    fig3, (ax3, ax4, ax5) = plt.subplots(1, 3, figsize=(15, 4))
    ax3.plot(df["I2 (A)"], (df["P2 (W)"]/df["P1 (W)"])*100, 'o-'); ax3.set(xlabel='I2', ylabel='η (%)', title="Rendement exp."); ax3.grid(True); ax3.set_ylim(0, 105)
    ax4.plot(df["I2 (A)"], df["U2 (V)"], 'ro-'); ax4.set(xlabel='I2', ylabel='U2 (V)', title="Caractéristique U2(I2)"); ax4.grid(True)
    ax5.plot(df["I2 (A)"], df["P1 (W)"]-df["P2 (W)"], 'ko-'); ax5.set(xlabel='I2', ylabel='Pertes (W)', title="Pertes totales"); ax5.grid(True)
    st.pyplot(fig3)
