containers: nginx mariadb wordpress

build:
	docker compose -f srcs/docker-compose.yml up

nginx:
	docker build -t nginx srcs/requirements/nginx

mariadb:
	docker build -t mariadb srcs/requirements/mariadb

wordpress:
	docker build -t wordpress srcs/requirements/wordpress

clear:
	docker image ls --filter=reference='*mariadb*'\
					--filter=reference='*nginx*'\
					--filter=reference='*wordpress*'\
					-q | xargs docker rmi -f
