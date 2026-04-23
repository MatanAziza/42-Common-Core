# USER_DOC.md — User & Administrator Documentation

## Overview of services

The Inception stack provides a self-hosted web infrastructure composed of three services, each isolated in its own Docker container:

| Container | Role | Exposed |
|---|---|---|
| **nginx** | Reverse proxy with TLS termination — sole entry point from the host | Port `443` (HTTPS) |
| **wordpress** | CMS running via PHP-FPM 8.2 — communicates with MariaDB and serves PHP to NGINX | Internal port `9000` |
| **mariadb** | Relational database storing all WordPress content | Internal port `3306` |

All containers are connected through a private bridge network named `inception`. Only NGINX is reachable from outside — MariaDB and WordPress are not directly accessible from the host.

Persistent data is stored on the host machine as **bind mounts**:

| Volume | Host path | Content |
|---|---|---|
| `wordpress` | `/home/maziza/data/wordpress` | WordPress files (themes, plugins, uploads) |
| `mariadb` | `/home/maziza/data/mariadb` | Database files |

---

## Starting and stopping the stack

All operations are driven by the `Makefile` at the root of the repository. Commands must be run from inside the `Inception/` folder.

**Start the stack** (builds images if they don't exist, then starts all containers):
```bash
make
```

> ⚠️ If MariaDB fails to start on the first attempt, press `Ctrl + C` twice to stop the stack, then run `make` again. This is a known timing issue on the very first boot.

**Remove Docker images** (stops containers and deletes the built images, data is preserved):
```bash
make clean
```

To do a full reset — delete images **and** all persistent data — run:
```bash
make clean
sudo rm -rf /home/maziza/data/wordpress/* /home/maziza/data/mariadb/*
```

Then run `make` to start fresh.

---

## Accessing the website and the administration panel

Once the stack is running, open a browser and navigate to:

| URL | Description |
|---|---|
| `https://maziza.42.fr` | Main WordPress website |
| `https://maziza.42.fr/wp-admin` | WordPress administration panel |

> **Note:** The TLS certificate is self-signed and generated at image build time. Your browser will display a security warning — this is expected. Accept the exception (e.g. "Proceed anyway") to continue.

The domain `maziza.42.fr` must resolve to `127.0.0.1` on your machine. This is configured in `/etc/hosts` and is handled automatically by the `vm_setup.sh` script. You can verify it with:
```bash
grep maziza /etc/hosts
# Expected: 127.0.0.1 maziza.42.fr
```

---

## Locating and managing credentials

All credentials are stored in the `.env` file at `srcs/.env`. This file is loaded by Docker Compose and injected into each container as environment variables at runtime.

| Variable | Description |
|---|---|
| `SQL_DATABASE` | Name of the MariaDB database |
| `SQL_USER` | MariaDB user granted access to the database |
| `SQL_PASSWORD` | Password for `SQL_USER` |
| `SQL_ROOT_PASSWORD` | MariaDB root account password |
| `WP_DATABASE` | WordPress database name (mirrors `SQL_DATABASE`) |
| `WP_USER` | WordPress regular (editor) account username |
| `WP_PASSWORD` | Password for `WP_USER` |
| `WP_ROOT_USER` | WordPress administrator account username |
| `WP_ROOT_PASSWORD` | Password for the WordPress administrator |

> ⚠️ The `.env` file contains sensitive credentials and must **never** be committed to a public repository.

To change a credential, edit `srcs/.env`, then rebuild the stack:
```bash
make clean
make
```

---

## Checking that the services are running correctly

**List all running containers:**
```bash
docker ps
```
All three containers — `nginx`, `wordpress`, `mariadb` — should appear with status `Up`.

**Check logs for a specific service:**
```bash
docker logs nginx
docker logs wordpress
docker logs mariadb
```

**Verify that the website responds:**
```bash
curl -k https://maziza.42.fr
```
The `-k` flag skips the self-signed certificate check. A successful response returns the HTML of the WordPress homepage.

**Check the database is accepting connections:**
```bash
docker exec -it mariadb mariadb-admin -u root -p status
```
Enter the `SQL_ROOT_PASSWORD` from `srcs/.env` when prompted. A healthy output shows server uptime and query statistics.

**Inspect the internal network:**
```bash
docker network inspect inception
```
This shows all containers attached to the `inception` bridge and their internal IP addresses.
