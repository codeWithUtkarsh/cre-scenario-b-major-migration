"""Placing and cancelling orders."""

import sqlalchemy as sa

from app.db import orders, products


def place_order(engine, user_id, sku, quantity):
    with engine.begin() as conn:
        product = conn.execute(sa.select([products]).where(products.c.sku == sku)).fetchone()
        if product is None:
            raise ValueError(f"unknown product {sku}")
        if product["stock"] < quantity:
            raise ValueError("insufficient stock")
        conn.execute(
            products.update().where(products.c.id == product["id"]).values(stock=product["stock"] - quantity)
        )
        result = conn.execute(
            orders.insert().values(user_id=user_id, product_id=product["id"], quantity=quantity, status="placed")
        )
        return result.inserted_primary_key[0]


def cancel_order(engine, order_id):
    with engine.begin() as conn:
        row = conn.execute("SELECT product_id, quantity, status FROM orders WHERE id = ?", order_id).fetchone()
        if row is None or row["status"] == "cancelled":
            return False
        conn.execute("UPDATE products SET stock = stock + ? WHERE id = ?", row["quantity"], row["product_id"])
        conn.execute("UPDATE orders SET status = 'cancelled' WHERE id = ?", order_id)
        return True


def orders_for_user(engine, user_id):
    query = (
        sa.select([orders.c.id, products.c.title, orders.c.quantity, orders.c.status])
        .select_from(orders.join(products, orders.c.product_id == products.c.id))
        .where(orders.c.user_id == user_id)
        .order_by(orders.c.id)
    )
    return [dict(row) for row in engine.execute(query)]
