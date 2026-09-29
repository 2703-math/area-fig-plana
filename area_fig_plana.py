import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

st.set_page_config(page_title="Área de Figuras Planas", layout="wide")

st.markdown("""
<style>
.main-title { font-size:2rem; font-weight:800; color:#0f172a; text-align:center; }
.subtitle { font-size:1rem; color:#64748b; text-align:center; margin-bottom:2rem; }
.concept-card { background:#f8fafc; border-radius:12px; padding:1.2rem; border-left:4px solid #3b82f6; margin-bottom:1rem; color:#334155; }
.param-box { background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:1rem; margin-bottom:1rem; }
.highlight { color:#ef4444; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

# ===================== UTILIDADES =====================
def build_scanline_fig(width_fn, y_max, x_off=0, color="#3b82f6", frac=1.0):
    """Constrói figura com preenchimento parcial por scanline horizontal."""
    fig = go.Figure()
    ys_full = np.linspace(0, y_max, 300)
    top_x = [width_fn(y)/2 + x_off for y in ys_full]
    bot_x = [-width_fn(y)/2 + x_off for y in ys_full[::-1]]
    border_x = top_x + bot_x
    border_y = list(ys_full) + list(ys_full[::-1])

    # Borda externa (contorno)
    fig.add_trace(go.Scatter(x=border_x, y=border_y, mode="lines",
                                  line=dict(color=color, width=3),
                                  fill="toself", fillcolor=color, opacity=0.0,
                                  name="Figura", hoverinfo="skip"))

    # Preenchimento parcial até frac*y_max
    y_lim = y_max * frac
    n_pts = max(6, int(300 * frac))
    ys = np.linspace(0, y_lim, n_pts)
    tx = [width_fn(y)/2 + x_off for y in ys]
    bx = [-width_fn(y)/2 + x_off for y in ys[::-1]]
    fx = tx + bx[::-1]
    fy = list(ys) + list(ys[::-1])

    fig.add_trace(go.Scatter(x=fx, y=fy, mode="lines",
                                  fill="toself", fillcolor=color, opacity=0.35,
                                  line=dict(color=color, width=2),
                                  hoverinfo="skip"))

    # Linha de varredura
    fig.add_trace(go.Scatter(x=[x_off, x_off], y=[0, y_lim], mode="lines",
                                  line=dict(color="black", width=2, dash="dash"),
                                  name="Varredura"))

    fig.update_layout(height=480, showlegend=False, plot_bgcolor="white",
                      paper_bgcolor="white", margin=dict(l=10,r=10,t=10,b=10),
                      xaxis=dict(range=[-y_max*1.2+x_off, y_max*1.2+x_off], visible=False),
                      yaxis=dict(range=[-0.1, y_max*1.1], visible=False))
    return fig

# ===================== ABAS =====================
st.markdown('<div class="main-title">📐 Área de Figuras Planas — Animação</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Construção animada da área por varredura (integral)</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📎 Retângulo", "🔺 Triângulo", "⭕ Círculo", "🔲 Trapézio",
    "🌀 Setor Circular", "🥚 Elipse", "🔷 Polígono Regular"
])

# --- 1. Retângulo ---
with tab1:
    st.markdown('<div class="concept-card"><b>Retângulo:</b> <span class="highlight">A = b × h</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        b = st.slider("Base (b)", 1.0, 10.0, 5.0, 0.5, key="ret_b")
        h = st.slider("Altura (h)", 1.0, 10.0, 6.0, 0.5, key="ret_h")
        st.markdown(f"**Área total = {b*h:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        frac = st.slider("Nível de preenchimento (%)", 0, 100, 100, 5, key="ret_frac") / 100
        w_fn = lambda y: b
        st.plotly_chart(build_scanline_fig(w_fn, h, N=80, color="#3b82f6", frac=frac),
                        use_container_width=True, config={"displayModeBar": False})

# --- 2. Triângulo ---
with tab2:
    st.markdown('<div class="concept-card"><b>Triângulo:</b> <span class="highlight">A = (b × h) / 2</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        b = st.slider("Base (b)", 1.0, 10.0, 6.0, 0.5, key="tri_b")
        h = st.slider("Altura (h)", 1.0, 10.0, 7.0, 0.5, key="tri_h")
        st.markdown(f"**Área total = {b*h/2:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        frac = st.slider("Nível de preenchimento (%)", 0, 100, 100, 5, key="tri_frac") / 100
        w_fn = lambda y: b * (1 - y/h)
        st.plotly_chart(build_scanline_fig(w_fn, h, color="#ef4444", frac=frac),
                        use_container_width=True, config={"displayModeBar": False})

# --- 3. Círculo ---
with tab3:
    st.markdown('<div class="concept-card"><b>Círculo:</b> <span class="highlight">A = π × r²</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        r = st.slider("Raio (r)", 1.0, 8.0, 5.0, 0.5, key="cir_r")
        st.markdown(f"**Área total = {math.pi*r**2:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        frac = st.slider("Nível de preenchimento (%)", 0, 100, 100, 5, key="cir_frac") / 100
        w_fn = lambda y: 2*math.sqrt(max(0, r**2 - y**2))
        st.plotly_chart(build_scanline_fig(w_fn, r, color="#10b981", frac=frac),
                        use_container_width=True, config={"displayModeBar": False})

# --- 4. Trapézio ---
with tab4:
    st.markdown('<div class="concept-card"><b>Trapézio:</b> <span class="highlight">A = (B + b) × h / 2</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        B = st.slider("Base maior (B)", 1.0, 10.0, 8.0, 0.5, key="trap_B")
        b = st.slider("Base menor (b)", 1.0, 10.0, 4.0, 0.5, key="trap_b")
        h = st.slider("Altura (h)", 1.0, 10.0, 6.0, 0.5, key="trap_h")
        st.markdown(f"**Área total = {(B+b)*h/2:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        frac = st.slider("Nível de preenchimento (%)", 0, 100, 100, 5, key="trap_frac") / 100
        w_fn = lambda y: B + (b - B) * (y/h)
        st.plotly_chart(build_scanline_fig(w_fn, h, color="#f59e0b", frac=frac),
                        use_container_width=True, config={"displayModeBar": False})

# --- 5. Setor circular ---
with tab5:
    st.markdown('<div class="concept-card"><b>Setor Circular:</b> <span class="highlight">A = π × r² × θ / 360</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        r_set = st.slider("Raio (r)", 1.0, 8.0, 5.0, 0.5, key="set_r")
        theta_deg = st.slider("Ângulo (°)", 10, 360, 90, 5, key="set_t")
        A = math.pi * r_set**2 * theta_deg / 360
        st.markdown(f"**Área total = {A:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        frac = st.slider("Nível de preenchimento (%)", 0, 100, 100, 5, key="set_frac") / 100
        theta_rad = math.radians(theta_deg)
        # Setor preenchido até frac do ângulo
        t_full = np.linspace(0, theta_rad, 200)
        bx_full = r_set*np.cos(t_full)
        by_full = r_set*np.sin(t_full)
        border_x = [0] + list(bx_full) + [0]
        border_y = [0] + list(by_full) + [0]

        t_part = np.linspace(0, theta_rad*frac, max(3, int(200*frac)))
        bx_part = r_set*np.cos(t_part)
        by_part = r_set*np.sin(t_part)
        fx = [0] + list(bx_part) + [0]
        fy = [0] + list(by_part) + [0]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=border_x, y=border_y, mode="lines",
                                      fill="toself", fillcolor="#8b5cf6", opacity=0.0,
                                      line=dict(color="#8b5cf6", width=3), hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=fx, y=fy, mode="lines",
                                      fill="toself", fillcolor="#8b5cf6", opacity=0.35,
                                      line=dict(color="#8b5cf6", width=2), hoverinfo="skip"))
        # Linha de varredura angular
        if frac > 0:
            ex, ey = r_set*math.cos(theta_rad*frac), r_set*math.sin(theta_rad*frac)
            fig.add_trace(go.Scatter(x=[0, ex], y=[0, ey], mode="lines",
                                          line=dict(color="black", width=2, dash="dash"),
                                          hoverinfo="skip"))
        fig.update_layout(height=480, showlegend=False, plot_bgcolor="white",
                          paper_bgcolor="white", margin=dict(l=10,r=10,t=10,b=10),
                          xaxis=dict(range=[-r_set*1.2, r_set*1.2], visible=False),
                          yaxis=dict(range=[-r_set*1.2, r_set*1.2], visible=False))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# --- 6. Elipse ---
with tab6:
    st.markdown('<div class="concept-card"><b>Elipse:</b> <span class="highlight">A = π × a × b</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        a_el = st.slider("Semieixo horizontal (a)", 1.0, 8.0, 6.0, 0.5, key="ell_a")
        b_el = st.slider("Semieixo vertical (b)", 1.0, 8.0, 4.0, 0.5, key="ell_b")
        st.markdown(f"**Área total = {math.pi*a_el*b_el:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        frac = st.slider("Nível de preenchimento (%)", 0, 100, 100, 5, key="ell_frac") / 100
        w_fn = lambda y: 2*a_el*math.sqrt(max(0, 1 - (y/b_el)**2))
        st.plotly_chart(build_scanline_fig(w_fn, b_el, color="#ec4899", frac=frac),
                        use_container_width=True, config={"displayModeBar": False})

# --- 7. Polígono regular ---
with tab7:
    st.markdown('<div class="concept-card"><b>Polígono Regular:</b> <span class="highlight">A = (n × l²) / (4 × tan(π/n))</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        n_lados = st.slider("Número de lados", 3, 16, 6, 1, key="pol_n")
        R_pol = st.slider("Raio da circunscrita (R)", 1.0, 8.0, 5.0, 0.5, key="pol_R")
        l_lado = 2*R_pol*math.sin(math.pi/n_lados)
        A_pol = n_lados*l_lado**2/(4*math.tan(math.pi/n_lados))
        st.markdown(f"**Área total = {A_pol:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        frac = st.slider("Nível de preenchimento (%)", 0, 100, 100, 5, key="pol_frac") / 100

        # Vértices do polígono regular
        theta_v = np.linspace(0, 2*math.pi, n_lados, endpoint=False)
        VX = R_pol*np.cos(theta_v)
        VY = R_pol*np.sin(theta_v)

        def width_poly(y):
            pts = []
            for i in range(n_lados):
                x1, y1 = VX[i], VY[i]
                x2, y2 = VX[(i+1)%n_lados], VY[(i+1)%n_lados]
                if y1 == y2: continue
                if min(y1,y2) <= y <= max(y1,y2):
                    t = (y - y1) / (y2 - y1)
                    pts.append(x1 + t*(x2 - x1))
            return (max(pts) - min(pts)) if len(pts) >= 2 else 0.0

        st.plotly_chart(build_scanline_fig(width_poly, R_pol, x_off=0, color="#6366f1", frac=frac),
                        use_container_width=True, config={"displayModeBar": False})

st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#94a3b5; font-size:0.85rem; padding:1rem;">
📐 <b>Área de Figuras Planas</b> — Animação didática via varredura e integral.
</div>""", unsafe_allow_html=True)
