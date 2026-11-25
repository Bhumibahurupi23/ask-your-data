"""Small display-formatting helpers."""


def fmt_money(value) -> str:
    v = float(value or 0)
    a = abs(v)
    if a >= 1_000_000:
        return f"${v / 1_000_000:,.2f}M"
    if a >= 100_000:
        return f"${v / 1_000:,.1f}K"
    if a >= 10_000:
        return f"${v:,.0f}"
    return f"${v:,.2f}"


def fmt_int(value) -> str:
    return f"{int(round(float(value or 0))):,}"


def fmt_pct(value, signed: bool = False) -> str:
    v = float(value or 0)
    return f"{v:+.1f}%" if signed else f"{v:.1f}%"


def truncate(text, limit: int = 34) -> str:
    text = str(text)
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"
