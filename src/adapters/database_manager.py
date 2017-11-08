from orator import DatabaseManager, Schema
import os
config = {
    'mysql': {
        'driver': 'mysql',
        'host': os.environ.get('DATABASE_HOST', 'localhost'),
        'database': os.environ.get('DATABASE_NAME', 'elastest'),
        'user': os.environ.get('DATABASE_USER', 'root'),
        'password': os.environ.get('DATABASE_PASSWORD', ''),
        'prefix': '',
        'port': os.environ.get('DATABASE_PORT', 3306)
    }
}
db = DatabaseManager(config)
schema = Schema(db)
