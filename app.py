import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="PFE Transformateur", layout="wide")
st.title("Étude, simulation et optimisation des pertes et du rendement d'un transformateur")

onglets = st.tabs(["⚡ Mode Industriel (Théorie)", "🔬 Mode Laboratoire (Expérimental)"])

with onglets[0]:
    st.image("https://i.postimg.cc/wxJcNW7K/shema-transfo.png", width=500)
    c1, c2, c3, c4 = st.columns(4)
    Sn = c1.number_input("Sn (VA)", value=100000)
    P0 = c2.number_input("P0 (W)", value=500)
    Pcc = c3.number_input("Pcc (W)", value=1500)
    cos_phi = c4.slider("cos φ", 0.5, 1.0, 0.8)

    beta = np.linspace(0.01, 1.5, 100)
    
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    ax1.plot(beta, [P0]*len(beta), 'r--', label='Pertes fer')
    ax1.plot(beta, Pcc * beta**2, 'b-.', label='Pertes Joule')
    ax1.plot(beta, P0 + Pcc * beta**2, 'k', label='Totales')
    ax1.set(xlabel='β', ylabel='Pertes (W)', title="Bilan des Pertes"); ax1.legend(); ax1.grid(True)
    st.pyplot(fig1)
    
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    for c in [0.7, 0.85, 1.0]:
        eta = 100 * (beta * Sn * c) / ((beta * Sn * c) + P0 + (Pcc * beta**2) + 1e-9)
        style = '-' if c == cos_phi else '--'
        ax2.plot(beta, eta, style, linewidth=2.5 if c == cos_phi else 1, label=f'cosφ={c}')
    ax2.set(xlabel='β', ylabel='η (%)', title="Rendement"); ax2.set_ylim(0, 105); ax2.grid(True); ax2.legend()
    st.pyplot(fig2)

with onglets[1]:
    st.header("Exploitation Expérimentale")
    df = pd.DataFrame({"I2 (A)": [0.0, 0.29, 0.40, 0.64, 0.92, 1.18, 1.50, 1.65],
                       "P1 (W)": [8.0, 38.0, 49.0, 73.0, 100.0, 119.0, 136.0, 140.0],
                       "P2 (W)": [0.0, 30.0, 42.0, 67.0, 88.0, 104.0, 119.0, 120.0],
                       "U2 (V)": [104.3, 102.0, 101.0, 96.0, 94.0, 87.0, 78.0, 72.0]})
    st.dataframe(df)
    for i, titre in enumerate(["Rendement", "Caractéristique U2(I2)", "Pertes"]):
        fig, ax = plt.subplots(figsize=(6, 3))
        if i == 0: ax.plot(df["I2 (A)"], (df["P2 (W)"]/df["P1 (W)"])*100, 'o-'); ax.set(ylabel="η (%)")
        elif i == 1: ax.plot(df["I2 (A)"], df["U2 (V)"], 'ro-'); ax.set(ylabel="U2 (V)")
        else: ax.plot(df["I2 (A)"], df["P1 (W)"]-df["P2 (W)"], 'ko-'); ax.set(ylabel="Pertes (W)")
        ax.set(title=titre, xlabel='I2 (A)'); ax.grid(True); st.pyplot(fig)
