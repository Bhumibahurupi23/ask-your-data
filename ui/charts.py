"""Reusable Plotly chart builders (consistent, restrained styling)."""
import plotly.graph_objects as go

from ui.format import fmt_money, truncate
from ui.theme import ACCENT, BG, PALETTE, RED, TEAL, TEXT, rgba, style_fig


def area_trend(df, x: str, y: str, color: str = ACCENT, name: str = "Sales", height: int = 300):
    fig = go.Figure(
        go.Scatter(
            x=df[x], y=df[y], mode="lines", name=name,
            line=dict(color=color, width=2.4),
            fill="tozeroy", fillcolor=rgba(color, 0.12),
            hovertemplate="%{x|%b %Y}<br>$%{y:,.0f}<extra></extra>",
        )
    )
    fig.update_yaxes(tickprefix="$", tickformat="~s")
    fig.update_xaxes(tickformat="%b %Y")
    return style_fig(fig, height)


def profit_bars(df, x: str, y: str, height: int = 300):
    colors = [TEAL if v >= 0 else RED for v in df[y]]
    fig = go.Figure(
        go.Bar(
            x=df[x], y=df[y], marker=dict(color=colors, cornerradius=3),
            hovertemplate="%{x|%b %Y}<br>$%{y:,.0f}<extra></extra>",
        )
    )
    fig.update_yaxes(tickprefix="$", tickformat="~s")
    fig.update_xaxes(tickformat="%b %Y")
    return style_fig(fig, height)


def donut(df, label: str, value: str, height: int = 300):
    total = float(df[value].sum())
    fig = go.Figure(
        go.Pie(
            labels=df[label], values=df[value], hole=0.66, sort=False,
            marker=dict(colors=PALETTE[: len(df)], line=dict(color=BG, width=3)),
            textinfo="percent", textfont=dict(color="#fff", size=12),
            hovertemplate="%{label}<br>$%{value:,.0f} (%{percent})<extra></extra>",
        )
    )
    fig.add_annotation(
        text=f"<b>{fmt_money(total)}</b><br><span style='font-size:11px'>total</span>",
        showarrow=False, font=dict(size=18, color=TEXT),
    )
    return style_fig(fig, height, legend=True)


def hbar(df, label: str, value: str, color: str = ACCENT, money: bool = True,
         height: int = 300, label_len: int = 30):
    """Horizontal bar chart, largest bar on top, long labels truncated."""
    d = df.sort_values(value, ascending=True)
    texts = [fmt_money(v) if money else f"{v:,.0f}" for v in d[value]]
    hover = "%{customdata}<br>" + ("$%{x:,.0f}" if money else "%{x:,.0f}") + "<extra></extra>"
    fig = go.Figure(
        go.Bar(
            x=d[value], y=[truncate(s, label_len) for s in d[label]], orientation="h",
            customdata=d[label], marker=dict(color=color, cornerradius=4),
            text=texts, textposition="outside", cliponaxis=False,
            textfont=dict(color=TEXT, size=11), hovertemplate=hover,
        )
    )
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, tickfont=dict(color=TEXT, size=12))
    fig.update_layout(margin=dict(l=4, r=56, t=6, b=4))
    return style_fig(fig, height)
