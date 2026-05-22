import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("TEST PERTES")

# ENTRÉES
P0_val  = st.number_input("Pertes Fer P0 (W)",    value=500,  step=50)
Pcc_val = st.number_input("Pertes Joule Pcc (W)", value=1500, step=100)

# VÉRIFICATION VISUELLE
st.write(f"✅ P0  utilisé = **{P0_val}**")
st.write(f"✅ Pcc utilisé = **{Pcc_val}**")

# CALCULS
beta      = np.arange(0, 1.55, 0.05)
Pfer      = np.full_like(beta, float(P0_val))
Pj        = (beta**2) * float(Pcc_val)
Ptot      = Pfer + Pj

# GRAPHIQUE
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(beta, Pfer, 'r--', linewidth=2, label=f'Pertes fer = {P0_val} W')
ax.plot(beta, Pj,   'b-.', linewidth=2, label='Pertes Joule')
ax.plot(beta, Ptot, 'k',   linewidth=2, label='Pertes Totales')
ax.set_xlabel('β')
ax.set_ylabel('Pertes (W)')
ax.legend()
ax.grid(True)
st.pyplot(fig)
plt.close(fig)
