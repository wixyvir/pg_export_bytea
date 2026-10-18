#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE TABLE test(filename text, content bytea);
	INSERT INTO test VALUES('fichier.jpg', pg_read_binary_file('/docker-entrypoint-initdb.d/fichier.jpg')::bytea);
	INSERT INTO test VALUES('GPU.sh', pg_read_binary_file('/docker-entrypoint-initdb.d/GPU.sh')::bytea);
EOSQL
