# db_config.py
import oracledb

# Oracle connection details
username = "SYSTEM"
password = "SRIMATHI"
dsn = "localhost:1522/orcl"

# Create and return a connection
def get_connection():
    try:
        connection = oracledb.connect(user=username, password=password, dsn=dsn)
        return connection
    except oracledb.DatabaseError as e:
        print("Oracle connection error:", e)
        return None
