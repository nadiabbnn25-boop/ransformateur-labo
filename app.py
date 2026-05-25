# 1. Les importations
import streamlit as st
import numpy as np  # si vous l'utilisez
import matplotlib.pyplot as plt  # si vous l'utilisez

# 1. Nom de l'université tout en haut (centré et discret)
st.markdown("<p style='text-align: center; color: gray; font-size: 14px; margin-bottom: 0px;'>Université de [BATNA2] - Département d'Électrotechnique</p>", unsafe_allow_html=True)
st.markdown("---")

# 2. Titre de l'application
st.title("Étude et optimisation des pertes et du rendement du transformateur monophasé")

# 3. LE MENU DÉROULANT "À PROPOS"
with st.expander("ℹ️ À propos de ce projet (Crédits)"):
    st.write("Ce simulateur a été développé dans le cadre des travaux pratiques de Licence 3 Électromécanique ou Électrotechnique .")
    
    # Création de deux colonnes à l'intérieur du menu pour une présentation propre
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎓 Réalisé par :**")
        st.markdown("""
        -  M.A.A BACHA                      
        -  Y. BAASSOU              
        - A. BENAMMAR 
        """)
        
    with col2:
        st.markdown("**👨‍🏫 Encadré par :**")
        st.markdown("- Dr. [N. Benbouza]")
        
    st.markdown("**📅 Année universitaire :** 2025/2026")

# 4. Suite du code de votre application (vos calculs et graphiques)
# st.subheader("Saisie des données expérimentales")
# ...

