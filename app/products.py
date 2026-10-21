"""Product catalogue and stock."""

import sqlalchemy as sa

from app.db import products


def add_product(engine, sku, title, stock):
    result = engine.execute(products.insert(), sku=sku, title=title, stock=stock)
    return result.inserted_primary_key[0]


def stock_for(engine, sku):
    return engine.execute(sa.select([products.c.stock]).where(products.c.sku == sku)).scalar()


def restock(engine, sku, quantity):
    engine.execute("UPDATE products SET stock = stock + ? WHERE sku = ?", quantity, sku)


def low_stock(engine, threshold):
    rows = engine.execute(
        sa.select([products.c.sku, products.c.stock]).where(products.c.stock < threshold)
    )
    return {row["sku"]: row["stock"] for row in rows}
