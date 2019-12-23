mysql -uroot -ppass < /docker-entrypoint-initdb.d/init.sql
# mysql -uroot -ppass < "GRANT ALL PRIVILEGES ON *.* TO 'web'@'%' IDENTIFIED BY 'pass';"