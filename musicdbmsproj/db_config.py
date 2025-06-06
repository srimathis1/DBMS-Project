import os
import oracledb

def get_connection():
    try:
        # Get credentials from environment variables (Render-safe)
        username = os.environ.get("SYSTEM")
        password = os.environ.get("system")
        dsn = os.environ.get("localhost:1522/orcl")  # Format: host:port/service_name

        # Connect
        conn = oracledb.connect(user=username, password=password, dsn=dsn)
        return conn
    except oracledb.DatabaseError as e:
        print("Oracle connection error:", e)
        return None
