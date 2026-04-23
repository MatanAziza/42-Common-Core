*This activity has been created as part of the 42 curriculum by maziza*

# Inception

## Description

Inception is a 42 SysAdmin Project. It consists of learning how Docker works and \
how to setup a small infrastructure of different services linked together \
(in this project, a website linked to a database).

In this project, many choices were made between two or more options:

Firstly, using dockers instead of multiples threads on a virtual machine. This allow to \
separate tasks and treat problems separately if needed, but also to save work environment for each docker when you turn them off.

Then comes the question of security, which grasps 2 choices:
How to store secrets, and how to connect all these dockers.

The choice between the Host network and the Docker network is easy when you understand this:\
using the Host network means all containers and the host will share the same ip range, leading\
to easier breach/security problems.

That's why you use the Docker network kinda like a intermediate between the containers and the host,\
to prevent direct communication between them. In our project, the host only communicates with\
the NGINX container, and can't with the MariaDB or the Wordpress ones: \
they communicate with NGINX only.

As for the secrets you hold (.env file or secrets folder for Docker), \
secrets are stored in text files, and are a more secure way of running\
dockers without them being exposed by some accessing a docker while its running.\
As for .env, they can be more easily accessed, but for learning purpose and because\
the secrets aren't that secret right now, I used .env.

Finally, the difference of use between docker volumes and bind mounts. Basically,\
docker volume manage itself the data stored by containers, whereas bind mount\
are more admin-managed storage. This is the one I chose to do.

## Instructions

The project needs many components to work:

- A virtual machine to setup all dockers and data hold since we need \
 full access/rights to manipulate and install softwares
- Docker
- Preset folders to store data (Wordpress, MariaDB)
- a .env file in the srcs folder, that possesses these secrets:

```
SQL_DATABASE
SQL_USER
SQL_PASSWORD
SQL_ROOT_PASSWORD

WP_DATABASE
WP_USER
WP_PASSWORD
WP_ROOT_USER
WP_ROOT_PASSWORD
```

First, create a Virtual Machine (all instructions will help to install needed \
 softwares on Debian).

- Run the **vm_setup.sh** script to setup Docker, database folders, etc.
- Run the command `echo "127.0.0.1 maziza.42.fr" | sudo tee -a /etc/hosts`
- Go in the Inception folder and run the command `make`.
- If the database fails on the first try, do <kbd>Ctrl + C</kbd> twice then redo the `make`.

- Once the dockers are running, open a browser and enter the address written in the vm_setup.sh file.

Voilà !!

## Resources

AI (Perplexity, Claude, ...) Was used to understand basic docker concepts,\
find sources to learn about such concepts and make the DEV and USER DOC markdown. Ai was also used to understand errors, \
in addition to StackOverflow forum posts.

[Docker secrets understanding](https://docs.docker.com/compose/how-tos/use-secrets/)
[How to dockerise Wordpress](https://www.docker.com/blog/how-to-dockerize-wordpress/)
[NGINX image building](https://www.datacamp.com/tutorial/nginx-docker)
[NGINX SSL config](https://ubiq.co/tech-blog/nginx-ssl-configuration-step-step-details/)
