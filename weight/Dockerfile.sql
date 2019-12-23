FROM mysql/mysql-server:5.7
COPY create-db.sql /docker-entrypoint-initdb.d
COPY ./init.sql /docker-entrypoint-initdb.d/
# WORKDIR /grantprivscript
COPY initdb.sh /
RUN chmod +x /initdb.sh
# CMD ["/initdb.sh"]
# ENTRYPOINT [ "/initdb.sh" ]