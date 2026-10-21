# Scenario B: major code change

The data layer is written against SQLAlchemy 1.x idioms in every module:
`engine.execute(...)`, `select([...])`, raw SQL strings with positional
parameters, and string-keyed row access. SQLAlchemy 2.x removes all of them,
so updating it means migrating the whole data layer.

Expected: a PR with the safe updates (requests, pytest), SQLAlchemy held back,
and a story describing the migration for a developer.
