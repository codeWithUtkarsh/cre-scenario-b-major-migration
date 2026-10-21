"""Schema and engine for the shop database."""

import sqlalchemy as sa

metadata = sa.MetaData()

users = sa.Table(
    "users", metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(80), nullable=False),
    sa.Column("email", sa.String(120), unique=True),
    sa.Column("active", sa.Boolean, default=True),
)

products = sa.Table(
    "products", metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("sku", sa.String(20), unique=True),
    sa.Column("title", sa.String(120)),
    sa.Column("stock", sa.Integer, default=0),
)

orders = sa.Table(
    "orders", metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    sa.Column("product_id", sa.Integer, sa.ForeignKey("products.id")),
    sa.Column("quantity", sa.Integer),
    sa.Column("status", sa.String(20)),
)


def make_engine(url: str = "sqlite://"):
    engine = sa.create_engine(url)
    metadata.create_all(engine)
    return engine
