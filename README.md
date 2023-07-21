# <span style="color:orange">Udemy Django Course Framework - lecture 3</span>

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