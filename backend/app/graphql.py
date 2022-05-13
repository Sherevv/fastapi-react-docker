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


class WhereParser:

    def __init__(self,
                 model: any,
                 query: SelectOfScalar,
                 sort: str | None = None,
                 start: int | None = None,
                 limit: int | None = None,
                 where: Optional[JSON] = None):
        self.model = model
        self.query = query
        self.sort = sort
        self.start = start
        self.limit = limit
        self.where = where

    @classmethod
    def set_id_to_uuid(cls, ids):
        if isinstance(ids, str):
            return UUID(ids)
        if isinstance(ids, list):
            return [UUID(id) for id in ids]

    def get_clause(self, field: str, _: str, operator: str, value: str | list | None):
        """
        Parse single clause
        :param field: column name
        :param _: delimiter
        :param operator: operator name
        :param value: operator value
        :return: SQLModel clause
        """
        expression = None

        if field == 'id' or field.endswith('.id') or field.endswith('_id'):
            value = WhereParser.set_id_to_uuid(value)

        if not _:
            expression = getattr(self.model, operator) == value
        elif operator == 'eq':
            expression = getattr(self.model, field) == value
        elif operator == 'ne':
            expression = getattr(self.model, field) != value
        elif operator == 'lt':
            expression = getattr(self.model, field) < value
        elif operator == 'gt':
            expression = getattr(self.model, field) > value
        elif operator == 'lte':
            expression = getattr(self.model, field) <= value
        elif operator == 'gte':
            expression = getattr(self.model, field) >= value
        elif operator == 'in':
            expression = getattr(self.model, field).in_(value)
        elif operator == 'nin':
            expression = getattr(self.model, field).not_in(value)
        elif operator == 'contains':
            expression = getattr(self.model, field).ilike(f'%{value}%')
        elif operator == 'ncontains':
            expression = getattr(self.model, field).not_ilike(f'%{value}%')
        elif operator == 'containss':
            expression = getattr(self.model, field).like(f'%{value}%')
        elif operator == 'ncontainss':
            expression = getattr(self.model, field).not_like(f'%{value}%')
        elif operator == 'between':
            expression = getattr(self.model, field).between(*value)
        elif operator == 'nbetween':
            expression = ~getattr(self.model, field).between(*value)
        elif operator == 'null':
            expression = getattr(self.model, field).is_(None)
        elif operator == 'nnull':
            expression = getattr(self.model, field).is_not(None)
        return expression

    def parse_or(self, values: list):
        """
        Parse list of OR clauses
        :param values:
        :return: list of clauses
        """
        expressions = []
        for value in values:
            for key, val in value.items():
                field, _, operator = key.rpartition('_')
                expression = self.get_clause(field, _, operator, val)
                if expression is not None:
                    expressions.append(expression)
        return expressions

    def parse_where(self, where: dict):
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
                expressions_or = self.parse_or(value)
            else:
                expression = self.get_clause(field, _, operator, value)
                if expression is not None:
                    expressions_and.append(expression)

        return expressions_and, expressions_or

    def get_where_query(self, query: SelectOfScalar, where: dict | None) -> SelectOfScalar:
        expressions_and, expressions_or = self.parse_where(where)
        if expressions_and:
            query = query.where(*expressions_and)
        if expressions_or:
            query = query.where(or_(*expressions_or))
        return query

    def prepare_query(self) -> SelectOfScalar:

        if self.sort:  # format: 'field:order'
            field, order = self.sort.split(':')
            self.query = self.query.order_by(text(f'{field} {order}'))
        if self.start:
            self.query = self.query.offset(self.start)
        if self.limit:
            self.query = self.query.limit(self.limit)
        if self.where:
            self.query = self.get_where_query(self.query, self.where)

        return self.query
