import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌷 Tulip Price Odyssey",
    page_icon="🌷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── DATA ────────────────────────────────────────────────────────────────────────
years = list(range(2015, 2026))

data = {
    "year": years,
    "usa_low":  [10, 10, 12, 12, 15, 15, 20, 25, 25, 30, 30],
    "usa_high": [15, 15, 18, 18, 20, 25, 30, 35, 40, 45, 50],
    "arg_ars_low":  [80, 120, 200, 350, 700, 1000, 2000, 5000,  15000, 40000, 60000],
    "arg_ars_high": [120, 200, 300, 500, 900, 1500, 2800, 7000,  30000, 70000, 100000],
    "usd_ars":  [9.5, 14.5, 17.5, 39, 61, 83, 101, 260, 575, 925, 1260],
    "arg_usd_low":  [10, 9, 9, 9, 9, 10, 10, 13, 13, 13, 13],
    "arg_usd_high": [12, 12, 12, 12, 12, 13, 13, 15, 16, 15, 15],
}

df = pd.DataFrame(data)
df["usa_mid"]     = (df["usa_low"] + df["usa_high"]) / 2
df["arg_ars_mid"] = (df["arg_ars_low"] + df["arg_ars_high"]) / 2
df["arg_usd_mid"] = (df["arg_usd_low"] + df["arg_usd_high"]) / 2

# ─── KEY EVENTS ─────────────────────────────────────────────────────────────────
events = [
    {"year": 2018, "label": "Argentina IMF Crisis\nPeso -50%", "color": "#ff4444"},
    {"year": 2020, "label": "COVID-19\nPandemic", "color": "#ff8800"},
    {"year": 2022, "label": "Hyperinflation\nAccelerates", "color": "#ffcc00"},
    {"year": 2023, "label": "Milei Elected\nDevaluation Shock", "color": "#ff44aa"},
]

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

  :root {
    --gold:    #f5c842;
    --pink:    #ff6eb4;
    --teal:    #00e5cc;
    --dark:    #0a0a12;
    --card:    #12121e;
    --border:  #2a2a3e;
    --text:    #e8e8f0;
    --muted:   #7878a0;
  }

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: var(--dark);
    color: var(--text);
  }

  .stApp {
    background: 
      radial-gradient(ellipse 80% 50% at 20% -10%, rgba(245,200,66,0.08) 0%, transparent 60%),
      radial-gradient(ellipse 60% 40% at 80% 110%, rgba(0,229,204,0.06) 0%, transparent 60%),
      var(--dark);
    min-height: 100vh;
  }

  /* Hero */
  .hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
  }
  .hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.35em;
    color: var(--teal);
    text-transform: uppercase;
    margin-bottom: 0.75rem;
  }
  .hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.5rem, 8vw, 7rem);
    letter-spacing: 0.05em;
    line-height: 0.95;
    background: linear-gradient(135deg, var(--gold) 0%, var(--pink) 50%, var(--teal) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
  }
  .hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    max-width: 600px;
    margin: 1.2rem auto 0;
    line-height: 1.7;
    font-weight: 300;
  }

  /* Stat cards */
  .stats-row {
    display: flex;
    gap: 1rem;
    margin: 2rem 0;
    flex-wrap: wrap;
  }
  .stat-card {
    flex: 1;
    min-width: 180px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
  }
  .stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
  }
  .stat-card.gold::before  { background: linear-gradient(90deg, var(--gold), transparent); }
  .stat-card.pink::before  { background: linear-gradient(90deg, var(--pink), transparent); }
  .stat-card.teal::before  { background: linear-gradient(90deg, var(--teal), transparent); }
  .stat-card.red::before   { background: linear-gradient(90deg, #ff4444, transparent); }

  .stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }
  .stat-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    line-height: 1;
    margin-bottom: 0.25rem;
  }
  .stat-card.gold .stat-value { color: var(--gold); }
  .stat-card.pink .stat-value { color: var(--pink); }
  .stat-card.teal .stat-value { color: var(--teal); }
  .stat-card.red  .stat-value { color: #ff4444; }
  .stat-delta {
    font-size: 0.78rem;
    color: var(--muted);
  }

  /* Section headers */
  .section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2.5rem 0 1rem;
  }
  .section-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.15em;
  }
  .section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 0.06em;
    color: var(--text);
    margin: 0;
  }
  .section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
  }

  /* Insight boxes */
  .insight-box {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    line-height: 1.7;
    color: var(--muted);
  }
  .insight-box strong { color: var(--text); }
  .insight-box.pink  { border-left-color: var(--pink); }
  .insight-box.teal  { border-left-color: var(--teal); }
  .insight-box.red   { border-left-color: #ff4444; }

  /* Timeline */
  .timeline {
    position: relative;
    padding: 1rem 0;
  }
  .timeline-item {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
    align-items: flex-start;
  }
  .timeline-dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    margin-top: 0.3rem;
    flex-shrink: 0;
    box-shadow: 0 0 8px currentColor;
  }
  .timeline-year {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    color: var(--gold);
    min-width: 45px;
  }
  .timeline-content {
    font-size: 0.88rem;
    color: var(--muted);
    line-height: 1.6;
  }
  .timeline-content strong { color: var(--text); }

  /* Footer */
  .footer {
    text-align: center;
    padding: 3rem 1rem 2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: var(--muted);
    border-top: 1px solid var(--border);
    margin-top: 3rem;
  }

  /* Plotly chart containers */
  .chart-container {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 0.5rem;
    margin-bottom: 1.5rem;
  }

  /* Hide Streamlit default elements */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem; max-width: 1400px; }
  div[data-testid="stHorizontalBlock"] { gap: 1rem; }
