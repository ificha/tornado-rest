
# one 

## two 


### start postgres docker container

``` bash
docker run --name postgres-ccm -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -d --net=host postgres
```

### celery redis 

``` bash
docker run --name redis-ccm -d --net=host redis
```

### cache redis 

``` bash
docker run --name redis-cache -d -p 6380:6379 redis
```


### start celery worker

``` bash
.tox/py27/bin/celery worker -A apps.worker.tasks
```

### start python server

``` bash
.tox/py27/bin/python -m apps.server.ccm
```

