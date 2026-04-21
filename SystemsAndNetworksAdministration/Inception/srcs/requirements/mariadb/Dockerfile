FROM debian:12.13

RUN apt update -y && apt install mariadb-server mariadb-client galera-4 -y

COPY conf/50-server.cnf /etc/mysql/mariadb.conf.d/50-server.cnf

COPY tools/setup.sh /setup.sh
RUN chmod u+x /setup.sh
ENTRYPOINT ["/setup.sh"]
