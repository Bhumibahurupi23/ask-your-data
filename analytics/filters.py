"""Global dashboard filters and the SQL WHERE clause they produce."""
from dataclasses import dataclass, replace
from datetime import date, timedelta

# Every dashboard query uses the same joined base so filters apply uniformly.
BASE_FROM = """
FROM order_items oi
JOIN orders o     ON oi.order_id   = o.order_id
JOIN products p   ON oi.product_id = p.product_id
JOIN customers c  ON o.customer_id = c.customer_id
"""


@dataclass(frozen=True)
class Filters:
    start: date
    end: date
    regions: tuple = ()
    categories: tuple = ()
    segments: tuple = ()
    ship_modes: tuple = ()

    def previous_period(self) -> "Filters":
        """Same-length window immediately before this one (for KPI deltas)."""
        span = (self.end - self.start).days + 1
        return replace(
            self,
            start=self.start - timedelta(days=span),
            end=self.start - timedelta(days=1),
        )

    def where(self) -> tuple[str, dict]:
        """Return (WHERE-clause body, bound params). Empty selection = no filter."""
        clauses = ["o.order_date BETWEEN :start AND :end"]
        params: dict = {
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
        }
        for column, name, values in (
            ("o.region", "regions", self.regions),
            ("p.category", "categories", self.categories),
            ("c.segment", "segments", self.segments),
            ("o.ship_mode", "ship_modes", self.ship_modes),
        ):
            if values:
                clauses.append(f"{column} IN :{name}")
                params[name] = list(values)
        return " AND ".join(clauses), params
