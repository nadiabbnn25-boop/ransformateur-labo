import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ... (votre config de page et onglets) ...

with onglets[0]:
    # ... (vos entrées : Sn, P0, etc.) ...
    
    # 1. Graphique des pertes (Isolé)
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    ax1.plot(beta, [P0]*len(beta), 'r--', label='Pertes fer')
    ax1.plot(beta, Pcc * beta**2, 'b-.', label='Pertes Joule')
    ax1.plot(beta, P0 + Pcc * beta**2, 'k', label='Totales')
    ax1.set(xlabel='β', ylabel='Pertes (W)', title="Bilan des Pertes")
    ax1.legend(); ax1.grid(True)
    st.pyplot(fig1)

    # 2. Graphique du rendement (Isolé)
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    for c in [0.7, 0.85, 1.0]:
        eta = 100 * (beta * Sn * c) / ((beta * Sn * c) + P0 + (Pcc * beta**2) + 1e-9)
        style = '-' if c == cos_phi else '--'
        ax2.plot(beta, eta, style, linewidth=2, label=f'cosφ={c}')
    ax2.set(xlabel='β', ylabel='η (%)', title="Rendement (3 facteurs de puissance)")
    ax2.set_ylim(0, 105)
    ax2.grid(True); ax2.legend()
    st.pyplot(fig2)
