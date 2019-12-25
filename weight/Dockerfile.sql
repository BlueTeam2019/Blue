FROM mysql/mysql-server:5.7
COPY create-db.sql /docker-entrypoint-initdb.d
