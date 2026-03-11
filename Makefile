run:
	docker compose up --build app

test:
	docker compose run --rm app pytest

lint:
	docker compose run --rm app ruff check .
