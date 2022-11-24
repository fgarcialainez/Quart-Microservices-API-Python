populate-db:
	docker-compose run --rm core quart populate-db

drop-db:
	docker-compose run --rm core quart drop-db

run:
	docker-compose up

clean:
	docker-compose down --rmi all

test:
	docker-compose run --rm core python -m pytest -vv -c /app/pyproject.toml

lint:
	docker-compose run --rm core flake8
