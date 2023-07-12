# <span style="color:orange">Local Development - [Oddersea](https://oddersea.com/)</span>
![Local Development](https://bitbucket.org/customateteam/local-development/raw/6926ae46580411d4117a3b5d897a7686cb06179d/odd_6.jpg)

## <span style="color:orange">Background</span>
This repo has been put together to simplify the process of getting our application installed and working on your local machine. 

***
***


## API documentation
You can find our API documentation here:

* [API documentation](https://frontendservice.docs.apiary.io/)


***
***
## <span style="color:orange">Prerequisites<span>
* [Docker & Docker Compose](https://docs.docker.com/desktop/) (<span style="color:orange">Local Development with Docker</span> only)
* Access to Oddersea's VPN (on staging)

***
***


## Repositories:
1. Navigate to your development directory and open a bash terminal.
2. Clone the development repository:
    ```
    git clone https://github.com/Oddersea/local-dev-framework.git .
    mkdir api && cd api
    git clone --branch develop https://github.com/Oddersea/backend-api.git .
    cd ..
    mkdir spa && cd spa
    git clone --branch develop https://github.com/Oddersea/frontend-spa.git .
    cd ..
    mkdir main-site && cd main-site
    git clone --branch develop https://github.com/Oddersea/main-site.git .
    cd ..
    ```

***
***


## Local directory setup
We will need to add a directories to our project to store logs.

```
echo > .env
cd api
cp env_template .env
cd /app/backend
mkdir media
mkdir logs && cd logs
echo > celery.log
echo > app.log
cd ../../..
cd main-site
cp env_template .env
cd app/backend
mkdir media
mkdir logs && cd logs
echo > celery.log
echo > app.log
cd ../../..
cd spa
cp env_template .env
cd ..
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

* Our app UI is accessible at [http://localhost:3000](http://localhost:3000)
* The REST API's should now be available at [http://localhost:8000/](http://localhost:8000/)
* Flower is accessible at [http://localhost:5555](http://localhost:5555)
* Your database instances are accessible at [http://localhost:5050](http://localhost:5050)
* Main site is running on [http://localhost:8080](http://localhost:8080)

***
*** 

### Helpful Docker stuff
You can run Django commands as normal by accessing the Django `api` image.
The following example display all files in the container

```
docker exec -it api bash
ls
exit
```

The following example will rebuild one container (and its dependencies)
```
docker-compose -f up -d --no-deps --build payment-api
```


***
***