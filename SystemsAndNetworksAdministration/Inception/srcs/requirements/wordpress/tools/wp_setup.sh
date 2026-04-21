#!/bin/bash
set -e

echo "=== WordPress Setup ==="

# 1. Attendre MariaDB PROPREMENT
echo "Waiting for MariaDB..."
for i in {1..30}; do
	if mysql -h mariadb -u${WP_USER} -p${WP_PASSWORD} -e "SELECT 1;" >/dev/null 2>&1; then
		echo "✓ MariaDB ready!"
		break
	fi
	echo "MariaDB not ready ($i/30), waiting..."
	sleep 2
done

# 2. Vérifier/réparer WordPress directory
cd /var/www/wordpress

if [ -f wp-config.php ]; then
	echo "✓ wp-config.php exists, skipping config creation"
else
	echo "Creating wp-config.php..."
	wp config create --allow-root \
		--dbname="${WP_DATABASE}" \
		--dbuser="${WP_USER}" \
		--dbpass="${WP_PASSWORD}" \
		--dbhost=mariadb:3306 \
		--path=/var/www/wordpress
fi

# 3. Gérer WordPress files déjà présents
if wp core is-installed --allow-root --path=/var/www/wordpress >/dev/null 2>&1; then
	echo "✓ WordPress already installed, skipping setup"
else
	echo "Installing WordPress..."
	wp core install --allow-root \
		--path=/var/www/wordpress \
		--url="https://maziza.42.fr" \
		--title="MainPage" \
		--admin_user="${WP_ROOT_USER}" \
		--admin_password="${WP_ROOT_PASSWORD}" \
		--admin_email="matan.aziza@learner.42.tech"
fi

echo "=== Setup COMPLETE ==="
exec php-fpm8.2
