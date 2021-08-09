# Dockerized FastAPI + RedisQueue application

### Run app

`docker-compose up --build`

### Run tests

`docker-compose exec web python -m pytest -k "test_mock_task"`
