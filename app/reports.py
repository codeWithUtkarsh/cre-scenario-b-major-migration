"""Reporting queries."""

import sqlalchemy as sa

from app.db import orders


def order_counts_by_status(engine):
    rows = engine.execute(sa.select([orders.c.status, sa.func.count()]).group_by(orders.c.status))
    return {status: count for status, count in rows}


def top_customers(engine, limit=3):
    rows = engine.execute(
        "SELECT u.name AS name, SUM(o.quantity) AS items FROM orders o "
        "JOIN users u ON u.id = o.user_id WHERE o.status = 'placed' "
        "GROUP BY u.id ORDER BY items DESC LIMIT ?",
        limit,
    )
    return [(row["name"], row["items"]) for row in rows]
