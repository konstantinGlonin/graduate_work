
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


start:
	docker-compose -f docker-compose.yaml up -d
	docker-compose -f movies/docker-compose.yml up -d
	docker-compose -f ugc/docker-compose.yml up -d
	docker-compose -f etl/docker-compose.yml up -d


stop:
	docker-compose -f etl/docker-compose.yml stop
	docker-compose -f movies/docker-compose.yml stop
	docker-compose -f ugc/docker-compose.yml stop
	docker-compose -f docker-compose.yaml stop


down:
	docker-compose -f etl/docker-compose.yml down  --remove-orphans
	docker-compose -f movies/docker-compose.yml down --remove-orphans
	docker-compose -f ugc/docker-compose.yml down --remove-orphans
	docker-compose -f docker-compose.yaml down  --remove-orphans

ps:
	docker ps