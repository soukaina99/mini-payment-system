Backend DRF for mini payment system

## Usage

Running as docker containers

```bash
docker-compose build
docker-compose up -d
```

## Access the admin panel

### Create a super user:
```
docker-compose exec web bash
python manage.py createsuperuser
```

login using this link: http://localhost:8000/admin/login/


## Tests

```bash
$ docker-compose run --rm web pytest
```

or, to run a single test:

```bash
docker-compose run --rm web pytest -q -s tests/payment/test_api.py
```
to see test coverage report:

```bash
docker-compose exec web bash
py.test tests/ --cov='.'

```

# **API endpoints[Swagger]:**

 http://localhost:8000/docs


