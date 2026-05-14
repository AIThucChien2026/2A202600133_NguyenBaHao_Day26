# Implementation Plan: Database MCP Server with FastMCP and SQLite

Build a Model Context Protocol (MCP) server that exposes a SQLite database through specific tools and resources, ensuring safety and discoverability.

## User Review Required

> [!IMPORTANT]
> The implementation relies on the `fastmcp` library. Ensure it is installed in your Python environment.
> The database will use a sample schema (students, courses, enrollments) for demonstration purposes.

## Proposed Changes

### Phase 1: Environment & Database Initialization
Set up the project structure and initialize the SQLite database with seed data.

#### [NEW] `implementation/db.py`
- Define a `SQLiteAdapter` class to handle connections and query execution.
- Implement methods for schema inspection.

#### [NEW] `implementation/init_db.py`
- Create tables: `students`, `courses`, `enrollments`.
- Insert sample data for each table.

---

### Phase 2: Database Adapter Implementation
Implement the core logic for querying and modifying the database safely.

#### [MODIFY] `implementation/db.py`
- Implement `search_records(table, filters, columns, limit, offset, order_by, descending)`.
- Implement `insert_record(table, values)`.
- Implement `aggregate_data(table, metric, column, filters, group_by)`.
- Use parameterized queries to prevent SQL injection.

---

### Phase 3: MCP Server Core (Tools & Resources)
Expose the database functionality through FastMCP tools and resources.

#### [NEW] `implementation/mcp_server.py`
- Initialize `FastMCP("SQLite Lab MCP Server")`.
- Implement `@mcp.tool(name="search")`.
- Implement `@mcp.tool(name="insert")`.
- Implement `@mcp.tool(name="aggregate")`.
- Implement `@mcp.resource("schema://database")`.
- Implement `@mcp.resource("schema://table/{table_name}")`.

---

### Phase 4: Validation and Error Handling
Add robust validation to reject unsafe or invalid requests.

#### [MODIFY] `implementation/mcp_server.py`
- Add validation for table names and column names against the actual schema.
- Validate metrics (count, avg, sum, min, max).
- Ensure `insert` values are not empty and match table columns.
- Return descriptive error messages for invalid requests.

---

### Phase 5: Verification and Testing
Create scripts and tests to verify the server's functionality.

#### [NEW] `implementation/verify_server.py`
- A script to run the server and perform smoke tests (tool discovery, basic queries).

#### [NEW] `implementation/tests/test_server.py`
- Unit tests for the `SQLiteAdapter` and MCP tools using a mock or temporary database.

---

### Phase 6: Documentation and Demo
Prepare the final deliverables.

#### [NEW] `implementation/README.md`
- Installation and setup instructions.
- Tool descriptions and usage examples.
- Client configuration (Gemini CLI, Claude Code).
- Steps to run the MCP Inspector.

## Verification Plan

### Automated Tests
- Run `pytest implementation/tests/test_server.py` to verify core logic.
- Run `python implementation/verify_server.py` for a quick integration check.

### Manual Verification
- Use **MCP Inspector** to explore tools and resources:
  `npx @modelcontextprotocol/inspector python implementation/mcp_server.py`
- Connect via **Gemini CLI**:
  `gemini mcp add sqlite-lab python implementation/mcp_server.py`
  Verify with: `gemini --allowed-mcp-server-names sqlite-lab -p "show all students"`
