import sqlite3

import config


class BaseModel:
    _conn = sqlite3.connect(config.DB_NAME)
