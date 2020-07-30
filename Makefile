up:
	docker-compose up -d
upb:
	docker-compose up -d --force-recreate --build
down:
	docker-compose down && docker volume prune -f
stop:
	docker-compose stop
db:
	docker exec -it healthcheck_db_1 psql -Uhealthcheck
sh:
	docker exec -it $(c) /bin/bash