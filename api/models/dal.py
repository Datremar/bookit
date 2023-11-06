import config
from typing import List, Dict, Any

class DAL:
    __tablename__ = None

    @classmethod
    def insert(cls, **kwargs) -> int:
        conn = config.get_db()
        cursor = config.get_db_cursor()

        # Extracting the attributes and values provided
        attributes = list(kwargs.keys())
        values = list(kwargs.values())

        # Formulating the SQL query
        placeholders = ', '.join(['%s'] * len(values))
        columns = ', '.join(attributes)
        query = (f"INSERT INTO {cls.__tablename__} ({columns}) "
                 f"VALUES ({placeholders})")

        # Executing the query
        cursor.execute(query, tuple(values))
        conn.commit()

        # Getting the last inserted ID
        last_inserted_id = cursor.lastrowid

        cursor.close()
        return last_inserted_id

    @classmethod
    # pylint: disable=line-too-long
    def select(cls, limit=None, offset=None, order_by=None, **conditions) -> List[Dict[str, Any]]:
        cursor = config.get_db_cursor()

        # Formulating the SQL query
        if conditions:
            condition_str = " AND ".join([f"{key} = %s" for key in conditions])
            query = f"SELECT * FROM {cls.__tablename__} WHERE {condition_str}"
        else:
            query = f"SELECT * FROM {cls.__tablename__}"

        # Adding an ORDER BY clause if order_by is specified
        if order_by is not None:
            query += f" ORDER BY {order_by}"

        # Adding pagination clauses if limit and offset are specified
        if limit is not None:
            query += f" LIMIT {limit}"
        if offset is not None:
            query += f" OFFSET {offset}"

        if conditions:
            cursor.execute(query, tuple(conditions.values()))
        else:
            cursor.execute(query)

        # Fetching the results
        results = cursor.fetchall()

        result_dicts = []
        columns = [desc[0] for desc in cursor.description]
        for row in results:
            result_dict = dict(zip(columns, row))
            result_dicts.append(result_dict)

        return result_dicts

    @classmethod
    def select_first(cls, **conditions) -> dict:
        cursor = config.get_db_cursor()

        # Formulating the SQL query
        if conditions:
            cond_str = ' AND '.join([f"{key} = %s" for key in conditions])
            query = (f"SELECT * FROM {cls.__tablename__} WHERE {cond_str} "
                     f"LIMIT 1")
            cursor.execute(query, tuple(conditions.values()))
        else:
            query = f"SELECT * FROM {cls.__tablename__} LIMIT 1"
            cursor.execute(query)

        # Fetching the result and mapping it to a class instance
        row = cursor.fetchone()

        if row:
            columns = [col[0] for col in cursor.description]
            result_dict = dict(zip(columns, row))
            return result_dict

        return None

    @classmethod
    def delete(cls, **conditions) -> None:
        conn = config.get_db()
        cursor = config.get_db_cursor()

        # Formulating the SQL query
        if conditions:
            condition_str = ' AND '.join([f"{key} = %s" for key in conditions])
            query = f"DELETE FROM {cls.__tablename__} WHERE {condition_str}"
            cursor.execute(query, tuple(conditions.values()))
        else:
            # If no conditions are provided, delete all records
            query = f"DELETE FROM {cls.__tablename__}"
            cursor.execute(query)

        conn.commit()
        cursor.close()

    @classmethod
    def update(cls, conditions: dict, new_values: dict) -> None:
        conn = config.get_db()
        cursor = config.get_db_cursor()

        # Formulating the SQL query
        if not conditions:
            raise ValueError(
                "Conditions must be provided for the update operation."
            )

        # Formulating the SET part of the query
        set_str = ', '.join([f"{key} = %s" for key in new_values])

        # Formulating the WHERE part of the query
        condition_str = ' AND '.join([f"{key} = %s" for key in conditions])

        query = (
                f"UPDATE {cls.__tablename__} SET {set_str} "
                f"WHERE {condition_str}"
            )

        # Combining new values and conditions for the execute method
        values = list(new_values.values()) + list(conditions.values())

        # Executing the query
        cursor.execute(query, tuple(values))
        conn.commit()
        cursor.close()

    @classmethod
    def exec_query(cls, query, params=None):
        cursor = config.get_db_cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
