import pytest

from app import orders, products, reports, users
from app.db import make_engine


@pytest.fixture
def engine():
    return make_engine()


@pytest.fixture
def ids(engine):
    alice = users.create_user(engine, "alice", "alice@example.com")
    bob = users.create_user(engine, "bob", "bob@example.com")
    products.add_product(engine, "SKU-1", "Widget", 10)
    products.add_product(engine, "SKU-2", "Gadget", 2)
    return {"alice": alice, "bob": bob}


def test_users(engine, ids):
    alice = ids["alice"]
    assert users.get_user(engine, alice)["email"] == "alice@example.com"
    assert users.find_by_email(engine, "bob@example.com")["name"] == "bob"
    users.deactivate(engine, alice)
    assert users.active_names(engine) == ["bob"]


def test_stock(engine, ids):
    assert products.stock_for(engine, "SKU-1") == 10
    products.restock(engine, "SKU-2", 5)
    assert products.stock_for(engine, "SKU-2") == 7
    assert products.low_stock(engine, 8) == {"SKU-2": 7}


def test_orders(engine, ids):
    alice = ids["alice"]
    order_id = orders.place_order(engine, alice, "SKU-1", 3)
    assert products.stock_for(engine, "SKU-1") == 7
    assert orders.orders_for_user(engine, alice)[0]["title"] == "Widget"
    assert orders.cancel_order(engine, order_id) is True
    assert products.stock_for(engine, "SKU-1") == 10
    with pytest.raises(ValueError):
        orders.place_order(engine, alice, "SKU-2", 99)


def test_reports(engine, ids):
    orders.place_order(engine, ids["alice"], "SKU-1", 2)
    orders.place_order(engine, ids["bob"], "SKU-1", 5)
    assert reports.order_counts_by_status(engine) == {"placed": 2}
    assert reports.top_customers(engine) == [("bob", 5), ("alice", 2)]
