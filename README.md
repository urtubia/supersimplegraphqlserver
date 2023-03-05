# Super Simple Graphql Server (with strawberry-graphql and SQLAlchemy)

This repository contains a simple GraphQL server built using [Strawberry GraphQL](https://strawberry.rocks/) and [SQLAlchemy](https://www.sqlalchemy.org/). 

For a client that uses this server, see [supersimplereactgraphqlclient](https://github.com/urtubia/supersimplereactgraphqlclient)

## Requirements

- Python 3.10+

### Running it locally

Setup the virtual environment and install the dependencies:
```
make setup-local-dev
```

Run the server:
```
make start
```

### Running it with docker

```
make start-docker-build
```

## Graphqli
After starting the server, head over to http://localhost:8000/graphql which will show you the available queries and mutations.



