.PHONY: dc-up
dc-up:
	docker compose up --build

.PHONY: dc-down
dc-down:
	docker compose down