import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
import base64

BLUE = "#2E398C"
BLACK = "#000000"
MUTED = "#6D6F6E"
GRID = "#ECEBE6"
CARD_TOP = "#F6F7FB"
GREEN = "#00A552"
AMBER = "#9E3900"

st.set_page_config(page_title="Demand Forecast", layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
header[data-testid='stHeader']{display:none}
#MainMenu,footer{visibility:hidden}
.stApp{background:#FFFFFF}
.block-container{max-width:1120px;padding-top:0.75rem;padding-bottom:2rem}
</style>
""",
    unsafe_allow_html=True,
)

DATA = {
    "series": [
        ("May 5", 1100, "actual"),
        ("May 12", 1450, "actual"),
        ("May 19", 1050, "actual"),
        ("May 26", 1500, "actual"),
        ("Jun 2", 1000, "actual"),
        ("Jun 9", 1400, "actual"),
        ("Jun 16", 1200, "actual"),
        ("Jun 23", 1450, "forecast"),
        ("Jun 30", 1230, "forecast"),
    ],
}

logo = Path(__file__).parent / "tiller_logo.png"
if logo.exists():
    b64 = base64.b64encode(logo.read_bytes()).decode()
    logo_html = f'<img src="data:image/png;base64,{b64}" width="132" height="36" style="display:block;object-fit:contain" />'
else:
    logo_html = f'<span style="color:{BLUE};font-weight:700;letter-spacing:0.14em;font-size:18px">TILLER</span>'

# Navbar: logo | separator | title   gap 24px — NO bottom border under nav
left, right = st.columns([4, 2])
with left:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:24px">
          {logo_html}
          <div style="width:1px;height:24px;background:{GRID};flex-shrink:0"></div>
          <div style="color:{BLACK};font-size:29px;font-weight:700;line-height:1.1;
            font-family:Roboto,system-ui,sans-serif">Demand Forecast</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        f"""
        <div style="display:flex;justify-content:flex-end;align-items:center;gap:12px;height:36px">
          <span style="color:{BLACK};font-size:20px;font-weight:400">Cafe Lumiere</span>
          <span style="width:36px;height:36px;border-radius:999px;background:{BLUE};color:white;
            display:inline-flex;align-items:center;justify-content:center;font-size:16px;font-weight:500">CL</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Space only — no horizontal rule under navbar
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)


def forecast_card(title, value, pct, baseline, status_color, status_label, status_sub):
    # Top block: padding 16 24 24 24, gap 24 between label and numbers
    return f"""
<div style="border-radius:16px;overflow:hidden;background:#fff">
  <div style="
    display:flex;
    padding:16px 24px 24px 24px;
    flex-direction:column;
    align-items:flex-start;
    gap:24px;
    border-radius:16px 16px 0 0;
    border-top:1px solid {GRID};
    border-right:1px solid {GRID};
    border-left:1px solid {GRID};
    background:{CARD_TOP};
  ">
    <div style="color:{BLACK};font-size:16px;font-weight:500;margin:0;line-height:1.2;
      font-family:Roboto,system-ui,sans-serif">{title}</div>
    <div style="display:flex;align-items:flex-start;gap:12px;margin:0">
      <div style="color:{BLACK};font-size:56px;font-weight:700;line-height:1;
        letter-spacing:-2px;margin:0;font-family:Roboto,system-ui,sans-serif">{value}</div>
      <div style="display:flex;flex-direction:column;gap:2px;padding-top:6px">
        <div style="color:{BLUE};font-size:16px;font-weight:500;line-height:1.2">↑ {pct}</div>
        <div style="color:{BLUE};font-size:16px;font-weight:500;line-height:1.2">{baseline}</div>
      </div>
    </div>
  </div>
  <div style="
    padding:16px 24px;
    border:1px solid {GRID};
    border-top:none;
    border-radius:0 0 16px 16px;
    background:#fff;
  ">
    <div style="display:flex;align-items:center;gap:8px">
      <span style="width:8px;height:8px;border-radius:999px;background:{status_color};display:inline-block"></span>
      <span style="color:{status_color};font-size:14px;font-weight:500">{status_label}</span>
    </div>
    <div style="margin-top:4px;color:{MUTED};font-size:12px;font-weight:500">{status_sub}</div>
  </div>
</div>
"""

c1, c2 = st.columns(2)
with c1:
    st.markdown(
        forecast_card(
            "Expected orders · Next week",
            "1,250",
            "4.2%",
            "vs previous week",
            GREEN,
            "Stable",
            "Recent demand steady",
        ),
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        forecast_card(
            "Expected orders · Next 2 weeks",
            "2,480",
            "3.1%",
            "vs previous 2-week period",
            AMBER,
            "Longer horizon",
            "Typically less accurate than 1-week",
        ),
        unsafe_allow_html=True,
    )

st.markdown(
    f"<p style='text-align:center;color:{MUTED};font-size:12px;font-weight:500;margin:16px 0'>"
    "2-week forecasts are generally less accurate than 1-week forecasts.</p>",
    unsafe_allow_html=True,
)

ax, ay, fx, fy, last = [], [], [], [], None
for lab, y, t in DATA["series"]:
    if t == "actual":
        ax.append(lab)
        ay.append(y)
        last = (lab, y)
    else:
        if last and not fx:
            fx.append(last[0])
            fy.append(last[1])
        fx.append(lab)
        fy.append(y)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=ax, y=ay, mode="lines+markers", name="Actual",
        line=dict(color="#292E34", width=2.5), marker=dict(size=9, color="#292E34"),
    )
)
fig.add_trace(
    go.Scatter(
        x=fx, y=fy, mode="lines+markers", name="Forecast",
        line=dict(color=BLUE, width=2.5, dash="dash"), marker=dict(size=9, color=BLUE),
    )
)
if last:
    fig.add_vline(x=last[0], line_dash="dot", line_color="#9CA3AF")
    fig.add_annotation(
        x=last[0], y=1600, text="Today", showarrow=False,
        bgcolor="black", font=dict(color="white", size=12),
    )

fig.update_layout(
    title=dict(text="Recent demand", font=dict(size=22, color=BLACK)),
    height=360,
    margin=dict(l=48, r=24, t=48, b=56),
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
    xaxis=dict(showgrid=False, tickfont=dict(size=15, color=BLACK)),
    yaxis=dict(range=[0, 2000], gridcolor="#E7E7E7", tickfont=dict(size=12, color=BLACK)),
)
st.plotly_chart(fig, width="stretch")

st.caption(
    "Forecasts are based on your store historical order patterns. "
    "When recent demand becomes less stable, reliability will show caution. "
    "Decision support only - no automated recommendations."
)
