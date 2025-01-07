import os
import pandas as  pd
import psycopg2 as pg
from psycopg2  import sql
from psycopg2.extras import RealDictCursor

class PostgreSQLConnector:
    
    def ___init__(self, host, database, user, password, port=5432):
        self.host = host
        self.database = database
        self.user = user
        self.pw = password
        self.port = port
        self.__connection = None
        self.cursor = None
        self.__path_db_sctructure = "D:\\Hungtv7\\Personal_Fin\\"

    def connect(self):
        try :
            self.connection = pg.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.pw,
                port=self.port
            )
            self.cursor = self.__connection.cursor(cursor_factory=RealDictCursor)
            print("Connection established")
        except Exception as e:
            print(f"Failed to connect to database: {e}")

    def execute_query(self, query, params=None):

        if self.__connection is None:
            print("No connection to database")
            return
        try:
            self.cursor.execute(query, params)
            self.__connection.commit()
        except Exception as e:
            self.__connection.rollback()
            print(f"Failed to execute query: {e} ")
    
    def fectch_one(self):
        """Fetches a single row from last execute query"""
        if self.cursor is None:
            print("No query executed recently")
            return None
        return self.cursor.fetchone()
    
    def fetch_all(self):
        """Fetches all rows from last executed query"""
        if self.cursor  is None:
            print("No query executed recently")
            return None
        return self.cursor.fetchall()
    
    def create_table(self, table_name, columns):
        """
        Create a table in  the database
        Args:
            table_name: Name of the table to create
            columns: Dictionary where keys are column's name and value are SQL data
        """
        if self.__connection is None:
            print("No connections to any database")
            return
        try :
            with open(os.path.join(self.__path_db_sctructure, f"{table_name}.sql"), 'r') as f:
                sql_script = f.read()
            self.cursor.execute(sql_script)
            self.__connection.commit()
            #Check table existsence
        except Exception as e:
            self.__connection.rollback()
            print(f"Failed to create table {table_name}: {e}")
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.__connection:
            self.__connection.close()
            print("Connection closed.")