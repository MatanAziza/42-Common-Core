FROM debian:12.13

RUN apt update -y && apt upgrade -y && \
	apt-get install mariadb-server -y

COPY conf/50-server.cnf /etc/mysql/mariadb.conf.d/50-server.cnf

COPY tools/script.sh /mariadb.sh
RUN chmod u+x /mariadb.sh
RUN /mariadb.sh
