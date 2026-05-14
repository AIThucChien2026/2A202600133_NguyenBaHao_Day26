import sqlite3
import os

class ValidationError(Exception):
    """Raised when a request cannot be safely executed."""

class SQLiteAdapter:
    def __init__(self, db_path="lab_database.db"):
        self.db_path = db_path

    def connect(self):
        """Returns a sqlite connection with row_factory enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def list_tables(self):
        """Queries sqlite_master and returns non-internal tables."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            return [row['name'] for row in cursor.fetchall()]

    def get_table_schema(self, table_name):
        """Runs PRAGMA table_info(table) and normalizes result."""
        # Safety check for table name
        if table_name not in self.list_tables():
            raise ValidationError(f"Table '{table_name}' does not exist.")

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name});")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_all_schemas(self):
        """Collects schemas for all tables."""
        tables = self.list_tables()
        schemas = {}
        for table in tables:
            schemas[table] = self.get_table_schema(table)
        return schemas

    def validate_columns(self, table_name, columns):
        """Validates that columns exist in the table."""
        schema = self.get_table_schema(table_name)
        valid_columns = [col['name'] for col in schema]
        for col in columns:
            if col not in valid_columns:
                raise ValidationError(f"Column '{col}' does not exist in table '{table_name}'.")

    def _build_where_clause(self, valid_columns, filters):
        """Helper to build a safe WHERE clause with multiple operators."""
        if not filters:
            return "", []
        
        where_clauses = []
        params = []
        for col, condition in filters.items():
            if col not in valid_columns:
                raise ValidationError(f"Invalid filter column: {col}")
            
            if isinstance(condition, dict):
                for op, val in condition.items():
                    allowed_ops = ["=", "!=", ">", "<", ">=", "<=", "LIKE", "IN"]
                    if op.upper() not in allowed_ops:
                        raise ValidationError(f"Unsupported operator: {op}")
                    
                    if op.upper() == "IN":
                        if not isinstance(val, list):
                            raise ValidationError("Value for 'IN' operator must be a list.")
                        if not val:
                            raise ValidationError("Value list for 'IN' operator cannot be empty.")
                        placeholders = ", ".join(["?" for _ in val])
                        where_clauses.append(f"{col} IN ({placeholders})")
                        params.extend(val)
                    else:
                        where_clauses.append(f"{col} {op.upper()} ?")
                        params.append(val)
            else:
                # Default to equality
                where_clauses.append(f"{col} = ?")
                params.append(condition)
        
        where_str = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        return where_str, params

    def search(self, table, columns=None, filters=None, limit=20, offset=0, order_by=None, descending=False):
        """
        Executes a search query with bound parameters and robust validation.
        """
        tables = self.list_tables()
        if table not in tables:
            raise ValidationError(f"Invalid table name: {table}")

        schema = self.get_table_schema(table)
        valid_columns = [col['name'] for col in schema]

        if columns:
            self.validate_columns(table, columns)
            cols_str = ", ".join(columns)
        else:
            cols_str = "*"

        query = f"SELECT {cols_str} FROM {table}"
        
        where_str, params = self._build_where_clause(valid_columns, filters)
        query += where_str

        if order_by:
            if order_by not in valid_columns:
                raise ValidationError(f"Invalid order_by column: {order_by}")
            direction = "DESC" if descending else "ASC"
            query += f" ORDER BY {order_by} {direction}"

        query += f" LIMIT {int(limit)} OFFSET {int(offset)}"

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def insert(self, table, values):
        """
        Executes a parameterized INSERT statement with validation.
        """
        tables = self.list_tables()
        if table not in tables:
            raise ValidationError(f"Invalid table name: {table}")

        if not values:
            raise ValidationError("Insert values cannot be empty.")

        self.validate_columns(table, values.keys())

        cols = ", ".join(values.keys())
        placeholders = ", ".join(["?" for _ in values])
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, list(values.values()))
            conn.commit()
            last_id = cursor.lastrowid
            
            # Return the inserted record
            schema = self.get_table_schema(table)
            if any(col['name'] == 'id' for col in schema):
                cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (last_id,))
            else:
                where = " AND ".join([f"{k} = ?" for k in values.keys()])
                cursor.execute(f"SELECT * FROM {table} WHERE {where}", list(values.values()))
            
            row = cursor.fetchone()
            return dict(row) if row else {}

    def aggregate(self, table, metric, column=None, filters=None, group_by=None):
        """
        Executes COUNT / AVG / SUM / MIN / MAX query with robust validation.
        """
        allowed_metrics = ["COUNT", "AVG", "SUM", "MIN", "MAX"]
        metric = metric.upper()
        if metric not in allowed_metrics:
            raise ValidationError(f"Invalid metric: {metric}. Allowed metrics: {allowed_metrics}")

        tables = self.list_tables()
        if table not in tables:
            raise ValidationError(f"Invalid table name: {table}")

        schema = self.get_table_schema(table)
        valid_columns = [col['name'] for col in schema]

        if column and column not in valid_columns:
            raise ValidationError(f"Invalid column name: {column}")

        if group_by and group_by not in valid_columns:
            raise ValidationError(f"Invalid group_by column: {group_by}")

        select_col = f"{metric}({column if column else '*'})"
        if group_by:
            query = f"SELECT {group_by}, {select_col} AS result"
        else:
            query = f"SELECT {select_col} AS result"
        
        query += f" FROM {table}"
        
        where_str, params = self._build_where_clause(valid_columns, filters)
        query += where_str

        if group_by:
            query += f" GROUP BY {group_by}"

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
