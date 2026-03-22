# budget-tracker-backend

```bash
python -m venv .venv
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null
pip install -r requirements.txt
python -m app.main
```

## Ruff

```bash
ruff check . \
  --fix \
  --select E,F,I,B,UP,ASYNC \
  --ignore E501 \
  --target-version py312
```

## Alembic

Generate migration script automatically:

```bash
alembic revision --autogenerate -m "message"
```

Apply latest migrations:

```bash
alembic upgrade head
```

Undo the last migration (go back one version):

```bash
alembic downgrade -1
```

See migration history:

```bash
alembic histor
```
