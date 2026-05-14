import pytest
import os
import sqlite3
import sys

# Add the implementation directory to path so we can import db
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import SQLiteAdapter, ValidationError

TEST_DB = "test_lab.db"

@pytest.fixture
def adapter():
    # Setup: Create a temporary test database
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 25), ('Bob', 30)")
    conn.commit()
    conn.close()
    
    adapter = SQLiteAdapter(db_path=TEST_DB)
    yield adapter
    
    # Teardown: Remove the test database
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_list_tables(adapter):
    tables = adapter.list_tables()
    assert "users" in tables

def test_search_valid(adapter):
    results = adapter.search("users", filters={"name": "Alice"})
    assert len(results) == 1
    assert results[0]["age"] == 25

def test_search_invalid_table(adapter):
    with pytest.raises(ValidationError, match="Invalid table name"):
        adapter.search("non_existent")

def test_search_invalid_column(adapter):
    with pytest.raises(ValidationError, match="Column 'wrong' does not exist"):
        adapter.search("users", columns=["wrong"])

def test_insert_valid(adapter):
    result = adapter.insert("users", {"name": "Charlie", "age": 35})
    assert result["name"] == "Charlie"
    assert result["age"] == 35
    
    # Verify it's actually in the DB
    results = adapter.search("users", filters={"name": "Charlie"})
    assert len(results) == 1

def test_insert_empty(adapter):
    with pytest.raises(ValidationError, match="Insert values cannot be empty"):
        adapter.insert("users", {})

def test_aggregate_count(adapter):
    results = adapter.aggregate("users", "COUNT")
    assert results[0]["result"] == 2

def test_aggregate_avg(adapter):
    results = adapter.aggregate("users", "AVG", column="age")
    assert results[0]["result"] == 27.5

def test_invalid_metric(adapter):
    with pytest.raises(ValidationError, match="Invalid metric"):
        adapter.aggregate("users", "INVALID")
