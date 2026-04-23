# DEV_DOC.md — Developer Documentation

## Prerequisites

The project is designed to run on a **Linux host** (Debian 12 recommended, consistent with the container base images). Make sure the following are installed before starting:

| Tool | Minimum version | Check command |
|---|---|---|
| Docker Engine | 20.x | `docker --version` |
| Docker Compose (plugin) | v2 | `docker compose version` |
| GNU Make | 3.x | `make --version` |

> Docker Desktop on macOS is not supported — the bind mount paths (`/home/maziza/data/...`) are Linux-specific.

---

## Setting up the environment from scratch

### 1 — Run the VM setup script

A convenience script at the root of the repository installs all required system dependencies and creates the data directories:

```bash
bash vm_setup.sh
```

This script performs the following steps automatically:
- Installs Docker Engine, Docker Compose plugin, and Make via `apt`
- Creates `/home/$USER/data/wordpress` and `/home/$USER/data/mariadb` (bind mount targets)
- Adds the current user to the `docker` group (avoids needing `sudo` for every Docker command)
- Appends `127.0.0.1 maziza.42.fr` to `/etc/hosts`

> After the script runs, **log out and back in** (or run `newgrp docker`) for the group change to take effect.

### 2 — Configure the `.env` file

The `srcs/` directory contains a pre-filled example at `srcs/.env.example`. Copy and edit it:

```bash
cp srcs/.env.example srcs/.env
```

The `.env` file must define the following variables:

```env
# MariaDB
SQL_DATABASE=<database_name>
SQL_USER=<db_user>
SQL_PASSWORD=<db_user_password>
SQL_ROOT_PASSWORD=<db_root_password>

# WordPress
WP_DATABASE=<same_as_SQL_DATABASE>
WP_USER=<wp_editor_username>
WP_PASSWORD=<wp_editor_password>
WP_ROOT_USER=<wp_admin_username>
WP_ROOT_PASSWORD=<wp_admin_password>
```

These values are injected at container startup — changing them requires a rebuild (see below).

> ⚠️ Never commit `srcs/.env` to version control. Ensure it is listed in `.gitignore`.

### 3 — Verify the domain resolution

The `vm_setup.sh` script already adds the host entry, but you can verify manually:

```bash
grep maziza /etc/hosts
# Expected: 127.0.0.1 maziza.42.fr
```

If it is missing, add it manually:
```bash
echo "127.0.0.1 maziza.42.fr" | sudo tee -a /etc/hosts
```

---

## Building and launching with the Makefile

The `Makefile` wraps the Docker Compose and Docker CLI commands. All commands must be run from the `Inception/` root directory.

| Command | Effect |
|---|---|
| `make` or `make build` | Builds all images and starts all containers via `docker compose up` |
| `make nginx` | Builds only the `nginx` image (`docker build`) |
| `make wordpress` | Builds only the `wordpress` image |
| `make mariadb` | Builds only the `mariadb` image |
| `make clean` | Removes the three built images (`nginx`, `wordpress`, `mariadb`) |

The Compose file is located at `srcs/docker-compose.yml` and is referenced explicitly in each Make target.

> **First-boot note:** MariaDB runs an initialization script on its first start. If it fails to become ready before WordPress connects, press `Ctrl + C` twice and re-run `make`. A `healthcheck` with 10 retries (5 s interval) is in place to mitigate this, but a second attempt is sometimes needed.

---

## Useful commands for managing containers and volumes

**Follow logs in real time for all services:**
```bash
docker compose -f srcs/docker-compose.yml logs -f
```

**Restart a single container without rebuilding:**
```bash
docker restart wordpress
docker restart nginx
docker restart mariadb
```

**Open a shell inside a running container:**
```bash
docker exec -it nginx bash
docker exec -it wordpress bash
docker exec -it mariadb bash
```

**Connect to MariaDB from inside its container:**
```bash
docker exec -it mariadb mariadb -u root -p
# Enter SQL_ROOT_PASSWORD from srcs/.env
```

**Inspect the `inception` network:**
```bash
docker network inspect inception
```

**List volumes and their mount points:**
```bash
docker volume ls
docker volume inspect inception_wordpress
docker volume inspect inception_mariadb
```

**Force a full image rebuild** (useful after modifying a Dockerfile or config file):
```bash
docker compose -f srcs/docker-compose.yml build --no-cache
make
```

---

## Container architecture and build details

### NGINX (`srcs/requirements/nginx/`)

- **Base image:** `debian:12.13`
- **Listens on:** port `443` (the only port mapped to the host)
- **TLS:** A self-signed certificate is generated at build time with `openssl req -x509` and stored inside the image at `/etc/nginx/ssl/`. Protocols restricted to **TLSv1.2** and **TLSv1.3**.
- **PHP routing:** All `.php` requests are forwarded to `wordpress:9000` via FastCGI (`fastcgi_pass wordpress:9000`).
- **Config file:** `srcs/requirements/nginx/conf/nginx.conf` — copied into the image at build time.

### WordPress (`srcs/requirements/wordpress/`)

- **Base image:** `debian:12.13`
- **Runtime:** PHP-FPM 8.2, listens on TCP port `9000`
- **WordPress version:** 6.9.4 (French locale), downloaded from `fr.wordpress.org` during the image build
- **WP-CLI:** Installed at `/usr/local/bin/wp` and used in the entrypoint script to configure and install WordPress non-interactively
- **Entrypoint:** `tools/wp_setup.sh` — waits for MariaDB to be ready, creates `wp-config.php` if absent, installs WordPress if not already installed, then starts `php-fpm8.2 -F`
- **PHP-FPM pool config:** `srcs/requirements/wordpress/conf/www.conf` — runs as `www-data`, `pm = dynamic`, max 5 children
- **Shared volume:** Mounts the `wordpress` volume at `/var/www/wordpress`, shared with the NGINX container so NGINX can serve static files directly

### MariaDB (`srcs/requirements/mariadb/`)

- **Base image:** `debian:12.13`
- **Listens on:** port `3306`, bound to all interfaces (`bind_address=*`) within the Docker network
- **Entrypoint:** `tools/setup.sh` — starts `mysqld_safe --skip-grant-tables` temporarily, creates the database and user, sets the root password, stops the temporary instance, then starts `mysqld_safe` normally
- **Config file:** `srcs/requirements/mariadb/conf/50-server.cnf` — sets `datadir`, socket, port, and user
- **Health check:** `mariadb-admin ping` with up to 10 retries (5 s interval), used by Compose to gate the WordPress startup

---

## Data persistence — where it lives and how it works

Both volumes are configured as **bind mounts** using the Docker `local` driver with `type: none` and `o: bind`. This means Docker does not manage the storage internally — data is written directly to the host filesystem.

| Volume name | Host path | Mounted in |
|---|---|---|
| `wordpress` | `/home/maziza/data/wordpress` | `nginx` and `wordpress` containers at `/var/www/wordpress` |
| `mariadb` | `/home/maziza/data/mariadb` | `mariadb` container at `/var/lib/mysql` |

**These directories are created by `vm_setup.sh`** and must exist before `make` is run, otherwise Docker Compose will fail with a bind mount error.

Data in these directories **persists across container restarts and image rebuilds** as long as the host directories are not deleted. Running `make clean` only removes the Docker images — it does not touch the data.

To inspect the WordPress files directly from the host:
```bash
ls /home/maziza/data/wordpress/
```

To inspect the MariaDB data directory:
```bash
ls /home/maziza/data/mariadb/
```
