# <span style="color:orange">Udemy Django Course Framework</span>

## <span style="color:orange">Background</span>
This repo has been put together as a starting point for a Udemy Django course. 

***
***
## <span style="color:orange">Prerequisites<span>
* [Docker & Docker Compose](https://docs.docker.com/desktop/) (<span style="color:orange">Local Development with Docker</span>)

***
***


## Repositories:
1. Navigate to your development directory and open a bash terminal.
2. Clone the development repository:
    ```
    git clone https://github.com/bobby-didcoding/udemy-django-course.git .
    ```

***
***


## Local directory setup
We will need to add a directories to our project to store logs.

```
#Unix and MacOS
cp env_template .env

#windows
copy env_template .env
```

***
***

## Build Docker images:

Use the following command to build the docker images:
> Make sure Docker is running on your machine!

1. Open a terminal on your machine.

2. Optional step! Prune docker.
    You may want to prune un-used Docker images and containers.
    ```
    docker system prune
    ```

3. Fire up a dev Docker container.
    > Note: you may want to prune un used Docker images and containers
    ```
    docker-compose up -d --build
    ```
***
***

### Finished
You should now be up and running!
>Note: Open an incognito browser when testing your project (Ctrl + Shift + N)

* Main site is running on [http://localhost:8000](http://localhost:8000)

***
*** 

### Helpful Docker stuff
You can run Django commands as normal by accessing the Django `app` image.
The following example display all files in the container

```
docker exec -it app bash
ls
exit
```

The following example will rebuild one container (and its dependencies)
```
docker-compose -f up -d --no-deps --build app
```

***
***

```
Create ssh key
ssh-keygen

add it to root authorized_key

add cert.pem and key.pem to etc/ssl/certs

update and upgrade packages

sudo apt update
sudo apt upgrade

add new user

adduser **username**
usermod -aG sudo **username**
gpasswd -a **username** sudo

install required packages
sudo apt install python3-pip python3-dev libpq-dev postgresql-client

install docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

#We now need to apply executable permissions to the binary file. You can do this by using the following command:
sudo chmod +x /usr/local/bin/docker-compose

Create a symbolic link to /usr/bin path. You can do this by using the following command:
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```