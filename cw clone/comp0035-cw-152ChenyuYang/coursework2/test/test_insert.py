import pytest
import sqlite3
from coursework2.section3.queries_insert import (
    insert_new_area,
    insert_new_year,
    insert_housing_data,
    insert_waiting_list_data,
)

# Mock database setup
@pytest.fixture(scope="function")
def setup_test_database():
    """
    Set up an in-memory SQLite database for testing.
    The database will be fresh for each test.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create mock tables
    cursor.executescript("""
    CREATE TABLE Area (
        area_code TEXT PRIMARY KEY,
        area_name TEXT
    );

    CREATE TABLE Year (
        year INTEGER PRIMARY KEY
    );

    CREATE TABLE Affordable_Housing_Data (
        area_code TEXT,
        year INTEGER,
        housing_units INTEGER,
        FOREIGN KEY (area_code) REFERENCES Area (area_code),
        FOREIGN KEY (year) REFERENCES Year (year)
    );

    CREATE TABLE Waiting_List_Data (
        area_code TEXT,
        year INTEGER,
        households_count INTEGER,
        FOREIGN KEY (area_code) REFERENCES Area (area_code),
        FOREIGN KEY (year) REFERENCES Year (year)
    );
    """)

    yield conn, cursor
    conn.close()


def test_insert_new_area(setup_test_database):
    conn, cursor = setup_test_database
    area_code = "A1"
    area_name = "Test Area"
    result = insert_new_area(cursor, area_code, area_name)

    # Verify the area is inserted
    cursor.execute("SELECT * FROM Area WHERE area_code = ?;", (area_code,))
    row = cursor.fetchone()
    assert row is not None, "The new area should be inserted into the database."
    assert row[0] == area_code
    assert row[1] == area_name

    # Test inserting duplicate area
    with pytest.raises(sqlite3.IntegrityError, match="UNIQUE constraint failed"):
        insert_new_area(cursor, area_code, area_name)


def test_insert_new_year(setup_test_database):
    conn, cursor = setup_test_database
    year = 2025
    result = insert_new_year(cursor, year)

    # Verify the year is inserted
    cursor.execute("SELECT * FROM Year WHERE year = ?;", (year,))
    row = cursor.fetchone()
    assert row is not None, "The new year should be inserted into the database."
    assert row[0] == year

    # Test inserting duplicate year
    with pytest.raises(sqlite3.IntegrityError, match="UNIQUE constraint failed"):
        insert_new_year(cursor, year)


def test_insert_housing_data(setup_test_database):
    conn, cursor = setup_test_database

    # Insert valid area and year
    insert_new_area(cursor, "A1", "Test Area")
    insert_new_year(cursor, 2025)

    # Insert valid housing data
    result = insert_housing_data(cursor, "A1", 2025, 100)
    cursor.execute("""
    SELECT * FROM Affordable_Housing_Data WHERE area_code = 'A1' AND year = 2025;
    """)
    row = cursor.fetchone()
    assert row is not None, "The new housing data should be inserted into the database."
    assert row[0] == "A1"
    assert row[1] == 2025
    assert row[2] == 100

    # Test inserting housing data with invalid foreign keys
    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY constraint failed"):
        insert_housing_data(cursor, "A99", 2025, 50)  # Invalid area_code
    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY constraint failed"):
        insert_housing_data(cursor, "A1", 2030, 50)  # Invalid year


def test_insert_waiting_list_data(setup_test_database):
    conn, cursor = setup_test_database

    # Insert valid area and year
    insert_new_area(cursor, "A1", "Test Area")
    insert_new_year(cursor, 2025)

    # Insert valid waiting list data
    result = insert_waiting_list_data(cursor, "A1", 2025, 50)
    cursor.execute("""
    SELECT * FROM Waiting_List_Data WHERE area_code = 'A1' AND year = 2025;
    """)
    row = cursor.fetchone()
    assert row is not None, "The new waiting list data should be inserted into the database."
    assert row[0] == "A1"
    assert row[1] == 2025
    assert row[2] == 50

    # Test inserting waiting list data with invalid foreign keys
    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY constraint failed"):
        insert_waiting_list_data(cursor, "A99", 2025, 30)  # Invalid area_code
    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY constraint failed"):
        insert_waiting_list_data(cursor, "A1", 2030, 30)  # Invalid year
