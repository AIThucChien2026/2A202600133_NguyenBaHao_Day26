# SQLite Lab MCP Server

A Model Context Protocol (MCP) server built with FastMCP that exposes a SQLite database with tools for searching, inserting, and aggregating data.

## Features

- **Tools**:
  - `search`: Search records with support for filters (=, !=, >, <, >=, <=, LIKE, IN), sorting, and pagination.
  - `insert`: Safely insert new records into the database.
  - `aggregate`: Perform COUNT, AVG, SUM, MIN, MAX operations with optional grouping.
- **Resources**:
  - `schema://database`: Full database schema in JSON format.
  - `schema://table/{table_name}`: Individual table schema definitions.
- **Safety**: Robust validation of table names, column names, and operators. Parameterized SQL queries to prevent injection.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r ../requirements.txt
   ```

2. **Initialize Database**:
   ```bash
   python init_db.py
   ```

3. **Verify Installation**:
   ```bash
   python verify_server.py
   ```

## Client Configuration

### 1. MCP Inspector (Testing Tool)
To inspect tools and resources visually:
```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

### 2. Gemini CLI
To add this server to Gemini CLI:
```bash
gemini mcp add sqlite-lab python /ABSOLUTE/PATH/TO/implementation/mcp_server.py --description "SQLite Lab Server"
```

Then use it:
```bash
gemini --allowed-mcp-server-names sqlite-lab -p "Show me all students in cohort A1"
```

### 3. Claude Code
Add to your `.mcp.json`:
```json
{
  "mcpServers": {
    "sqlite-lab": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/implementation/mcp_server.py"]
    }
  }
}
```

## Example Usage

- **Search**: `search(table="students", filters={"cohort": "A1"})`
- **Complex Search**: `search(table="enrollments", filters={"grade": {">": 3.8}})`
- **Aggregate**: `aggregate(table="enrollments", metric="AVG", column="grade", group_by="course_id")`
- **Resource**: Read `schema://database` to understand the table structures.
