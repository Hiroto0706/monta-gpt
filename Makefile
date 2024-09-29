DATABASE_URL=postgresql://postgres:password@localhost:5432/monta-gpt?sslmode=disable

.PHONY: createdb
createdb:
	docker exec -it postgres dropdb --username=postgres --if-exists monta-gpt
	docker exec -it postgres createdb --username=postgres --owner=postgres monta-gpt

.PHONY: dropdb
dropdb:
	docker exec -it postgres dropdb --username=postgres  monta-gpt

.PHONY: dc-up
dc-up:
	docker compose up --build

.PHONY: dc-down
dc-down:
	docker compose down

.PHONY: update-requirements
update-requirements:
	cd backend && rm -f requirements.txt && pip freeze > requirements.txt
