import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────
# Configuration de la page
# ─────────────────────────────────────────
st.set_page_config(page_title="PFE Transformateur", layout="wide")
st.title(
    "Étude, simulation et optimisation des pertes et du rendement "
    "d'un transformateur de puissance"
)

# ─────────────────────────────────────────
# Onglets principaux
# ─────────────────────────────────────────
onglets = st.tabs(["⚡ Mode Industriel (Théorie)", "🔬 Mode Laboratoire (Expérimental)"])


# ==========================================
# ONGLET 1 : MODE INDUSTRIEL (Version corrigée)
# ==========================================
with onglets[0]:
    st.header("Simulation d'un Transformateur de Puissance")

    # Image
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image("https://i.postimg.cc/wxJcNW7K/shema-transfo.png", 
                 caption="Principe de fonctionnement", width=500)

    st.info("**Plaque signalétique :** 100 kVA | 20 kV / 400 V | 50 Hz")

    # ====================== PARAMÈTRES ======================
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    Sn      = col_p1.number_input("Puissance Nominale Sn (VA)", value=100000, step=10000)
    P0      = col_p2.number_input("Pertes à vide P0 (W)", value=500, step=50)
    Pcc     = col_p3.number_input("Pertes en court-circuit Pcc (W)", value=1500, step=100)
    cos_phi = col_p4.slider("Facteur de puissance (cos φ)", 0.5, 1.0, 0.8, step=0.05)

    # ====================== CALCULS (placés APRÈS les widgets) ======================
    beta = np.arange(0.0, 1.55, 0.05)
    beta_opt = np.sqrt(P0 / Pcc) if Pcc > 0 else 0.0

    # Calculs qui dépendent de cos_phi
    P_utile = beta * Sn * cos_phi
    Pj      = beta**2 * Pcc
    Pfer    = np.full_like(beta, P0)
    P_tot   = Pfer + Pj

    # Rendement
    eta = 100 * P_utile / (P_utile + P0 + Pj + 1e-9)

    # Rendement maximal au point optimal
    P_utile_opt = beta_opt * Sn * cos_phi
    eta_max = 100 * P_utile_opt / (P_utile_opt + 2 * P0 + 1e-9)

    st.success(f"**β optimal = {beta_opt:.3f}** | **Rendement max = {eta_max:.2f} %** (à cos φ = {cos_phi})")

    # ====================== GRAPHIQUES ======================
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("Bilan des Pertes")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.plot(beta, Pfer, 'r--', label='Pertes fer (fixes)')
        ax1.plot(beta, Pj, 'b-.', label='Pertes Joule (variables)')
        ax1.plot(beta, P_tot, 'k-', linewidth=2, label='Pertes totales')
        ax1.axvline(beta_opt, color='gray', linestyle='--', label=f'β optimal = {beta_opt:.3f}')
        ax1.set_xlabel('Taux de charge β')
        ax1.set_ylabel('Pertes (W)')
        ax1.legend()
        ax1.grid(True, alpha=0.6)
        st.pyplot(fig1)
        plt.close(fig1)

    with col_g2:
        st.subheader("Courbes de Rendement")
        fig2, (ax_top, ax_zoom) = plt.subplots(2, 1, figsize=(6, 7), gridspec_kw={'hspace': 0.4})

        cos_values = [0.7, cos_phi, 1.0]
        colors = ['red', 'navy', 'green']
        styles = ['--', '-', ':']

        for c, color, sty in zip(cos_values, colors, styles):
            P_u = beta * Sn * c
            eta_c = 100 * P_u / (P_u + P0 + (beta**2 * Pcc) + 1e-9)
            label = f"cos(φ) = {c:.2f}"
            if abs(c - cos_phi) < 0.01:           # Met en valeur la courbe sélectionnée
                linewidth = 3.0
                alpha = 1.0
            else:
                linewidth = 1.5
                alpha = 0.7
            ax_top.plot(beta, eta_c, color=color, linestyle=sty, linewidth=linewidth, 
                       alpha=alpha, label=label)
            ax_zoom.plot(beta, eta_c, color=color, linestyle=sty, linewidth=linewidth, 
                        alpha=alpha, label=label)

        for ax in [ax_top, ax_zoom]:
            ax.axvline(beta_opt, color='black', linestyle='--', linewidth=1, label='β optimal')
            ax.set_xlabel('Taux de charge β')
            ax.set_ylabel('Rendement (%)')
            ax.legend()
            ax.grid(True, alpha=0.6)

        ax_top.set_ylim(0, 105)
        ax_top.set_title("Rendement - Vue globale")
        ax_zoom.set_ylim(60, 105)
        ax_zoom.set_title("Zoom sur la zone utile (60% – 105%)")

        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    # ====================== ANALYSE DE L'OPTIMISATION ======================
    col_gauche, col_droite = st.columns([1.1, 0.9])

    with col_gauche:
        st.subheader("Analyse de l'optimisation")
        st.write(f"""
        Le point optimal est atteint pour **β = {beta_opt:.3f}**.  
        À ce point :
        - Les pertes fer = pertes Joule
        - Le rendement maximal est de **{eta_max:.2f} %** pour cos(φ) = **{cos_phi:.2f}**
        - Plus le **cos φ est élevé**, meilleur est le rendement
        """)
        
        st.info("💡 Conseil : Faire fonctionner le transformateur proche de β = {:.3f} permet de minimiser les pertes.".format(beta_opt))

    with col_droite:
        st.subheader("Influence du cos φ sur le rendement maximal")
        cos_range = np.linspace(0.5, 1.0, 100)
        eta_vs_cos = []
        for c in cos_range:
            pu = beta_opt * Sn * c
            eta_vs_cos.append(100 * pu / (pu + 2 * P0 + 1e-9))

        fig3, ax3 = plt.subplots(figsize=(5, 4))
        ax3.plot(cos_range, eta_vs_cos, 'navy', linewidth=2.5)
        ax3.scatter([cos_phi], [eta_max], color='red', s=80, zorder=5)
        ax3.axvline(cos_phi, color='red', linestyle='--', alpha=0.7)
        ax3.set_xlabel("cos φ")
        ax3.set_ylabel("Rendement maximal (%)")
        ax3.set_title("Rendement max à β optimal")
        ax3.grid(True, alpha=0.6)
        st.pyplot(fig3)
        plt.close(fig3)


