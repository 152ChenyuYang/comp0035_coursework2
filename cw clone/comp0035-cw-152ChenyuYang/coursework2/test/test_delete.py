import pytest
import sqlite3
from pathlib import Path
from coursework2.section3.queries_delete import (
    delete_area,
    delete_year,
    delete_housing_data_by_area,
    delete_waiting_list_by_year,
    clear_all_data,
    get_db_connection,
)

# Set the test database path
db_path = Path(":memory:")


@pytest.fixture(scope="function")
def setup_test_database():
    """
    Set up an in-memory SQLite database for testing.
    The database will be fresh for each test.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create mock tables and insert mock data
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
        FOREIGN KEY (area_code) REFERENCES Area (area_code)
    );

    CREATE TABLE Waiting_List_Data (
        area_code TEXT,
        year INTEGER,
        households_count INTEGER,
        FOREIGN KEY (area_code) REFERENCES Area (area_code)
    );

    -- Insert mock data
    INSERT INTO Area VALUES ('A1', 'Area 1'), ('A2', 'Area 2');
    INSERT INTO Year VALUES (2020), (2021);
    INSERT INTO Affordable_Housing_Data VALUES ('A1', 2020, 100), ('A2', 2020, 200);
    INSERT INTO Waiting_List_Data VALUES ('A1', 2020, 50), ('A2', 2020, 60);
    """)

    yield conn, cursor

    conn.close()


def test_delete_area(setup_test_database):
    conn, cursor = setup_test_database
    delete_area(cursor, 'A1')

    # Verify the area is deleted
    cursor.execute("SELECT * FROM Area WHERE area_code = 'A1';")
    results = cursor.fetchall()
    assert len(results) == 0, "Area with area_code 'A1' should be deleted."


def test_delete_year(setup_test_database):
    conn, cursor = setup_test_database
    delete_year(cursor, 2020)

    # Verify the year is deleted
    cursor.execute("SELECT * FROM Year WHERE year = 2020;")
    results = cursor.fetchall()
    assert len(results) == 0, "Year 2020 should be deleted."


def test_delete_housing_data_by_area(setup_test_database):
    conn, cursor = setup_test_database
    delete_housing_data_by_area(cursor, 'A1')

    # Verify the housing data for the area is deleted
    cursor.execute("SELECT * FROM Affordable_Housing_Data WHERE area_code = 'A1';")
    results = cursor.fetchall()
    assert len(results) == 0, "Housing data for area_code 'A1' should be deleted."


def test_delete_waiting_list_by_year(setup_test_database):
    conn, cursor = setup_test_database
    delete_waiting_list_by_year(cursor, 2020)

    # Verify the waiting list data for the year is deleted
    cursor.execute("SELECT * FROM Waiting_List_Data WHERE year = 2020;")
    results = cursor.fetchall()
    assert len(results) == 0, "Waiting list data for year 2020 should be deleted."


def test_clear_all_data(setup_test_database):
    conn, cursor = setup_test_database
    clear_all_data(cursor)

    # Verify all tables are cleared
    for table in ["Area", "Year", "Affordable_Housing_Data", "Waiting_List_Data"]:
        cursor.execute(f"SELECT * FROM {table};")
        results = cursor.fetchall()
        assert len(results) == 0, f"Table {table} should be cleared."


def test_invalid_area_deletion(setup_test_database):
    conn, cursor = setup_test_database
    delete_area(cursor, 'A99')  # Area 'A99' does not exist

    # Verify no error occurs and other data remains intact
    cursor.execute("SELECT COUNT(*) FROM Area;")
    count = cursor.fetchone()[0]
    assert count == 2, "Non-existent area deletion should not affect existing data."
