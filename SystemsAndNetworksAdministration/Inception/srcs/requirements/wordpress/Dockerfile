FROM debian:12.13

# MODIF 1 : corriger backslashes + ajouter -y pour tous
RUN apt-get update && apt-get install -y \
    wget netcat-openbsd \
    php8.2 php8.2-fpm php8.2-mysql php8.2-curl php8.2-gd php8.2-mbstring \
    php8.2-xml php8.2-zip \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# MODIF 2 : corriger chown www-data + créer /run/php
RUN mkdir -p /var/www/wordpress /run/php && \
    wget https://fr.wordpress.org/wordpress-6.9.4-fr_FR.tar.gz -P /tmp && \
    cd /var/www && tar -xzf /tmp/wordpress-6.9.4-fr_FR.tar.gz && \
    rm -rf /tmp/wordpress-6.9.4-fr_FR.tar.gz /var/www/wordpress/wp-config-sample.php && \
    chown -R www-data:www-data /var/www/wordpress /run/php

# MODIF 3 : forcer listen = 9000 TCP dans pool
RUN echo "listen = 9000" > /etc/php/8.2/fpm/pool.d/www.conf

COPY conf/php-fpm.conf /etc/php/8.2/fpm/php-fpm.conf
COPY conf/www.conf /etc/php/8.2/fpm/pool.d/www.conf

RUN wget https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -O /usr/local/bin/wp && \
    chmod +x /usr/local/bin/wp

COPY tools/wp_setup.sh /wp_setup.sh
RUN chmod +x /wp_setup.sh
ENTRYPOINT ["/wp_setup.sh"]
