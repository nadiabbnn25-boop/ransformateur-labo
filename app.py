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


# ══════════════════════════════════════════
# ONGLET 1 – MODE INDUSTRIEL
# ══════════════════════════════════════════
with onglets[0]:
    st.header("Simulation d'un Transformateur de Puissance")

    # Image centrée
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        st.image(
            "https://i.postimg.cc/wxJcNW7K/shema-transfo.png",
            caption="Principe de fonctionnement",
            width=500,
        )

    st.info("**Plaque signalétique :** 100 kVA | 20 kV / 400 V | 50 Hz")

    # ── Paramètres ──────────────────────────────────────────────
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    Sn      = col_p1.number_input("Puissance Nominale Sn (VA)",  value=100_000, step=10_000)
    P0      = col_p2.number_input("Pertes Fer P0 (W)",           value=500,     step=50)
    Pcc     = col_p3.number_input("Pertes Joule Pcc (W)",        value=1_500,   step=100)
    cos_phi = col_p4.slider("Facteur de puissance (cos φ)",      0.5, 1.0, 0.8)

    # ── Calculs communs ─────────────────────────────────────────
    beta     = np.arange(0, 1.55, 0.05)
    beta_opt = np.sqrt(P0 / Pcc) if Pcc > 0 else 0.0

    Pj    = (beta ** 2) * Pcc
    Pfer  = np.full_like(beta, float(P0))
    P_tot = Pfer + Pj
    P2    = beta * Sn * cos_phi                          # puissance utile

    st.success(f"Rendement maximal théorique : **β optimal = {beta_opt:.3f}**")

    # ── Graphiques ──────────────────────────────────────────────
    col_g1, col_g2 = st.columns(2)

    # Graphique 1 : Bilan des pertes
    with col_g1:
        st.write("#### Bilan des Pertes")
        fig1, ax1 = plt.subplots()
        ax1.plot(beta, Pfer,  "r--", label="Pertes fer")
        ax1.plot(beta, Pj,    "b-.", label="Pertes Joule")
        ax1.plot(beta, P_tot, "k",   label="Pertes Totales", linewidth=2)
        ax1.set_xlabel("Taux de charge (β)")
        ax1.set_ylabel("Pertes (W)")
        ax1.legend()
        ax1.grid(True)
        fig1.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

    # Graphique 2 : Rendement (courbe interactive) + zoom
    with col_g2:
        st.write(f"#### Rendement pour différents cos(φ)")

        fig2, (ax2, ax_zoom) = plt.subplots(
            2, 1, figsize=(6, 7),
            gridspec_kw={"hspace": 0.45}
        )

        # Ensemble des cos(φ) à tracer : toujours 0.7, valeur curseur, 1.0
        cos_set = sorted({0.7, round(float(cos_phi), 2), 1.0})

        styles = {
            "active":  dict(color="navy",  linewidth=2.0, linestyle="-"),
            "low":     dict(color="red",   linewidth=1.2, linestyle="--"),
            "high":    dict(color="green", linewidth=1.2, linestyle=":"),
        }

        for c in cos_set:
            P_utile  = Sn * beta * c
            eta      = 100 * P_utile / (P_utile + P0 + Pcc * beta ** 2 + 1e-9)

            # Choix du style
            if abs(c - cos_phi) < 0.001:
                kw = styles["active"]
            elif c < cos_phi:
                kw = styles["low"]
            else:
                kw = styles["high"]

            label = f"cos(φ) = {c:.2f}"
            ax2.plot(beta, eta, label=label, **kw)
            ax_zoom.plot(beta, eta, label=label, **kw)

        for ax in (ax2, ax_zoom):
            ax.axvline(x=beta_opt, color="k", linestyle="--",
                       linewidth=0.9, label="β optimal")
            ax.set_xlabel("Taux de charge (β)")
            ax.set_ylabel("Rendement (%)")
            ax.legend(fontsize="x-small")
            ax.grid(True, alpha=0.6)

        # Vue globale
        ax2.set_ylim(0, 105)
        ax2.set_title("Vue globale")

        # Vue zoomée
        ax_zoom.set_ylim(60, 105)
        ax_zoom.set_title("Zoom (60 – 105 %)")

        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)


# ══════════════════════════════════════════
# ONGLET 2 – MODE LABORATOIRE
# ══════════════════════════════════════════
with onglets[1]:
    st.header("Exploitation Expérimentale")

    # Paramètres de la maquette
    R1, R2, P10 = 9.5, 2.5, 8.0

    donnees = pd.DataFrame({
        "I1 (A)": [0.06, 0.19, 0.24, 0.37, 0.50, 0.64, 0.80, 0.86],
        "P1 (W)": [8.0,  38.0, 49.0, 73.0, 100.0, 119.0, 136.0, 140.0],
        "U2 (V)": [104.3, 102.0, 101.0, 96.0, 94.0,  87.0,  78.0,  72.0],
        "I2 (A)": [0.0,  0.29, 0.40, 0.64, 0.92,  1.18,  1.50,  1.65],
        "P2 (W)": [0.0,  30.0, 42.0, 67.0, 88.0,  104.0, 119.0, 120.0],
    })

    df = st.data_editor(donnees, use_container_width=True)

    # Sécurité : éviter division par zéro dans le rendement
    eta_labo = np.where(
        df["P1 (W)"] > 0,
        (df["P2 (W)"] / df["P1 (W)"]) * 100,
        0.0,
    )

    col_g3, col_g4, col_g5 = st.columns(3)

    # Graphique 3 : Rendement expérimental
    with col_g3:
        st.write("#### Rendement mesuré")
        fig3, ax3 = plt.subplots()
        ax3.plot(df["I2 (A)"], eta_labo, "-o", color="green")
        ax3.set_xlabel("I2 (A)")
        ax3.set_ylabel("Rendement (%)")
        ax3.set_ylim(0, 105)
        ax3.grid(True)
        fig3.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)

    # Graphique 4 : Chute de tension U2
    with col_g4:
        st.write("#### Tension secondaire U2")
        fig4, ax4 = plt.subplots()
        ax4.plot(df["I2 (A)"], df["U2 (V)"], "-o", color="red")
        ax4.set_xlabel("I2 (A)")
        ax4.set_ylabel("U2 (V)")
        ax4.grid(True)
        fig4.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)

    # Graphique 5 : Bilan des pertes (mesuré vs estimé)
    with col_g5:
        st.write("#### Pertes : mesuré vs estimé")
        pertes_mesurees = df["P1 (W)"] - df["P2 (W)"]
        pertes_estimees = (
            P10
            + R1 * df["I1 (A)"] ** 2
            + R2 * df["I2 (A)"] ** 2
        )
        fig5, ax5 = plt.subplots()
        ax5.plot(df["I2 (A)"], pertes_mesurees, "-o",  label="Mesuré")
        ax5.plot(df["I2 (A)"], pertes_estimees, "--s", label="Estimé")
        ax5.set_xlabel("I2 (A)")
        ax5.set_ylabel("Pertes (W)")
        ax5.legend()
        ax5.grid(True)
        fig5.tight_layout()
        st.pyplot(fig5)
        plt.close(fig5)
