"""Design tokens, global CSS and the shared Plotly styling."""
import streamlit as st

BG = "#0B1220"
SURFACE = "#111A2E"
BORDER = "#1E2A44"
GRID = "#18233B"
TEXT = "#E6EAF2"
MUTED = "#8B98B3"
ACCENT = "#6C8CFF"
TEAL = "#2DD4BF"
RED = "#F87171"
PALETTE = [ACCENT, TEAL, "#A78BFA", "#64748B", "#F59E0B"]

PLOT_CONFIG = {"displayModeBar": False}


def rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


def style_fig(fig, height: int = 320, legend: bool = False):
    """Apply the dashboard look to any Plotly figure."""
    fig.update_layout(
        height=height,
        margin=dict(l=4, r=4, t=6, b=4),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Segoe UI, sans-serif", color=MUTED, size=12),
        showlegend=legend,
        legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center", font=dict(size=12)),
        hoverlabel=dict(bgcolor=BG, bordercolor=BORDER, font=dict(color=TEXT, size=12)),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=BORDER, tickfont=dict(size=11))
    fig.update_yaxes(gridcolor=GRID, zeroline=False, tickfont=dict(size=11))
    return fig


_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root{
  --bg:#0B1220; --surface:#111A2E; --border:#1E2A44;
  --text:#E6EAF2; --muted:#8B98B3; --accent:#6C8CFF; --teal:#2DD4BF; --red:#F87171;
}

.stApp{
  background:
    radial-gradient(1100px 560px at 88% -12%, rgba(108,140,255,.10), transparent 60%),
    linear-gradient(180deg,#0B1220 0%,#0A1019 100%);
  font-family:'Inter',-apple-system,'Segoe UI',sans-serif;
}
#MainMenu, footer{visibility:hidden;}
header[data-testid="stHeader"]{background:transparent;}
.block-container{padding-top:1.4rem;padding-bottom:3rem;max-width:1480px;}

/* ---------- sidebar ---------- */
[data-testid="stSidebar"]{background:#0A101D;border-right:1px solid #18233B;}
[data-testid="stSidebar"] [role="radiogroup"]{gap:2px;}
[data-testid="stSidebar"] [role="radiogroup"] label{
  padding:9px 12px;border-radius:10px;width:100%;cursor:pointer;
  border:1px solid transparent;transition:background .15s,border-color .15s;
}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child{display:none;}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:rgba(108,140,255,.08);}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){
  background:rgba(108,140,255,.14);border-color:rgba(108,140,255,.30);
}
[data-testid="stSidebar"] [role="radiogroup"] label p{font-size:.92rem;font-weight:500;color:var(--muted);}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p{color:#fff;}

.brand{display:flex;align-items:center;gap:12px;padding:6px 6px 18px 6px;}
.brand-mark{
  width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,#6C8CFF 0%,#4F6BE8 55%,#2DD4BF 130%);
  color:#fff;font-weight:700;font-size:1.05rem;box-shadow:0 6px 18px rgba(108,140,255,.35);
}
.brand-name{font-weight:650;font-size:1.02rem;color:var(--text);letter-spacing:-.01em;line-height:1.1;}
.brand-sub{font-size:.72rem;color:var(--muted);margin-top:3px;}
.nav-label{font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:#5E6B87;padding:4px 8px 6px;}
.side-foot{font-size:.72rem;color:#5E6B87;padding:10px 8px;border-top:1px solid #18233B;margin-top:18px;}

/* ---------- page header ---------- */
.page-header{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;
  flex-wrap:wrap;margin-bottom:14px;}
.eyebrow{font-size:.76rem;color:var(--muted);letter-spacing:.02em;margin-bottom:4px;}
.page-title{font-size:1.65rem;font-weight:650;letter-spacing:-.02em;color:var(--text);line-height:1.15;}
.page-sub{font-size:.9rem;color:var(--muted);margin-top:4px;}
.chips{display:flex;gap:8px;flex-wrap:wrap;}
.chip{font-size:.74rem;color:#B6C2DB;background:rgba(108,140,255,.08);
  border:1px solid rgba(108,140,255,.22);padding:5px 10px;border-radius:999px;white-space:nowrap;}

/* ---------- cards ---------- */
[class*="st-key-card_"], .st-key-filter_bar{
  background:var(--surface);border:1px solid var(--border)!important;border-radius:14px;
  box-shadow:0 1px 0 rgba(255,255,255,.03) inset,0 10px 28px rgba(0,0,0,.28);
}
.sec-title{font-size:.95rem;font-weight:600;color:var(--text);letter-spacing:-.01em;}
.sec-sub{font-size:.78rem;color:var(--muted);margin:2px 0 6px;}

.kpi-card{position:relative;overflow:hidden;background:var(--surface);border:1px solid var(--border);
  border-radius:14px;padding:16px 18px 14px;height:100%;
  box-shadow:0 1px 0 rgba(255,255,255,.03) inset,0 10px 28px rgba(0,0,0,.28);}
.kpi-card::before{content:"";position:absolute;inset:0 0 auto 0;height:2px;
  background:linear-gradient(90deg,var(--accent),rgba(45,212,191,.7),transparent);opacity:.85;}
.kpi-label{font-size:.7rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);font-weight:500;}
.kpi-value{font-size:1.7rem;font-weight:650;letter-spacing:-.02em;color:var(--text);margin:8px 0 8px;line-height:1.1;}
.kpi-foot{display:flex;align-items:center;gap:8px;font-size:.76rem;color:var(--muted);min-height:20px;}
.kpi-delta{font-weight:600;padding:2px 7px;border-radius:6px;font-size:.72rem;}
.kpi-delta.up{color:var(--teal);background:rgba(45,212,191,.10);}
.kpi-delta.down{color:var(--red);background:rgba(248,113,113,.10);}
.kpi-delta.flat{color:var(--muted);background:rgba(139,152,179,.10);}

.status-dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:8px;}
.status-dot.ok{background:var(--teal);box-shadow:0 0 0 4px rgba(45,212,191,.15);}
.status-dot.bad{background:var(--red);box-shadow:0 0 0 4px rgba(248,113,113,.15);}
.status-line{font-size:1.05rem;font-weight:600;color:var(--text);}
.muted{color:var(--muted);font-size:.85rem;}
</style>
"""


def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