</style>
""", unsafe_allow_html=True)

# ─── PLOTLY THEME ────────────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#7878a0", size=11),
    xaxis=dict(gridcolor="#1e1e2e", linecolor="#2a2a3e", tickcolor="#2a2a3e", zeroline=False),
    yaxis=dict(gridcolor="#1e1e2e", linecolor="#2a2a3e", tickcolor="#2a2a3e", zeroline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#2a2a3e", borderwidth=1),
    margin=dict(l=15, r=15, t=40, b=15),
    hoverlabel=dict(bgcolor="#1a1a2e", bordercolor="#2a2a3e", font_color="#e8e8f0"),
)

GOLD  = "#f5c842"
PINK  = "#ff6eb4"
TEAL  = "#00e5cc"
RED   = "#ff4444"

def add_event_lines(fig, yref="y", y_pos=None, y_frac=0.95):
    for ev in events:
        fig.add_vline(
            x=ev["year"], line_dash="dot", line_color=ev["color"], line_width=1, opacity=0.5
        )
        fig.add_annotation(
            x=ev["year"], y=y_frac, yref="paper",
            text=ev["label"].replace("\n", "<br>"),
            showarrow=False,
            font=dict(size=9, color=ev["color"]),
            align="center",
            xanchor="center",
            bgcolor="rgba(10,10,18,0.7)",
            bordercolor=ev["color"],
            borderwidth=1,
            borderpad=3,
        )

# ─── HERO ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">🌷 Data Analytics Dashboard · 2015 – 2025</div>
  <h1 class="hero-title">The Tulip<br>Price Odyssey</h1>
  <p class="hero-sub">
    A decade of bouquet prices in the <strong style="color:#e8e8f0">United States</strong> and 
    <strong style="color:#e8e8f0">Argentina</strong> — a story of mild inflation, 
    hyperinflation, currency collapse, and economic shock.
  </p>
</div>
""", unsafe_allow_html=True)

