run-staging:
	docker-compose -f docker-compose-staging.yaml --env-file .env.staging up -d --build --force-recreate
stop-staging:
	docker-compose -f docker-compose-staging.yaml down -v --remove-orphans
