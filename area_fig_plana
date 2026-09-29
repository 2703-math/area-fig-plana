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
def trapz(width_fn, a, b, n=500):
    """Integração numérica pela regra do trapézio."""
    if b <= a: return 0.0
    xs = np.linspace(a, b, n)
    ys = np.array([width_fn(x) for x in xs])
    h = (b - a) / (n - 1)
    return h * (0.5*ys[0] + 0.5*ys[-1] + np.sum(ys[1:-1]))

def build_area_anim(width_fn, y_max, x_off=0, N=80, color="#3b82f6", label="y"):
    """Constrói figura com animação de preenchimento por scanline horizontal."""
    fig = go.Figure()
    # Borda fixa
    ys_full = np.linspace(0, y_max, 250)
    top_x = [width_fn(y)/2 + x_off for y in ys_full]
    bot_x = [-width_fn(y)/2 + x_off for y in ys_full[::-1]]
    border_x = top_x + bot_x
    border_y = list(ys_full) + list(ys_full[::-1])
    fig.add_trace(go.Scatter(x=border_x, y=border_y, mode="lines",
                             line=dict(color=color, width=3),
                             fill="toself", fillcolor=color, opacity=0.0,
                             name="Figura", hoverinfo="skip"))

    frames = []
    for i in range(N + 1):
        t = i / N
        y_lim = y_max * t
        n_pts = max(6, int(250 * t))
        ys = np.linspace(0, y_lim, n_pts)
        tx = [width_fn(y)/2 + x_off for y in ys]
        bx = [-width_fn(y)/2 + x_off for y in ys[::-1]]
        fx = tx + bx[::-1]
        fy = list(ys) + list(ys[::-1])
        area_parcial = trapz(width_fn, 0, y_lim)
        area_total = trapz(width_fn, 0, y_max)
        frames.append(go.Frame(
            data=[
                go.Scatter(x=border_x, y=border_y, mode="lines",
                           line=dict(color=color, width=3),
                           fill="toself", fillcolor=color, opacity=0.0,
                           hoverinfo="skip"),
                go.Scatter(x=fx, y=fy, mode="lines",
                           fill="toself", fillcolor=color, opacity=0.35,
                           line=dict(color=color, width=2),
                           text=f"Área parcial: {area_parcial:.3f}<br>Total: {area_total:.3f}",
                           hoverinfo="text"),
                go.Scatter(x=[x_off, x_off], y=[0, y_lim], mode="lines",
                           line=dict(color="black", width=2, dash="dash"),
                           name="Varredura")
            ],
            traces=[0, 1, 2]
        ))
    fig.frames = frames
    fig.update_layout(
        height=480, showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=50, b=10),
        updatemenus=[{
            "type": "buttons", "showactive": False, "x": 0.0, "y": 1.15,
            "buttons": [
                {"label": "▶ Animar", "method": "animate",
                 "args": [None, {"frame": {"duration": 60, "redraw": True}, "fromcurrent": True}]},
                {"label": "❚❚ Pausar", "method": "animate",
                 "args": [[None], {"frame": {"duration": 0, "redraw": False}}]}
            ]
        }]
    )
    fig.update_xaxes(range=[-y_max*1.2 + x_off, y_max*1.2 + x_off], visible=False)
    fig.update_yaxes(range=[-0.1, y_max*1.1], visible=False)
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
        b = st.slider("Base (b)", 1.0, 10.0, 5.0, 0.5)
        h = st.slider("Altura (h)", 1.0, 10.0, 6.0, 0.5)
        st.markdown(f"**Área = {b*h:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        w_fn = lambda y: b
        st.plotly_chart(build_area_anim(w_fn, h, N=80, color="#3b82f6"),
                        use_container_width=True, config={"displayModeBar": False})

# --- 2. Triângulo ---
with tab2:
    st.markdown('<div class="concept-card"><b>Triângulo:</b> <span class="highlight">A = (b × h) / 2</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        b = st.slider("Base (b)", 1.0, 10.0, 6.0, 0.5)
        h = st.slider("Altura (h)", 1.0, 10.0, 7.0, 0.5)
        st.markdown(f"**Área = {b*h/2:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        w_fn = lambda y: b * (1 - y/h)
        st.plotly_chart(build_area_anim(w_fn, h, N=80, color="#ef4444"),
                        use_container_width=True, config={"displayModeBar": False})

# --- 3. Círculo ---
with tab3:
    st.markdown('<div class="concept-card"><b>Círculo:</b> <span class="highlight">A = π × r²</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        r = st.slider("Raio (r)", 1.0, 8.0, 5.0, 0.5)
        st.markdown(f"**Área = {math.pi*r**2:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        w_fn = lambda y: 2*math.sqrt(max(0, r**2 - y**2))
        st.plotly_chart(build_area_anim(w_fn, r, N=80, color="#10b981"),
                        use_container_width=True, config={"displayModeBar": False})

# --- 4. Trapézio ---
with tab4:
    st.markdown('<div class="concept-card"><b>Trapézio:</b> <span class="highlight">A = (B + b) × h / 2</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        B = st.slider("Base maior (B)", 1.0, 10.0, 8.0, 0.5)
        b = st.slider("Base menor (b)", 1.0, 10.0, 4.0, 0.5)
        h = st.slider("Altura (h)", 1.0, 10.0, 6.0, 0.5)
        st.markdown(f"**Área = {(B+b)*h/2:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        w_fn = lambda y: B + (b - B) * (y/h)
        st.plotly_chart(build_area_anim(w_fn, h, N=80, color="#f59e0b"),
                        use_container_width=True, config={"displayModeBar": False})

# --- 5. Setor circular ---
with tab5:
    st.markdown('<div class="concept-card"><b>Setor Circular:</b> <span class="highlight">A = π × r² × θ / 360</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        r = st.slider("Raio (r)", 1.0, 8.0, 5.0, 0.5, key="set_r")
        theta = st.slider("Ângulo (°)", 10, 360, 90, 5, key="set_t")
        A = math.pi * r**2 * theta / 360
        st.markdown(f"**Área = {A:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        ang = math.radians(theta)
        w_fn = lambda y: 2*math.sqrt(max(0, r**2 - y**2)) if y <= r*math.sin(ang) else 0
        # Abordagem mais limpa: setor como arco + raios
        def build_setor(r, theta_deg, N=80):
            fig = go.Figure()
            theta_rad = math.radians(theta_deg)
            # Borda
            t = np.linspace(0, theta_rad, 200)
            bx = r*np.cos(t); by = r*np.sin(t)
            border_x = [0] + list(bx) + [0]
            border_y = [0] + list(by) + [0]
            fig.add_trace(go.Scatter(x=border_x, y=border_y, mode="lines",
                                     fill="toself", fillcolor="#8b5cf6", opacity=0.0,
                                     line=dict(color="#8b5cf6", width=3), hoverinfo="skip"))
            frames=[]
            for i in range(N+1):
                frac = i/N
                t_f = np.linspace(0, theta_rad*frac, max(3, int(200*frac)))
                bx_f = r*np.cos(t_f); by_f = r*np.sin(t_f)
                fx = [0] + list(bx_f) + [0]
                fy = [0] + list(by_f) + [0]
                area_parcial = r**2 * theta_rad * frac / 2
                area_total = math.pi*r**2*theta_deg/360
                frames.append(go.Frame(
                    data=[
                        go.Scatter(x=border_x, y=border_y, mode="lines",
                                   fill="toself", fillcolor="#8b5cf6", opacity=0.0,
                                   line=dict(color="#8b5cf6", width=3), hoverinfo="skip"),
                        go.Scatter(x=fx, y=fy, mode="lines", fill="toself",
                                   fillcolor="#8b5cf6", opacity=0.35,
                                   line=dict(color="#8b5cf6", width=2),
                                   text=f"Área parcial: {area_parcial:.3f}<br>Total: {area_total:.3f}",
                                   hoverinfo="text")
                    ], traces=[0,1]
                ))
            fig.frames = frames
            fig.update_layout(height=480, showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
                              margin=dict(l=10,r=10,t=50,b=10),
                              updatemenus=[{
                                  "type":"buttons","showactive":False,"x":0.0,"y":1.15,
                                  "buttons":[
                                      {"label":"▶ Animar","method":"animate",
                                       "args":[None, {"frame":{"duration":60,"redraw":True},"fromcurrent":True}]},
                                      {"label":"❚❚ Pausar","method":"animate",
                                       "args":[[None],{"frame":{"duration":0,"redraw":False}}]}
                                  ]
                              }],
                              xaxis=dict(range=[-r*1.2, r*1.2], visible=False),
                              yaxis=dict(range=[-r*1.2, r*1.2], visible=False))
            return fig
        st.plotly_chart(build_setor(r, theta), use_container_width=True, config={"displayModeBar": False})

# --- 6. Elipse ---
with tab6:
    st.markdown('<div class="concept-card"><b>Elipse:</b> <span class="highlight">A = π × a × b</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        a = st.slider("Semieixo horizontal (a)", 1.0, 8.0, 6.0, 0.5)
        b = st.slider("Semieixo vertical (b)", 1.0, 8.0, 4.0, 0.5)
        st.markdown(f"**Área = {math.pi*a*b:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        w_fn = lambda y: 2*a*math.sqrt(max(0, 1 - (y/b)**2))
        st.plotly_chart(build_area_anim(w_fn, b, N=80, color="#ec4899"),
                        use_container_width=True, config={"displayModeBar": False})

# --- 7. Polígono regular ---
with tab7:
    st.markdown('<div class="concept-card"><b>Polígono Regular:</b> <span class="highlight">A = (n × l²) / (4 × tan(π/n))</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="param-box">', unsafe_allow_html=True)
        n = st.slider("Número de lados", 3, 16, 6, 1)
        R = st.slider("Raio da circunferência circunscrita (R)", 1.0, 8.0, 5.0, 0.5)
        l = 2*R*math.sin(math.pi/n)
        A = n*l**2/(4*math.tan(math.pi/n))
        st.markdown(f"**Área = {A:.2f} u²**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        ys_poly = np.linspace(-R, R, 300)
        # Largura do polígono em cada y (aproximação por raio da seção)
        # Para polígono regular centrado, a largura em y é 2*R*cos(asin(y/R)) limitado pelas arestas.
        # Aproximação didática: círculo inscrito + correção (simplificação).
        # Versão precisa: construir vértices e interseção com scanline.
        theta = np.linspace(0, 2*math.pi, n, endpoint=False)
        VX = R*np.cos(theta); VY = R*np.sin(theta)
        def width_poly(y):
            pts = []
            for i in range(n):
                x1,y1 = VX[i], VY[i]; x2,y2 = VX[(i+1)%n], VY[(i+1)%n]
                if (y1-y)*(y2-y) < 0 or y1==y or y2==y:
                    if y2-y1 != 0:
                        t = (y-y1)/(y2-y1)
                        if 0 <= t <= 1:
                            pts.append(x1 + t*(x2-x1))
            if not pts: return 0.0
            return 2*(max(pts)-min(pts))/2 + (max(pts)-min(pts))
        # Reimplementar de forma correta:
        def width_poly(y):
            pts = []
            for i in range(n):
                x1,y1 = VX[i], VY[i]; x2,y2 = VX[(i+1)%n], VY[(i+1)%n]
                if y1 == y2: continue
                if min(y1,y2) <= y <= max(y1,y2):
                    t = (y-y1)/(y2-y1)
                    pts.append(x1 + t*(x2-x1))
            return (max(pts)-min(pts)) if len(pts)>=2 else 0.0
        st.plotly_chart(build_area_anim(width_poly, R, x_off=0, N=80, color="#6366f1"),
                        use_container_width=True, config={"displayModeBar": False})

st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#94a3b8; font-size:0.85rem; padding:1rem;">
📐 <b>Área de Figuras Planas</b> — Animação didática via varredura e integral.
</div>""", unsafe_allow_html=True)
