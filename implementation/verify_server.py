from db import SQLiteAdapter, ValidationError
import json

def test_adapter():
    adapter = SQLiteAdapter()
    print("--- Starting Verification ---")

    # 1. Test List Tables
    print("\n[1] Testing list_tables:")
    tables = adapter.list_tables()
    print(f"Tables found: {tables}")

    # 2. Test valid search
    print("\n[2] Testing valid search (students in cohort A1):")
    results = adapter.search("students", filters={"cohort": "A1"})
    print(json.dumps(results, indent=2))

    # 3. Test search with complex filter (grade > 3.8)
    print("\n[3] Testing complex search (enrollments with grade > 3.8):")
    results = adapter.search("enrollments", filters={"grade": {">": 3.8}})
    print(json.dumps(results, indent=2))

    # 4. Test unknown table (Should fail)
    print("\n[4] Testing unknown table error handling:")
    try:
        adapter.search("ghost_table")
    except ValidationError as e:
        print(f"Caught expected error: {e}")

    # 5. Test unknown column (Should fail)
    print("\n[5] Testing unknown column error handling:")
    try:
        adapter.search("students", columns=["non_existent_col"])
    except ValidationError as e:
        print(f"Caught expected error: {e}")

    # 6. Test unsupported operator (Should fail)
    print("\n[6] Testing unsupported operator error handling:")
    try:
        adapter.search("students", filters={"name": {"LIKE_SMILEY": "A%"}})
    except ValidationError as e:
        print(f"Caught expected error: {e}")

    # 7. Test valid insert
    print("\n[7] Testing valid insert:")
    new_student = {"name": "Frank Castle", "cohort": "C3", "email": "punisher@example.com"}
    result = adapter.insert("students", new_student)
    print(f"Inserted: {result}")

    # 8. Test empty insert (Should fail)
    print("\n[8] Testing empty insert error handling:")
    try:
        adapter.insert("students", {})
    except ValidationError as e:
        print(f"Caught expected error: {e}")

    # 9. Test valid aggregate
    print("\n[9] Testing valid aggregate (AVG grade per course):")
    results = adapter.aggregate("enrollments", "AVG", column="grade", group_by="course_id")
    print(json.dumps(results, indent=2))

    # 10. Test invalid metric (Should fail)
    print("\n[10] Testing invalid metric error handling:")
    try:
        adapter.aggregate("students", "DANCE")
    except ValidationError as e:
        print(f"Caught expected error: {e}")

    # 11. Test schema resource
    print("\n[11] Testing schema retrieval:")
    schema = adapter.get_table_schema("students")
    print(f"Schema for 'students': {len(schema)} columns found.")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    test_adapter()