# ─── KPI CARDS ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
  <div class="stat-card gold">
    <div class="stat-label">USA Price Growth</div>
    <div class="stat-value">+233%</div>
    <div class="stat-delta">$10–15 → $30–50 USD</div>
  </div>
  <div class="stat-card pink">
    <div class="stat-label">Argentina ARS Growth</div>
    <div class="stat-value">×1000</div>
    <div class="stat-delta">$80 → $100,000 ARS</div>
  </div>
  <div class="stat-card teal">
    <div class="stat-label">Argentina USD (stable)</div>
    <div class="stat-value">~$13</div>
    <div class="stat-delta">Remarkably stable in dollars</div>
  </div>
  <div class="stat-card red">
    <div class="stat-label">Peso Devaluation</div>
    <div class="stat-value">×132</div>
    <div class="stat-delta">9.5 → 1,260 ARS per USD</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── CHART 1: USA vs ARG in USD ──────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <span class="section-num">01 ——</span>
  <h2 class="section-title">Bouquet Price in USD: Two Countries, One Decade</h2>
  <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

fig1 = go.Figure()

# USA band
fig1.add_trace(go.Scatter(
    x=years + years[::-1],
    y=list(df["usa_high"]) + list(df["usa_low"])[::-1],
    fill="toself", fillcolor="rgba(245,200,66,0.08)",
    line=dict(color="rgba(0,0,0,0)"), showlegend=False, hoverinfo="skip"
))
fig1.add_trace(go.Scatter(
    x=years, y=df["usa_mid"],
    mode="lines+markers",
    name="🇺🇸 USA",
    line=dict(color=GOLD, width=3),
    marker=dict(size=8, color=GOLD, line=dict(color="#0a0a12", width=2)),
    hovertemplate="<b>USA %{x}</b><br>~$%{y:.0f} USD<extra></extra>"
))

# ARG band
fig1.add_trace(go.Scatter(
    x=years + years[::-1],
    y=list(df["arg_usd_high"]) + list(df["arg_usd_low"])[::-1],
    fill="toself", fillcolor="rgba(0,229,204,0.08)",
    line=dict(color="rgba(0,0,0,0)"), showlegend=False, hoverinfo="skip"
))
fig1.add_trace(go.Scatter(
    x=years, y=df["arg_usd_mid"],
    mode="lines+markers",
    name="🇦🇷 Argentina (USD equiv.)",
    line=dict(color=TEAL, width=3),
    marker=dict(size=8, color=TEAL, line=dict(color="#0a0a12", width=2)),
    hovertemplate="<b>Argentina %{x}</b><br>~$%{y:.0f} USD equiv.<extra></extra>"
))

add_event_lines(fig1)
fig1.update_layout(**CHART_LAYOUT, title=dict(
    text="Tulip Bouquet Price (USD) — USA vs. Argentina",
    font=dict(family="Bebas Neue", size=18, color="#e8e8f0"), x=0.01
), yaxis_title="Price (USD)", height=380)
fig1.update_xaxes(tickmode="linear", dtick=1)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig1, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box teal">
  <strong>Key Insight:</strong> Despite Argentina's economy going through multiple crises, the 
  <strong>dollar-equivalent price of a bouquet stayed remarkably anchored between $10–16 USD</strong> 
  throughout the entire decade. This is the "dollarization effect" — in high-inflation economies, 
  prices in hard currency stay stable while nominal local-currency prices explode.
