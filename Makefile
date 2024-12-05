DATABASE_URL=postgresql://postgres:password@localhost:5432/monta-gpt?sslmode=disable

.PHONY: createdb
createdb:
	docker exec -it postgres dropdb --username=postgres --if-exists monta-gpt
	docker exec -it postgres createdb --username=postgres --owner=postgres monta-gpt

.PHONY: dropdb
dropdb:
	docker exec -it postgres dropdb --username=postgres  monta-gpt

.PHONY: create-migration
create-migration:
	docker exec -it migration alembic revision -m $(name)

.PHONY: migrationup
migrationup:
	docker exec -it migration alembic upgrade head

.PHONY: migrationup-count
migrationup-count:
	docker exec -it migration alembic upgrade +${count}

.PHONY: migrationdown
migrationdown:
	docker exec -it migration alembic downgrade base

.PHONY: migrationdown-count
migrationdown-count:
	cd ./backend/app/db && alembic downgrade -${count}

.PHONY: dc-build-and-run
dc-build-and-run:
	docker compose up --build

.PHONY: dc-run
dc-run:
	docker compose up

.PHONY: dc-down
dc-down:
	docker compose down

# MEMO: 依存関係の管理は一旦は以下のコマンドを実行することで管理すると良い
# pip freeze | grep -E '^(fastapi|uvicorn|langchain|openai)=='
# -E 以降にほしいライブラリの名前を入れるだけで現在freezeに入っているライブラリから抽出してくれます
.PHONY: update-requirements
update-requirements:
	cd backend && rm -f requirements.txt && pip freeze > requirements.txt
