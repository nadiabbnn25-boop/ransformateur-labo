import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Test Pertes", layout="wide")
st.title("Test Réactivité - Courbe des Pertes")

st.info("Modifie les valeurs de P0 et Pcc → la courbe doit se mettre à jour immédiatement")

# ====================== WIDGETS ======================
col1, col2, col3 = st.columns(3)
Sn = col1.number_input("Puissance Nominale Sn (VA)", value=100000, step=10000, key="sn_key")
P0 = col2.number_input("Pertes Fer P0 (W)", value=500, step=10, key="p0_key")
Pcc = col3.number_input("Pertes Joule Pcc (W)", value=1500, step=50, key="pcc_key")

# ====================== CALCULS IMMÉDIATS ======================
beta = np.arange(0.0, 1.51, 0.05)
beta_opt = np.sqrt(P0 / Pcc) if Pcc > 0 else 0.0

Pfer = np.full_like(beta, float(P0))
Pj   = (beta ** 2) * float(Pcc)
Ptot = Pfer + Pj

# ====================== AFFICHAGE DEBUG ======================
st.write(f"**Valeurs actuelles :** P0 = {P0} W | Pcc = {Pcc} W | β optimal = {beta_opt:.3f}")

st.write(f"**Pertes totales à β=1 :** {Ptot[-1]:.0f} W")

# ====================== GRAPHIQUE ======================
fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(beta, Pfer, 'r--', linewidth=2, label=f'Pertes fer (fixes) = {P0} W')
ax.plot(beta, Pj,   'b-.', linewidth=2, label='Pertes Joule (variables)')
ax.plot(beta, Ptot, 'k-',  linewidth=2.5, label='Pertes Totales')

ax.axvline(x=beta_opt, color='gray', linestyle='--', linewidth=2, 
           label=f'β optimal = {beta_opt:.3f}')

ax.set_xlabel("Taux de charge β", fontsize=12)
ax.set_ylabel("Pertes (W)", fontsize=12)
ax.set_title("Évolution des Pertes en fonction du taux de charge", fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.7)

st.pyplot(fig)
plt.close(fig)

# ====================== ANALYSE ======================
st.subheader("Observation")
st.write("""
- Les **pertes fer** restent constantes quelle que soit la charge.
- Les **pertes Joule** augmentent avec le carré du taux de charge.
- Le point optimal (β optimal) est là où les deux courbes se croisent.
""")

st.success(f"Point optimal à β = {beta_opt:.3f} → Pertes fer = Pertes Joule = {P0:.0f} W")