</div>
""", unsafe_allow_html=True)

# ─── CHART 2: ARS Price Log Scale ──────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <span class="section-num">02 ——</span>
  <h2 class="section-title">Argentina in Pesos: The Hyperinflation Curve</h2>
  <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    scale = st.radio("Y-Axis Scale", ["Logarithmic (recommended)", "Linear"], horizontal=True)
    log_y = "log" in scale

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=years + years[::-1],
        y=list(df["arg_ars_high"]) + list(df["arg_ars_low"])[::-1],
        fill="toself", fillcolor="rgba(255,110,180,0.08)",
        line=dict(color="rgba(0,0,0,0)"), showlegend=False, hoverinfo="skip"
    ))
    fig2.add_trace(go.Scatter(
        x=years, y=df["arg_ars_mid"],
        mode="lines+markers",
        name="🇦🇷 Argentina ARS",
        line=dict(color=PINK, width=3),
        marker=dict(size=9, color=PINK, line=dict(color="#0a0a12", width=2)),
        fill="tonexty", fillcolor="rgba(255,110,180,0.05)",
        hovertemplate="<b>Argentina %{x}</b><br>~$%{y:,.0f} ARS<extra></extra>"
    ))

    add_event_lines(fig2)
    fig2.update_layout(**CHART_LAYOUT, title=dict(
        text="Argentina Tulip Price in Pesos (ARS)",
        font=dict(family="Bebas Neue", size=18, color="#e8e8f0"), x=0.01
    ), yaxis_title="Price (ARS)", yaxis_type="log" if log_y else "linear", height=400)
    fig2.update_xaxes(tickmode="linear", dtick=1)

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="padding-top: 2.5rem;">
      <div class="insight-box pink" style="margin-top:0">
        <strong>2015</strong><br>~$100 ARS
      </div>
      <div class="insight-box pink">
        <strong>2018</strong><br>~$425 ARS<br><span style="font-size:0.8rem">IMF Crisis hits</span>
      </div>
      <div class="insight-box pink">
        <strong>2021</strong><br>~$2,400 ARS<br><span style="font-size:0.8rem">24× vs 2015</span>
      </div>
      <div class="insight-box pink">
        <strong>2023</strong><br>~$22,500 ARS<br><span style="font-size:0.8rem">Milei shock</span>
      </div>
      <div class="insight-box pink">
        <strong>2025</strong><br>~$80,000 ARS<br><span style="font-size:0.8rem">800× vs 2015</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─── CHART 3: Exchange Rate ──────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <span class="section-num">03 ——</span>
  <h2 class="section-title">The Peso Collapse: USD → ARS Exchange Rate</h2>
  <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

fig3 = go.Figure()

fig3.add_trace(go.Bar(
    x=years, y=df["usd_ars"],
    name="ARS per 1 USD",
    marker=dict(
        color=df["usd_ars"],
        colorscale=[[0, "#1a2a1a"], [0.3, GOLD], [0.7, PINK], [1.0, RED]],
        line=dict(color="rgba(0,0,0,0)", width=0)
    ),
    hovertemplate="<b>%{x}</b><br>1 USD = %{y:,.1f} ARS<extra></extra>"
))

for ev in events:
    fig3.add_vline(x=ev["year"], line_dash="dot", line_color=ev["color"], line_width=1, opacity=0.5)
    rate_at_event = df[df["year"] == ev["year"]]["usd_ars"].values[0]
    fig3.add_annotation(
        x=ev["year"], y=rate_at_event + 30,
        text=ev["label"].replace("\n", "<br>"),
        showarrow=True,
        arrowhead=2,
        arrowcolor=ev["color"],
        arrowsize=0.8,
        font=dict(size=9, color=ev["color"]),
        bgcolor="rgba(10,10,18,0.85)",
        bordercolor=ev["color"],
        borderwidth=1,
        borderpad=3,
    )

fig3.update_layout(**CHART_LAYOUT, title=dict(
    text="Official USD → ARS Exchange Rate (year-end approximate)",
    font=dict(family="Bebas Neue", size=18, color="#e8e8f0"), x=0.01
), yaxis_title="ARS per 1 USD", height=380, bargap=0.25)
fig3.update_xaxes(tickmode="linear", dtick=1)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box red">
  <strong>The December 2023 Shock:</strong> When President Milei took office, his government 
  immediately devalued the peso from ~360 to ~800+ ARS per dollar overnight — 
  <strong>a 120% devaluation in a single day.</strong> By 2025 the rate had crossed 1,200 ARS/USD. 
  Yet the dollar price of a tulip bouquet barely moved.
</div>
""", unsafe_allow_html=True)

