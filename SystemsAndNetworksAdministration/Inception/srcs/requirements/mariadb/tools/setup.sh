#!/bin/bash
set -e

# Nettoyer anciens processus
pkill -f mysqld || true
sleep 2

# Démarrer temporairement
mysqld_safe --skip-grant-tables &
MYSQL_PID=$!
sleep 10

# Setup
mysql <<EOF
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS \`${SQL_DATABASE}\`;
CREATE USER IF NOT EXISTS '${SQL_USER}'@'%' IDENTIFIED BY '${SQL_PASSWORD}';
GRANT ALL PRIVILEGES ON \`${SQL_DATABASE}\`.* TO '${SQL_USER}'@'%';
ALTER USER 'root'@'localhost' IDENTIFIED BY '${SQL_ROOT_PASSWORD}';
FLUSH PRIVILEGES;
EOF

kill -TERM $MYSQL_PID
wait $MYSQL_PID
sleep 3

exec mysqld_safe
