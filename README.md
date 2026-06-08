![Project Architecture](./docs/images/clean_architecture.png)

# Essential Commands

[Local]  
- Install deps and create venv: uv sync  
- Add deps: uv add fastapi
- Remove deps: uv remove fastapi
- Activate venv: source .venv/bin/activate
- Run Application: uv run fastapi dev app/main.py
- Deactivate venv: deactivate
- Generate ORM Schema: uv run alembic revision --autogenerate -m "initial_schema"
- Run Migrations: uv run alembic upgrade head

[Docker]
- Run Application (Runtime environment changes): docker-compose -f docker-compose.dev.yml up -d --build
- Run Application (Coding changes): docker-compose -f docker-compose.dev.yml up -d
- Down Application (Normal): docker-compose -f docker-compose.dev.yml down
- Down Application (Down volumes and delete DB): docker-compose -f docker-compose.dev.yml down -v