# ─── CHART 4: Side-by-side comparison bars ──────────────────────────────────────
st.markdown("""
<div class="section-header">
  <span class="section-num">04 ——</span>
  <h2 class="section-title">Side-by-Side: Cumulative Price Growth (Indexed to 2015)</h2>
  <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

base_usa     = df["usa_mid"].iloc[0]
base_ars     = df["arg_ars_mid"].iloc[0]
base_usd_ars = df["usd_ars"].iloc[0]
base_arg_usd = df["arg_usd_mid"].iloc[0]

df["usa_idx"]     = df["usa_mid"] / base_usa * 100
df["ars_idx"]     = df["arg_ars_mid"] / base_ars * 100
df["xrate_idx"]   = df["usd_ars"] / base_usd_ars * 100
df["arg_usd_idx"] = df["arg_usd_mid"] / base_arg_usd * 100

fig4 = go.Figure()

fig4.add_trace(go.Scatter(
    x=years, y=df["usa_idx"], name="🇺🇸 USA (USD)",
    mode="lines+markers",
    line=dict(color=GOLD, width=2.5),
    marker=dict(size=7, color=GOLD),
    hovertemplate="<b>USA %{x}</b><br>Index: %{y:.0f}<extra></extra>"
))
fig4.add_trace(go.Scatter(
    x=years, y=df["ars_idx"], name="🇦🇷 Argentina (ARS)",
    mode="lines+markers",
    line=dict(color=PINK, width=2.5),
    marker=dict(size=7, color=PINK),
    hovertemplate="<b>Argentina ARS %{x}</b><br>Index: %{y:,.0f}<extra></extra>"
))
fig4.add_trace(go.Scatter(
    x=years, y=df["xrate_idx"], name="💱 Exchange Rate (ARS/USD)",
    mode="lines+markers",
    line=dict(color=RED, width=2.5, dash="dash"),
    marker=dict(size=7, color=RED),
    hovertemplate="<b>Exchange Rate %{x}</b><br>Index: %{y:,.0f}<extra></extra>"
))
fig4.add_trace(go.Scatter(
    x=years, y=df["arg_usd_idx"], name="🇦🇷 Argentina (USD equiv.)",
    mode="lines+markers",
    line=dict(color=TEAL, width=2.5),
    marker=dict(size=7, color=TEAL),
    hovertemplate="<b>Argentina USD %{x}</b><br>Index: %{y:.0f}<extra></extra>"
))

fig4.add_hline(y=100, line_dash="dot", line_color="#2a2a3e", line_width=1)
fig4.add_annotation(x=2015.3, y=115, text="Baseline 2015 = 100",
    font=dict(size=9, color="#4a4a6a"), showarrow=False)

add_event_lines(fig4)
fig4.update_layout(**CHART_LAYOUT, title=dict(
    text="Indexed Growth (2015 = 100) — Log Scale",
    font=dict(family="Bebas Neue", size=18, color="#e8e8f0"), x=0.01
), yaxis_title="Index (2015 = 100)", yaxis_type="log", height=420)
fig4.update_layout(legend=dict(
    orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0
))
fig4.update_xaxes(tickmode="linear", dtick=1)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig4, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── CHART 5: Waterfall / annual change ─────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <span class="section-num">05 ——</span>
  <h2 class="section-title">Year-over-Year Peso Inflation on Tulip Prices</h2>
  <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

yoy = [None] + [
    (df["arg_ars_mid"].iloc[i] / df["arg_ars_mid"].iloc[i-1] - 1) * 100
    for i in range(1, len(df))
]

colors_yoy = [PINK if (v or 0) > 150 else GOLD if (v or 0) > 50 else TEAL for v in yoy[1:]]

fig5 = go.Figure()
fig5.add_trace(go.Bar(
    x=years[1:],
    y=yoy[1:],
    marker_color=colors_yoy,
    hovertemplate="<b>%{x}</b><br>YoY change: +%{y:.0f}%<extra></extra>",
    name="YoY % Change (ARS)"
))
fig5.update_layout(**CHART_LAYOUT, title=dict(
    text="Year-over-Year % Price Increase — Argentina (ARS)",
    font=dict(family="Bebas Neue", size=18, color="#e8e8f0"), x=0.01
), yaxis_title="% Change vs Prior Year", height=350, bargap=0.3)
fig5.update_xaxes(tickmode="linear", dtick=1)
fig5.add_hline(y=100, line_dash="dot", line_color="#ff4444", line_width=1, opacity=0.5)
fig5.add_annotation(x=2024.5, y=105, text="100% line", font=dict(size=9, color="#ff4444"), showarrow=False)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig5, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── DATA TABLE ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <span class="section-num">06 ——</span>
  <h2 class="section-title">Full Data Table</h2>
  <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

table_df = pd.DataFrame({
    "Year": years,
    "USA Low ($)": df["usa_low"],
    "USA High ($)": df["usa_high"],
    "ARG Low (ARS)": df["arg_ars_low"].apply(lambda x: f"{x:,}"),
    "ARG High (ARS)": df["arg_ars_high"].apply(lambda x: f"{x:,}"),
    "ARG (USD equiv.)": df["arg_usd_low"].apply(lambda x: f"${x}") + "–" + df["arg_usd_high"].apply(lambda x: f"${x}"),
    "USD→ARS Rate": df["usd_ars"].apply(lambda x: f"{x:,}"),
})

st.dataframe(
    table_df.set_index("Year"),
    use_container_width=True,
    height=420
)

# ─── TIMELINE ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <span class="section-num">07 ——</span>
  <h2 class="section-title">Key Events Timeline</h2>
  <div class="section-line"></div>
</div>

<div class="timeline">
  <div class="timeline-item">
    <div class="timeline-dot" style="color:#f5c842; background:#f5c842;"></div>
    <div class="timeline-year">2015</div>
    <div class="timeline-content"><strong>Macri Takes Office.</strong> Argentina exits currency controls ("cepo cambiario"). Official rate jumps from 9 to 14 ARS/USD almost immediately. Tulips: ~$100 ARS / ~$10 USD.</div>
  </div>
  <div class="timeline-item">
    <div class="timeline-dot" style="color:#ff4444; background:#ff4444;"></div>
    <div class="timeline-year">2018</div>
    <div class="timeline-content"><strong>IMF Crisis.</strong> Argentina requests a record $57B IMF bailout. The peso loses nearly 50% of its value in a single year, jumping from ~18 to ~38 ARS/USD. Tulips: ~$425 ARS but still ~$10 USD.</div>
  </div>
  <div class="timeline-item">
    <div class="timeline-dot" style="color:#ff8800; background:#ff8800;"></div>
    <div class="timeline-year">2020</div>
    <div class="timeline-content"><strong>COVID-19 Pandemic.</strong> Global supply chains disrupted. US tulip prices rise ~10–15% due to logistics costs. Argentina reimplements strict currency controls. Blue dollar premium widens.</div>
  </div>
  <div class="timeline-item">
    <div class="timeline-dot" style="color:#ffcc00; background:#ffcc00;"></div>
    <div class="timeline-year">2022</div>
    <div class="timeline-content"><strong>Hyperinflation Accelerates.</strong> Argentina's annual inflation hits 94%. The official rate reaches 350+ ARS/USD by year-end, but the informal "blue dollar" trades above 300 ARS/USD mid-year.</div>
  </div>
  <div class="timeline-item">
    <div class="timeline-dot" style="color:#ff44aa; background:#ff44aa;"></div>
    <div class="timeline-year">2023</div>
    <div class="timeline-content"><strong>Milei Elected — Devaluation Shock.</strong> President Javier Milei takes office in December and immediately devalues the peso by ~120% overnight (360 → 800+ ARS/USD). Annual inflation hits 211%. Tulips: ~$22,500 ARS but still ~$14 USD.</div>
  </div>
  <div class="timeline-item">
    <div class="timeline-dot" style="color:#00e5cc; background:#00e5cc;"></div>
    <div class="timeline-year">2025</div>
    <div class="timeline-content"><strong>Stabilization Attempts.</strong> Exchange rate crosses 1,200 ARS/USD. Inflation begins to slow but cumulative damage is massive. Tulips: ~$80,000 ARS — 800× their 2015 price in pesos, but still just ~$13–15 in dollars.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  🌷 TULIP PRICE ODYSSEY · 2015–2025 · DATA: MARKET RESEARCH & FLORIST SURVEYS (ESTIMATED) · 
  BUILT WITH STREAMLIT + PLOTLY · FOR EDUCATIONAL PURPOSES
</div>
""", unsafe_allow_html=True)
