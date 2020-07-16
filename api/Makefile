init:
	pip install pipenv
	pipenv install --dev

run:
	pipenv run gunicorn app.main:app --workers=4 --bind 0.0.0.0:5000 --reload

test:
	pipenv run pytest tests/unit

integration-test:
	pipenv run pytest tests/integration

coverage:
	pipenv run pytest tests/unit --doctest-modules --junitxml=junit/test-results.xml --cov=app --cov-report=xml --cov-report=html

lint:
	pipenv run pylint app