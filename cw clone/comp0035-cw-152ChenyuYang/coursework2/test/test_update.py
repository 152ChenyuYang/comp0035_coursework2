import pytest
import sqlite3
from coursework2.section3.queries_update import (
    update_area_name,
    update_waiting_list_by_year,
    update_housing_data,
    update_all_waiting_lists,
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

    -- Insert initial data
    INSERT INTO Area (area_code, area_name) VALUES ('A1', 'Test Area 1'), ('A2', 'Test Area 2');
    INSERT INTO Year (year) VALUES (2020), (2021);
    INSERT INTO Affordable_Housing_Data (area_code, year, housing_units) VALUES
        ('A1', 2020, 100),
        ('A2', 2021, 200);
    INSERT INTO Waiting_List_Data (area_code, year, households_count) VALUES
        ('A1', 2020, 50),
        ('A2', 2021, 60);
    """)

    yield conn, cursor
    conn.close()


def test_update_area_name(setup_test_database, monkeypatch):
    conn, cursor = setup_test_database

    # Mock user input
    monkeypatch.setattr("builtins.input", lambda _: "A1" if "area code" in _ else "Updated Area 1")
    
    # Update area name
    update_area_name(cursor)

    # Verify update
    cursor.execute("SELECT area_name FROM Area WHERE area_code = 'A1';")
    result = cursor.fetchone()
    assert result[0] == "Updated Area 1", "The area name should be updated."


def test_update_waiting_list_by_year(setup_test_database, monkeypatch):
    conn, cursor = setup_test_database

    # Mock user input
    monkeypatch.setattr("builtins.input", lambda _: "2020" if "year" in _ else ("A1" if "area code" in _ else "100"))
    
    # Update waiting list
    update_waiting_list_by_year(cursor)

    # Verify update
    cursor.execute("SELECT households_count FROM Waiting_List_Data WHERE area_code = 'A1' AND year = 2020;")
    result = cursor.fetchone()
    assert result[0] == 100, "The waiting list count should be updated to 100."


def test_update_housing_data(setup_test_database, monkeypatch):
    conn, cursor = setup_test_database

    # Mock user input
    monkeypatch.setattr("builtins.input", lambda _: "A1" if "area code" in _ else ("2020" if "year" in _ else "150"))
    
    # Update housing data
    update_housing_data(cursor)

    # Verify update
    cursor.execute("SELECT housing_units FROM Affordable_Housing_Data WHERE area_code = 'A1' AND year = 2020;")
    result = cursor.fetchone()
    assert result[0] == 150, "The housing units should be updated to 150."


def test_update_all_waiting_lists(setup_test_database, monkeypatch):
    conn, cursor = setup_test_database

    # Mock user input
    monkeypatch.setattr("builtins.input", lambda _: "10")
    
    # Batch update waiting lists
    update_all_waiting_lists(cursor)

    # Verify update
    cursor.execute("SELECT households_count FROM Waiting_List_Data;")
    results = cursor.fetchall()
    assert results == [(60,), (70,)], "All waiting list counts should be incremented by 10."
