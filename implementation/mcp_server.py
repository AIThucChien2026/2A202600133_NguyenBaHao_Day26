from fastmcp import FastMCP
from db import SQLiteAdapter, ValidationError
import json

# Initialize the FastMCP server
mcp = FastMCP("SQLite Lab MCP Server")

# Initialize the database adapter
adapter = SQLiteAdapter()

@mcp.tool(name="search")
def search(table: str, filters: dict = None, columns: list = None, limit: int = 20, offset: int = 0, order_by: str = None, descending: bool = False):
    """
    Search for records in a specified table with optional filters, column selection, and pagination.
    
    Args:
        table: Name of the table to search.
        filters: Dictionary of column-value pairs for filtering (e.g., {"cohort": "A1"}).
        columns: List of columns to return.
        limit: Maximum number of records to return (default 20).
        offset: Number of records to skip (default 0).
        order_by: Column to sort by.
        descending: Whether to sort in descending order (default False).
    """
    try:
        results = adapter.search(table, columns, filters, limit, offset, order_by, descending)
        return json.dumps(results, indent=2)
    except ValidationError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"

@mcp.tool(name="insert")
def insert(table: str, values: dict):
    """
    Insert a new record into a specified table.
    
    Args:
        table: Name of the table to insert into.
        values: Dictionary of column-value pairs for the new record.
    """
    try:
        result = adapter.insert(table, values)
        return json.dumps({"message": "Record inserted successfully", "data": result}, indent=2)
    except ValidationError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"

@mcp.tool(name="aggregate")
def aggregate(table: str, metric: str, column: str = None, filters: dict = None, group_by: str = None):
    """
    Perform aggregate operations (COUNT, AVG, SUM, MIN, MAX) on a table.
    
    Args:
        table: Name of the table.
        metric: Aggregate function to use (COUNT, AVG, SUM, MIN, MAX).
        column: Column to perform the aggregate on (optional for COUNT).
        filters: Optional filters to apply before aggregation.
        group_by: Optional column to group results by.
    """
    try:
        results = adapter.aggregate(table, metric, column, filters, group_by)
        return json.dumps(results, indent=2)
    except ValidationError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"

@mcp.resource("schema://database")
def get_database_schema() -> str:
    """Returns the full schema of the database."""
    try:
        schema = adapter.get_all_schemas()
        return json.dumps(schema, indent=2)
    except Exception as e:
        return f"Error fetching database schema: {str(e)}"

@mcp.resource("schema://table/{table_name}")
def get_table_schema(table_name: str) -> str:
    """Returns the schema for a specific table."""
    try:
        schema = adapter.get_table_schema(table_name)
        return json.dumps({table_name: schema}, indent=2)
    except ValidationError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error fetching schema for table {table_name}: {str(e)}"

if __name__ == "__main__":
    mcp.run()
