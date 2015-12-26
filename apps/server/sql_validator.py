

import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

class SqlValidator():

    def __init__(self, sql):
        self.sql = sql
        self.parsed = sqlparse.parse(sql)[0]

    def is_valid(self):
        return True

    def get_tables(self):
        return [
            { 'name': 'table1', 'namespace': 'vcf', 'alias': None }
        ]