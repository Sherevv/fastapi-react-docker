# Full stack demo app

Database:
- [PostgreSQL](https://www.postgresql.org) database (with [asyncpg](https://magicstack.github.io/asyncpg/current/)) 
- [pgAdmin](https://www.pgadmin.org) administration interface

Backend:
- [Python](https://www.python.org/) 3.10
- [Uvicorn](https://www.uvicorn.org) ASGI web server,
- [FastAPI](https://fastapi.tiangolo.com) web framework
- [SQLModel](https://sqlmodel.tiangolo.com) - an ORM, based on [SQLAlchemy](https://www.sqlalchemy.org) 
  and [Pydantic](https://pydantic-docs.helpmanual.io)
- [Strawberry](https://strawberry.rocks) for [GraphQL](https://graphql.org)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) for migrations

Frontend:
- [Nginx](https://nginx.org) web server
- [React](https://reactjs.org) - a js library for building user interfaces 
- [Refine](https://refine.dev) react CRUD framework
- [Ant Design](https://ant.design) UI

Tools: 
- [Docker](https://www.docker.com) and [docker-compose](https://docs.docker.com/compose/)
- [Makefile](https://www.gnu.org/software/make/manual/make.html) for shortcuts


## DB prepare
FastAPI doesn't create db tables on start, use alembic migrations for it.

```bash
make migrations m="migration message" # create migrations
make migrate # apply migrations to db
make downgrade # downgrade last migration
```

## Resources
1. article: [FastAPI with Async SQLAlchemy, SQLModel, and Alembic](https://testdriven.io/blog/fastapi-sqlmodel/)
2. github: [FastAPI, Strawberry](https://github.com/rodrigoney/fastapi-strawberry-graphql)
