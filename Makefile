.PHONY: dc-up
dc-up:
	docker compose up --build

.PHONY: dc-down
dc-down:
	docker compose down

.PHONY: update-requirements
update-requirements:
	cd backend && rm -f requirements.txt && pip freeze > requirements.txt
