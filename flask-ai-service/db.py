import oracledb
from config import config

_connection = None


def get_connection():
    global _connection

    try:
        # If connection exists and is valid, reuse it
        if _connection:
            _connection.ping()
            return _connection
    except:
        _connection = None

    # Create fresh connection
    _connection = oracledb.connect(
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        dsn=f"{config.DB_HOST}:{config.DB_PORT}/{config.DB_SERVICE}"
    )

    return _connection