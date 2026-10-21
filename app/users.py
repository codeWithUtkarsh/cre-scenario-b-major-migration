"""User accounts."""

import sqlalchemy as sa

from app.db import users


def create_user(engine, name, email):
    result = engine.execute(users.insert().values(name=name, email=email, active=True))
    return result.inserted_primary_key[0]


def get_user(engine, user_id):
    row = engine.execute(sa.select([users]).where(users.c.id == user_id)).fetchone()
    return dict(row) if row else None


def find_by_email(engine, email):
    row = engine.execute("SELECT id, name FROM users WHERE email = ?", email).fetchone()
    return {"id": row["id"], "name": row["name"]} if row else None


def deactivate(engine, user_id):
    engine.execute(users.update().where(users.c.id == user_id).values(active=False))


def active_names(engine):
    rows = engine.execute(
        sa.select([users.c.name]).where(users.c.active == True).order_by(users.c.name)  # noqa: E712
    )
    return [row["name"] for row in rows]
