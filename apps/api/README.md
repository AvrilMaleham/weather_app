docker-compose up -d
docker exec -it api-db-1 psql -U postgres -d weatherdb
