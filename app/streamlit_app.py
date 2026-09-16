"""Tiller Demand Forecast — static-data MVP."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

BLUE = "#2E398C"
BLACK = "#000000"
MUTED = "#6D6F6E"
GRID = "#ECEBE6"
CARD_TOP = "#F6F7FB"
GREEN = "#00A552"
AMBER = "#9E3900"
RED = "#ef4444"

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

APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR / "data" / "weekly_store_orders.csv"

@st.cache_data
def load_weekly_orders(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["week"])
    df["id_store"] = df["id_store"].astype(str)
    df["orders"] = pd.to_numeric(df["orders"], errors="coerce")
    df["week"] = df["week"].dt.normalize()
    return df.dropna(subset=["week", "orders"]).sort_values(["id_store", "week"])

if not DATA_PATH.exists():
    st.error("App data is missing. Run `python3 prepare_app_data.py` from the repository root.")
    st.stop()

weekly = load_weekly_orders(DATA_PATH)

store_summary = (
    weekly.groupby("id_store")["orders"]
    .agg(total_orders="sum", observed_weeks="count")
    .query("observed_weeks >= 12")
    .sort_values("total_orders", ascending=False)
)

if store_summary.empty:
    st.error("No store has enough weekly history to create the forecast.")
    st.stop()

STORE_ID = store_summary.index[0]
store = weekly.loc[weekly["id_store"] == STORE_ID].copy().sort_values("week")

if len(store) < 6:
    st.error("The selected store has insufficient history for this prototype.")
    st.stop()

latest_week = store["week"].max()
latest_actual = int(store.iloc[-1]["orders"])
previous_week = int(store.iloc[-2]["orders"])
two_weeks_ago = int(store.iloc[-3]["orders"])

next_week_forecast = latest_actual
following_week_forecast = two_weeks_ago
two_week_total = next_week_forecast + following_week_forecast

baseline_next_week = previous_week
baseline_following_week = int(store.iloc[-4]["orders"]) if len(store) >= 4 else two_weeks_ago
baseline_two_week = baseline_next_week + baseline_following_week

def pct_change(current: float, baseline: float) -> float:
    if baseline == 0:
        return 0.0
    return ((current - baseline) / baseline) * 100

next_week_change = pct_change(next_week_forecast, baseline_next_week)
following_week_change = pct_change(following_week_forecast, baseline_following_week)
total_change = pct_change(two_week_total, baseline_two_week)

# Reliability state based on Phase 3 H6 threshold (41.9%)
# Note: Threshold from retrospective test-period analysis
wow_change = abs(next_week_change)
H6_THRESHOLD = 41.9

if wow_change <= H6_THRESHOLD:
    reliability_1week_label = "Stable"
    reliability_1week_text = "Recent demand steady"
else:
    reliability_1week_label = "Use caution"
    reliability_1week_text = "Recent demand volatile"

next_week_date = latest_week + pd.Timedelta(days=7)
following_week_date = latest_week + pd.Timedelta(days=14)

# Navbar
logo = APP_DIR / "tiller_logo.png"
if logo.exists():
    import base64
    b64 = base64.b64encode(logo.read_bytes()).decode()
    logo_html = f'<img src="data:image/png;base64,{b64}" width="132" height="36" style="display:block;object-fit:contain" />'
else:
    logo_html = f'<span style="color:{BLUE};font-weight:700;letter-spacing:0.14em;font-size:18px">TILLER</span>'

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
          <span style="color:{BLACK};font-size:20px;font-weight:400">Café Lumière</span>
          <span style="width:36px;height:36px;border-radius:999px;background:{BLUE};color:white;
            display:inline-flex;align-items:center;justify-content:center;font-size:16px;font-weight:500">CL</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

def forecast_card(title, value, pct, baseline, status_color, status_label, status_sub):
    arrow = "↑" if pct >= 0 else "↓"
    pill_color = GREEN if pct > 0.5 else (RED if pct < -0.5 else MUTED)
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
        letter-spacing:-2px;margin:0;font-family:Roboto,system-ui,sans-serif">{value:,}</div>
      <div style="display:flex;flex-direction:column;gap:2px;padding-top:6px">
        <div style="color:{pill_color};font-size:16px;font-weight:500;line-height:1.2">{arrow} {abs(pct):.1f}%</div>
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
            next_week_forecast,
            next_week_change,
            "vs previous week",
            GREEN,
            reliability_1week_label,
            reliability_1week_text,
        ),
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        forecast_card(
            "Expected orders · Next 2 weeks",
            two_week_total,
            total_change,
            "vs previous 2-week period",
            AMBER,
            "Longer horizon",
            "Phase 3: higher error at 2-week horizon",
        ),
        unsafe_allow_html=True,
    )

st.markdown(
    f"<p style='text-align:center;color:{MUTED};font-size:12px;font-weight:500;margin:16px 0'>"
    "2-week forecasts are generally less accurate than 1-week forecasts.</p>",
    unsafe_allow_html=True,
)

# Chart: Show last 10 weeks of history + 2 forecast weeks
n_history_weeks = 10
history = store.tail(n_history_weeks).copy()
forecast_dates = [next_week_date, following_week_date]
forecast_values = [next_week_forecast, following_week_forecast]

fig = go.Figure()

# Get actual dates from data
history_dates = history["week"].tolist()
forecast_date_objs = [next_week_date, following_week_date]

# Combine all dates for X-axis
all_dates = history_dates + forecast_date_objs

# Show every other week label (best practice for 10+ weeks)
tick_indices = list(range(0, len(all_dates), 2))
tick_vals = [all_dates[i] for i in tick_indices]
tick_text = [d.strftime("%d %b") for d in tick_vals]

fig.add_trace(
    go.Scatter(
        x=history_dates,
        y=history["orders"],
        mode="lines+markers",
        name="Actual",
        line=dict(color="#292E34", width=2.5),
        marker=dict(size=9, color="#292E34"),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:,} orders<br>Actual<extra></extra>",
    )
)

# Connect last actual to first forecast point
last_actual_date = history_dates[-1]
fig.add_trace(
    go.Scatter(
        x=[last_actual_date] + forecast_date_objs,
        y=[history["orders"].iloc[-1]] + forecast_values,
        mode="lines+markers",
        name="Forecast",
        line=dict(color=BLUE, width=2.5, dash="dash"),
        marker=dict(size=9, color=BLUE),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:,} orders<br>Forecast<extra></extra>",
    )
)

max_y = max(history["orders"].max(), max(forecast_values))

fig.update_layout(
    title=dict(text="Recent demand", font=dict(size=22, color=BLACK)),
    height=360,
    margin=dict(l=48, r=24, t=48, b=56),
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
    hovermode="x unified",
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=13, color=BLACK),
        tickmode="array",
        tickvals=tick_vals,
        ticktext=tick_text,
    ),
    yaxis=dict(
        range=[0, max_y * 1.22],
        gridcolor="#E7E7E7",
        zeroline=False,
        tickfont=dict(size=12, color=BLACK),
        title="Orders",
        title_font=dict(color=MUTED, size=11),
    ),
)

st.plotly_chart(fig, width="stretch")

st.caption(
    "Prototype uses a static historical dataset and a simple lag-based forecasting rule. "
    "Forecasts are based on your store's historical order patterns. When recent demand becomes less stable, "
    "reliability will show caution. Decision support only — no automated recommendations."
)
