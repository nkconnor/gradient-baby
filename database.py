import MySQLdb, json
from nmi_mysql import nmi_mysql

class Query:
    def __init__(self, query, params=None, schema=None):
        """

        :param query: Query string with formats
        :type query: String

        :param params: Escape params
        :type params: Dict

        :param schema: Column schema
        :type schema:
        """
        self.query = query
        self.params = params
        self.schema = schema

class MySQLConnection:

    def __init__(self, host, port, username, password, database):
        conf = {
            'host': host,
            'user': username,
            'password': password,
            'db': database,
            'port': port,
            'max_pool_size': 20  # optional, default is 10
        }

        self.db = nmi_mysql.DB(conf)

    def execute(self, query):
        rows = self.execute_raw(query.query, query.params)
        if query.schema is None: return rows
        self._apply_schema(rows, query)
        return rows

    def execute_raw(self, query, params):
        return self.db.query(query, params)
        ##results = []
        ##connection = MySQLdb.connect(host=self.host, port=self.port, user=self.username, password=self.password, database=self.database, connect_timeout=3)
        ##try:
        ##    with connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        ##        cursor.execute(query, params)
        ##        connection.commit()
        ##        results = cursor.fetchall()
        ##finally:
        ##    connection.close()
        ##    return results

    def _apply_schema(self, rows, query):
        for row in rows:
            for key, _type in query.schema.items():
                if _type == "JSON":
                    try:
                        row[key] = json.loads(row[key])
                    except:
                        row[key] = None



DB = MySQLConnection(
    host="localhost",
    port=3306,
    username="root",
    password="****",
    database="research"
)