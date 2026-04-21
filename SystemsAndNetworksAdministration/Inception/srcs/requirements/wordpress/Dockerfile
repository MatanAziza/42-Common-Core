FROM debian:12.13

RUN apt update && apt upgrade &&\
	apt-get install -y wget &&\
	apt-get install -y netcat-openbsd &&\
	apt-get install -y php7.3\
	php-fpm\
	php-mysql\
	mariadb-client

RUN wget https://fr.wordpress.org/wordpress-6.9.4-fr_FR.tar.gz -P /var/www
RUN cd /var/www && tar -xvf wordpress-6.9.4-fr_FR.tar.gz && rm wordpress-6.9.4-fr_FR.tar.gz
RUN chown -R root:root /var/www/wordpress

COPY conf/php-fpm.conf /etc/php/8.2/fpm/php-fpm.conf

RUN wget https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -P /usr/local/bin
RUN cd /usr/local/bin && chmod +x wp-cli.phar && mv wp-cli.phar wp

COPY tools/wp_setup.sh /wp_setup.sh
RUN chmod +x /wp_setup.sh
ENTRYPOINT ["/wp_setup.sh"]