# 4. Le reste de votre code (vos graphiques, calculs de bêta, etc.)


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
onglets = st.tabs([
    "⚡ Mode Industriel (Théorie)",
    "🔬 Mode Laboratoire (Expérimental)"
])

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

    # ══════════════════════════════════════
    # ÉTAPE 1 : ENTRÉES UTILISATEUR
    # ══════════════════════════════════════
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)

    Sn_val      = col_p1.number_input("Puissance Nominale Sn (VA)",
                                       value=100000, step=10000, key="Sn")
    P0_val      = col_p2.number_input("Pertes Fer P0 (W)",
                                       value=500, step=50, key="P0")
    Pcc_val     = col_p3.number_input("Pertes Joule Pcc (W)",
                                       value=1500, step=100, key="Pcc")
    cosphi_val  = col_p4.slider("Facteur de puissance (cos φ)",
                                 0.5, 1.0, 0.8, key="cosphi")

    # ══════════════════════════════════════
    # ÉTAPE 2 : CALCULS (après les entrées)
    # ══════════════════════════════════════
    beta     = np.arange(0, 1.55, 0.05)
    beta_opt = float(np.sqrt(P0_val / Pcc_val)) if Pcc_val > 0 else 0.0

    # Pertes (recalculées avec les valeurs actuelles)
    Pfer_calc  = np.full_like(beta, float(P0_val))
    Pj_calc    = (beta ** 2) * float(Pcc_val)
    Ptot_calc  = Pfer_calc + Pj_calc

    # Rendement (recalculé avec les valeurs actuelles)
    P2_calc    = beta * float(Sn_val) * float(cosphi_val)
    eta_calc   = 100 * P2_calc / (P2_calc + float(P0_val) + Pj_calc + 1e-9)

    # Rendement au point optimal
    eta_opt = (
        100 * (beta_opt * float(Sn_val) * float(cosphi_val))
        / (beta_opt * float(Sn_val) * float(cosphi_val) + 2 * float(P0_val) + 1e-9)
    )

    st.success(
        f"Rendement maximal théorique : **β optimal = {beta_opt:.3f}** "
        f"| η max ≈ **{eta_opt:.1f} %** pour cos(φ) = {cosphi_val:.2f}"
    )

    # ══════════════════════════════════════
    # ÉTAPE 3 : GRAPHIQUES LIGNE 1
    # ══════════════════════════════════════
    col_g1, col_g2 = st.columns(2)

    # ── Graphique 1 : Bilan des pertes ──
    with col_g1:
        st.write("#### Bilan des Pertes")

        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.plot(beta, Pfer_calc,  'r--', linewidth=2,
                 label=f'Pertes fer = {P0_val} W')
        ax1.plot(beta, Pj_calc,    'b-.', linewidth=2,
                 label='Pertes Joule')
        ax1.plot(beta, Ptot_calc,  'k',   linewidth=2.5,
                 label='Pertes Totales')
        ax1.axvline(x=beta_opt, color='gray', linestyle=':',
                    linewidth=1, label=f'β opt = {beta_opt:.3f}')
        ax1.set_xlabel('Taux de charge (β)')
        ax1.set_ylabel('Pertes (W)')
        ax1.legend(fontsize='small')
        ax1.grid(True, alpha=0.6)
        fig1.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

    # ── Graphique 2 : Rendement + Zoom ──
    with col_g2:
        st.write("#### Rendement pour différents cos(φ)")

        fig2, (ax2, ax_zoom) = plt.subplots(
            2, 1, figsize=(6, 7),
            gridspec_kw={"hspace": 0.45}
        )

        # Ensemble des cos(φ) à tracer
        cos_set = sorted({0.7, round(float(cosphi_val), 2), 1.0})

        for c in cos_set:
            P_utile = float(Sn_val) * beta * c
            eta_c   = 100 * P_utile / (
                P_utile + float(P0_val) + float(Pcc_val) * beta**2 + 1e-9
            )

            # Style selon si c'est la courbe active ou non
            if abs(c - cosphi_val) < 0.001:
                kw = dict(color="navy", linewidth=2.5,
                          linestyle="-", label=f"cos(φ)={c:.2f} ◄ Actuel")
            elif c < cosphi_val:
                kw = dict(color="red", linewidth=1.2,
                          linestyle="--", label=f"cos(φ)={c:.2f}")
            else:
                kw = dict(color="green", linewidth=1.2,
                          linestyle=":", label=f"cos(φ)={c:.2f}")

            ax2.plot(beta, eta_c, **kw)
            ax_zoom.plot(beta, eta_c, **kw)

        # Mise en forme des deux axes
        for ax, ylim, titre in [
            (ax2,    (0,  105), "Vue globale"),
            (ax_zoom,(60, 105), "Zoom (60 – 105 %)"),
        ]:
            ax.axvline(x=beta_opt, color='k', linestyle='--',
                       linewidth=0.9, label='β optimal')
            ax.set_xlabel('Taux de charge (β)')
            ax.set_ylabel('Rendement (%)')
            ax.set_ylim(*ylim)
            ax.set_title(titre)
            ax.legend(fontsize='x-small')
            ax.grid(True, alpha=0.6)

        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    # ══════════════════════════════════════
    # ÉTAPE 4 : ANALYSE + COURBE SENSIBILITÉ
    # ══════════════════════════════════════
    st.write("---")
    col_gauche, col_droite = st.columns(2)

    # ── Analyse textuelle ──
    with col_gauche:
        st.subheader("Analyse de l'optimisation")
        st.write(f"""
        Le point optimal est atteint pour **β = {beta_opt:.3f}**.  
        À ce point :
        * Les **pertes fer** (fixes = {P0_val} W) = **pertes Joule** (variables).
        * Le rendement maximal estimé est **η ≈ {eta_opt:.1f} %**
          pour cos(φ) = {cosphi_val:.2f}.
        * Un **cos(φ) élevé** améliore le rendement à charge égale.
        * Chargez le transformateur près de **β_opt** pour minimiser
          les pertes totales.
        """)

        st.info(
            "💡 Le transformateur est optimisé quand il fonctionne "
            "proche de son point de rendement maximal."
        )

        # Tableau récapitulatif
        st.write("##### Récapitulatif au point optimal")
        recap = pd.DataFrame({
            "Grandeur": [
                "β optimal",
                "Pertes fer (W)",
                "Pertes Joule au point opt (W)",
                "Pertes totales au point opt (W)",
                "η max (%)"
            ],
            "Valeur": [
                f"{beta_opt:.3f}",
                f"{P0_val:.0f}",
                f"{(beta_opt**2) * Pcc_val:.0f}",
                f"{P0_val + (beta_opt**2) * Pcc_val:.0f}",
                f"{eta_opt:.1f}",
            ],
        })
        st.dataframe(recap, use_container_width=True, hide_index=True)

    # ── Courbe sensibilité η = f(cos φ) ──
    with col_droite:
        st.subheader("Sensibilité du rendement au cos(φ)")

        cos_range    = np.linspace(0.5, 1.0, 200)
        P_utile_opt  = beta_opt * float(Sn_val) * cos_range
        eta_vs_cos   = (
            100 * P_utile_opt
            / (P_utile_opt + 2 * float(P0_val) + 1e-9)
        )

        # Valeur du point actuel
        eta_point = (
            100 * (beta_opt * float(Sn_val) * float(cosphi_val))
            / (beta_opt * float(Sn_val) * float(cosphi_val) + 2 * float(P0_val) + 1e-9)
        )

        fig3, ax3 = plt.subplots(figsize=(6, 4))
        ax3.plot(cos_range, eta_vs_cos, color='navy', linewidth=2,
                 label='η max = f(cos φ)')
        ax3.axvline(x=cosphi_val, color='red', linestyle='--',
                    linewidth=1.5, label=f'cos(φ) = {cosphi_val:.2f}')
        ax3.scatter([cosphi_val], [eta_point],
                    color='red', s=80, zorder=5,
                    label=f'η = {eta_point:.1f} %')
        ax3.set_xlabel('cos(φ)')
        ax3.set_ylabel('Rendement maximal (%)')
        ax3.set_title(f'Rendement à β = {beta_opt:.3f} selon cos(φ)')
        ax3.legend(fontsize='small')
        ax3.grid(True, alpha=0.6)
        fig3.tight_layout()
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

    # ── Graphique L1 : Rendement mesuré ──
    with col_l1:
        st.write("#### Rendement mesuré")
        fig_l1, ax_l1 = plt.subplots(figsize=(5, 4))
        ax_l1.plot(df["I2 (A)"], eta_labo, "-o", color="green", linewidth=2)
        ax_l1.set_xlabel("I2 (A)")
        ax_l1.set_ylabel("Rendement (%)")
        ax_l1.set_ylim(0, 105)
        ax_l1.grid(True, alpha=0.6)
        fig_l1.tight_layout()
        st.pyplot(fig_l1)
        plt.close(fig_l1)

    # ── Graphique L2 : Tension secondaire ──
    with col_l2:
        st.write("#### Tension secondaire U2")
        fig_l2, ax_l2 = plt.subplots(figsize=(5, 4))
        ax_l2.plot(df["I2 (A)"], df["U2 (V)"], "-o", color="red", linewidth=2)
        ax_l2.set_xlabel("I2 (A)")
        ax_l2.set_ylabel("U2 (V)")
        ax_l2.grid(True, alpha=0.6)
        fig_l2.tight_layout()
        st.pyplot(fig_l2)
        plt.close(fig_l2)

    # ── Graphique L3 : Pertes mesuré vs estimé ──
    with col_l3:
        st.write("#### Pertes : mesuré vs estimé")
        pertes_mesurees = df["P1 (W)"] - df["P2 (W)"]
        pertes_estimees = (
            P10
            + R1 * df["I1 (A)"] ** 2
            + R2 * df["I2 (A)"] ** 2
        )
        fig_l3, ax_l3 = plt.subplots(figsize=(5, 4))
        ax_l3.plot(df["I2 (A)"], pertes_mesurees, "-o",
                   linewidth=2, label="Mesuré")
        ax_l3.plot(df["I2 (A)"], pertes_estimees, "--s",
                   linewidth=2, label="Estimé")
        ax_l3.set_xlabel("I2 (A)")
        ax_l3.set_ylabel("Pertes (W)")
        ax_l3.legend()
        ax_l3.grid(True, alpha=0.6)
        fig_l3.tight_layout()
        st.pyplot(fig_l3)
        plt.close(fig_l3)
