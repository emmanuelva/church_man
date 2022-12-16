# Prayer management app

## Developer

### Linting

To execute Flake 8 in a docker container, execute:

```shell
docker-compose run --rm app sh -c "flake8"
```

### Tests

To execute all tests, run:

```shell
docker-compose run --rm app sh -c "python manage.py test"
```
