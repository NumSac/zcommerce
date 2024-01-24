

## up: starts all containers in the background without forcing build
up:
	@echo "Starting docker images..."
	docker compose up -d
	@echo "Docker images started!"

## down: stop docker compose
down:
	@echo "Stopping docker images"
	docker compose down
	@echo "Docker stopped!"


## build_dev: builds dev environments for django development with sqlite3
build_dev: build_django
	@echo "Building dev environment..."





build_django:
	@echo "Building Django for dev"
	cd ecommerce && python