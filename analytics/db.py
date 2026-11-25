"""Database access for the dashboard.

Reuses the SQLAlchemy engine already defined in schema_inspector.py
(credentials come from .env), so there is exactly one connection setup.
"""
from decimal import Decimal

import pandas as pd
from sqlalchemy import bindparam, text

from schema_inspector import engine


def _normalise(df: pd.DataFrame) -> pd.DataFrame:
    """MySQL returns DECIMAL as decimal.Decimal; convert to float for Plotly/Pandas."""
    for col in df.columns:
        if df[col].dtype == object:
            sample = df[col].dropna()
            if not sample.empty and isinstance(sample.iloc[0], Decimal):
                df[col] = df[col].astype(float)
    return df


def run_query(sql: str, params: dict | None = None) -> pd.DataFrame:
    """Run a trusted, parameterised dashboard query and return a DataFrame.

    List/tuple parameters are bound as expanding IN-lists. Values are always
    bound parameters, never string-formatted into the SQL.
    """
    params = params or {}
    stmt = text(sql)
    expanding = [
        bindparam(key, expanding=True)
        for key, value in params.items()
        if isinstance(value, (list, tuple))
    ]
    if expanding:
        stmt = stmt.bindparams(*expanding)

    with engine.connect() as connection:
        result = connection.execute(stmt, params)
        df = pd.DataFrame(result.fetchall(), columns=list(result.keys()))
    return _normalise(df)