# ══════════════════════════════════════════
# ONGLET 2 – MODE LABORATOIRE
# ══════════════════════════════════════════
with onglets[1]:
    st.header("Exploitation Expérimentale")

    R1, R2, P10 = 9.5, 2.5, 8.0

    donnees = pd.DataFrame({
        "I1 (A)": [0.06, 0.19, 0.24, 0.37, 0.50, 0.64, 0.80, 0.86],
        "P1 (W)": [8.0,  38.0, 49.0, 73.0, 100.0, 119.0, 136.0, 140.0],
        "U2 (V)": [104.3, 102.0, 101.0, 96.0, 94.0, 87.0, 78.0, 72.0],
        "I2 (A)": [0.0,  0.29, 0.40, 0.64, 0.92, 1.18, 1.50, 1.65],
        "P2 (W)": [0.0,  30.0, 42.0, 67.0, 88.0, 104.0, 119.0, 120.0],
    })

    df = st.data_editor(donnees, use_container_width=True)

    # Protection division par zéro
    eta_labo = np.where(
        df["P1 (W)"] > 0,
        (df["P2 (W)"] / df["P1 (W)"]) * 100,
        0.0,
    )

    col_l1, col_l2, col_l3 = st.columns(3)

    # ── Graphique L1 : Rendement mesuré ─────────────────────────
    with col_l1:
        st.write("#### Rendement mesuré")
        fig_l1, ax_l1 = plt.subplots()
        ax_l1.plot(df["I2 (A)"], eta_labo, "-o", color="green")
        ax_l1.set_xlabel("I2 (A)")
        ax_l1.set_ylabel("Rendement (%)")
        ax_l1.set_ylim(0, 105)
        ax_l1.grid(True)
        fig_l1.tight_layout()
        st.pyplot(fig_l1)
        plt.close(fig_l1)

    # ── Graphique L2 : Tension secondaire ───────────────────────
    with col_l2:
        st.write("#### Tension secondaire U2")
        fig_l2, ax_l2 = plt.subplots()
        ax_l2.plot(df["I2 (A)"], df["U2 (V)"], "-o", color="red")
        ax_l2.set_xlabel("I2 (A)")
        ax_l2.set_ylabel("U2 (V)")
        ax_l2.grid(True)
        fig_l2.tight_layout()
        st.pyplot(fig_l2)
        plt.close(fig_l2)

    # ── Graphique L3 : Pertes mesuré vs estimé ──────────────────
    with col_l3:
        st.write("#### Pertes : mesuré vs estimé")
        pertes_mesurees = df["P1 (W)"] - df["P2 (W)"]
        pertes_estimees = P10 + R1 * df["I1 (A)"] ** 2 + R2 * df["I2 (A)"] ** 2

        fig_l3, ax_l3 = plt.subplots()
        ax_l3.plot(df["I2 (A)"], pertes_mesurees, "-o",  label="Mesuré")
        ax_l3.plot(df["I2 (A)"], pertes_estimees, "--s", label="Estimé")
        ax_l3.set_xlabel("I2 (A)")
        ax_l3.set_ylabel("Pertes (W)")
        ax_l3.legend()
        ax_l3.grid(True)
        fig_l3.tight_layout()
        st.pyplot(fig_l3)
        plt.close(fig_l3)
