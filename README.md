# Dockerized FastAPI + RedisQueue application

### Run app

`docker-compose up --build`

#### Go to 127.0.0.1:5057 (main app)

#### Go to 127.0.0.1:5057/subapi (sub app)

### Run tests

Before running tests, you need to comment line #24 in main.py:

`app.mount('/static', StaticFiles(directory='static'), name='static')`

For some weird reasons, it throws an error when running the tests

Also, make sure the docker container is running (the command above)

`docker-compose exec web python -m pytest`

OR

`docker-compose exec web python run_tests.py`
