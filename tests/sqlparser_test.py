
from unittest import TestCase
from apps.server.sql_validator import SqlValidator

def validateTable(self, table, namespace, name, alias):
    self.assertEqual(table['namespace'], namespace)
    self.assertEqual(table['name'], name)
    self.assertEqual(table['alias'], alias)


class SqlParserTest(TestCase):

    # def test_sql1(self):
    #     validator = SqlValidator('select * from vcf.samples')
    #     tables = validator.getTables()
    #     validateTable(self, tables[0], 'vcf', 'samples', None)

    def test_sql2(self):
        validator = SqlValidator('select a.c0, a.c1, b.c0, b.c1 from table_a as a, table_b as b where a.c0=b.c0')
        tables = validator.extract_tables()
