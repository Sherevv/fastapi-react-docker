from typing import Optional
from uuid import UUID

from strawberry.scalars import JSON
from sqlalchemy.sql.expression import text, or_, literal_column
from sqlmodel.sql.expression import SelectOfScalar
'''
Parsing GraphQL queries received from Refine frontend
https://refine.dev/docs/guides-and-concepts/data-provider/graphql/
https://github.com/pankod/refine/blob/master/packages/graphql/src/index.ts
'''


def set_id_to_uuid(ids):
    if isinstance(ids, str):
        return UUID(ids)
    if isinstance(ids, list):
        return [UUID(id) for id in ids]


def get_clause(field: str, _: str, operator: str, value: str | list | None):
    """
    Parse single clause
    :param field: column name
    :param _: delimiter
    :param operator: operator name
    :param value: operator value
    :return: SQLModel clause
    """
    expression = None

    if field == 'id' or field.endswith('_id'):
        value = set_id_to_uuid(value)

    if not _:
        expression = literal_column(operator) == value
    elif operator == 'eq':
        expression = literal_column(field) == value
    elif operator == 'ne':
        expression = literal_column(field) != value
    elif operator == 'lt':
        expression = literal_column(field) < value
    elif operator == 'gt':
        expression = literal_column(field) > value
    elif operator == 'lte':
        expression = literal_column(field) <= value
    elif operator == 'gte':
        expression = literal_column(field) >= value
    elif operator == 'in':
        expression = literal_column(field).in_(value)
    elif operator == 'nin':
        expression = literal_column(field).not_in(value)
    elif operator == 'contains':
        expression = literal_column(field).ilike(f'%{value}%')
    elif operator == 'ncontains':
        expression = literal_column(field).not_ilike(f'%{value}%')
    elif operator == 'containss':
        expression = literal_column(field).like(f'%{value}%')
    elif operator == 'ncontainss':
        expression = literal_column(field).not_like(f'%{value}%')
    elif operator == 'between':
        expression = literal_column(field).between(*value)
    elif operator == 'nbetween':
        expression = ~literal_column(field).between(*value)
    elif operator == 'null':
        expression = literal_column(field).is_(None)
    elif operator == 'nnull':
        expression = literal_column(field).is_not(None)
    return expression


def parse_or(values: list):
    """
    Parse list of OR clauses
    :param values:
    :return: list of clauses
    """
    expressions = []
    for value in values:
        for key, val in value.items():
            field, _, operator = key.rpartition('_')
            expression = get_clause(field, _, operator, val)
            if expression is not None:
                expressions.append(expression)
    return expressions


def parse_where(where: dict):
    """
    Parse WHERE clauses
    :param where:
    :return: tuple (AND, OR) clauses
    """
    expressions_and = []
    expressions_or = None
    for key, value in where.items():
        field, _, operator = key.rpartition('_')
        if operator == 'or':
            expressions_or = parse_or(value)
        else:
            expression = get_clause(field, _, operator, value)
            if expression is not None:
                expressions_and.append(expression)

    return expressions_and, expressions_or


def get_where_query(query: SelectOfScalar, where: dict | None) -> SelectOfScalar:
    expressions_and, expressions_or = parse_where(where)
    if expressions_and:
        query = query.where(*expressions_and)
    if expressions_or:
        query = query.where(or_(*expressions_or))
    return query


def prepare_query(query: SelectOfScalar,
                  sort: str | None = None,
                  start: int | None = None,
                  limit: int | None = None,
                  where: Optional[JSON] = None) -> SelectOfScalar:

    if sort:  # format: 'field:order'
        field, order = sort.split(':')
        query = query.order_by(text(f'{field} {order}'))
    if start:
        query = query.offset(start)
    if limit:
        query = query.limit(limit)
    if where:
        query = get_where_query(query, where)
    return query
