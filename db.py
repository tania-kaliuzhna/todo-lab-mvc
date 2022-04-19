import sqlite3

import config

class DbConnector:
    _conn = sqlite3.connect(config.DB_NAME)
    schema = {
        config.TASK_LIST_TABLE: ["title"],
        config.TASK_TABLE: ["description", "done", f"{config.TASK_LIST_TABLE}_id"]
    }

    @staticmethod
    def get_typed(value):
        if isinstance(value, bool):
            return str(int(value))
        return str(value) if (isinstance(value, int) or isinstance(value, float)) else f"'{value}'"

    @classmethod
    def create_entity(cls, table_name, *props):
        typed_props = [cls.get_typed(prop) for prop in props]
        props_string = ",".join(typed_props)
        query = """
        INSERT INTO {table_name} ({schema}) VALUES ({props_string})
        """.format(props_string=props_string,
        table_name=table_name,
        schema=",".join(cls.schema[table_name]))
        # print(query)
        cls._conn.execute(query)
        cls._conn.commit()

    @classmethod
    def get_entities(cls, table_name, **props):
        props_string = " WHERE " + " AND ".join([f"{key}={cls.get_typed(value)}" for key,value in props.items()]) if props else ""
        query = """
        SELECT * FROM {table_name} {props_string}
        """.format(props_string=props_string, table_name=table_name)
        return list(cls._conn.execute(query))

    @classmethod
    def update_entities(cls, table_name, old_props, new_props):
        old_props_string = " AND ".join([f"{key}={cls.get_typed(value)}" for key,value in old_props.items()])
        new_props_string = ", ".join([f"{key}={cls.get_typed(value)}" for key,value in new_props.items()]) 
        query = """
        UPDATE {table_name} SET {new_props_string} WHERE {old_props_string}
        """.format(new_props_string=new_props_string, old_props_string=old_props_string, table_name=table_name)
        # print(query)
        cls._conn.execute(query)
        cls._conn.commit()
        
    @classmethod
    def delete_entities(cls, table_name, **props):
        props_string = " WHERE " + " AND ".join([f"{key}={cls.get_typed(value)}" for key,value in props.items()]) if props else ""
        query = """
        DELETE FROM {table_name} {props_string}
        """.format(props_string=props_string, table_name=table_name)
        # print(query)
        cls._conn.execute(query)
        cls._conn.commit()
        