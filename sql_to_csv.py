import pandas as pd
import psycopg2 
import os
import sqlalchemy as sa
from sqlalchemy.pool import NullPool
from config import config

# https://www.postgresqltutorial.com/postgresql-python/connect/
def connect():
    query = {}
    query['test'] = "<special query for 'test' table>"
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        url = sa.engine.URL.create("postgresql+psycopg2", **params)

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        db = sa.create_engine(url, poolclass=NullPool)
        conn = db.connect()

        sql_query = pd.read_sql_query(''' 
                                      SELECT table_name FROM information_schema.columns WHERE column_name = '<desired id>'
                                      '''
                                    ,conn)
        df = pd.DataFrame(sql_query)

        for _, row in df.iterrows():
            table = row['table_name']
            print("Reading table " + table + "...")
            default = "SELECT * FROM <db>." + table
            sql_query = pd.read_sql_query(query.get(table, default), conn)
            df = pd.DataFrame(sql_query)
            # Set path if not $HOME
            path = os.environ['HOME']
            df = df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
            df.to_csv(path + '/' + table + '_data.csv', index = False)
            print("Data written to " + path + '/' + table + '_data.csv')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.close()
        print('Database connection closed.')


if __name__ == '__main__':
    connect()
