init:
	pip install uv
	uv venv
	uv pip install -e ".[dev]"

run:
	uv run gunicorn app.main:app --workers=4 --bind 0.0.0.0:5000 --reload

test:
	uv run pytest tests/unit

integration-test:
	uv run pytest tests/integration

coverage:
	uv run pytest tests/unit --doctest-modules --junitxml=junit/test-results.xml --cov=app --cov-report=xml --cov-report=html

lint:
	uv run pylint app
