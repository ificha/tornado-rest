
class HiveMetastoreAdapter(object):

    def is_table_exist(self, table_name):
        return True

    def are_tables_exists(self, table_names):
        return True;

    def get_table_meta(self, table_name):
        return { 'full_name': 'vcf.samples', 'location': 's3://url' }