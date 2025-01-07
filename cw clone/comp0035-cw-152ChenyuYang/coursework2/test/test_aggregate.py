import pytest
import sqlite3
from coursework2.section3.queries_aggregate import (
    get_total_housing_units_by_year,
    get_avg_waiting_list,
    get_max_waiting_list,
    get_min_waiting_list,
    get_housing_units_statistics,
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

    # Create mock tables and insert test data
    cursor.executescript("""
    CREATE TABLE Affordable_Housing_Data (
        area_code TEXT,
        year INTEGER,
        housing_units INTEGER
    );

    CREATE TABLE Waiting_List_Data (
        area_code TEXT,
        year INTEGER,
        households_count INTEGER
    );

    INSERT INTO Affordable_Housing_Data (area_code, year, housing_units) VALUES
        ('A1', 2020, 100),
        ('A1', 2021, 150),
        ('A2', 2020, 200),
        ('A2', 2021, 250);

    INSERT INTO Waiting_List_Data (area_code, year, households_count) VALUES
        ('A1', 2020, 50),
        ('A1', 2021, 60),
        ('A2', 2020, 30),
        ('A2', 2021, 80);
    """)

    yield conn, cursor
    conn.close()


def test_get_total_housing_units_by_year(setup_test_database):
    """
    Test the total housing units by year.
    """
    conn, cursor = setup_test_database

    # Test for year 2020
    result = get_total_housing_units_by_year(cursor, 2020)
    assert result == [(300,)], "The total housing units for 2020 should be 300."

    # Test for year 2021
    result = get_total_housing_units_by_year(cursor, 2021)
    assert result == [(400,)], "The total housing units for 2021 should be 400."


def test_get_avg_waiting_list(setup_test_database):
    """
    Test the average waiting list count.
    """
    conn, cursor = setup_test_database

    # Test average calculation
    result = get_avg_waiting_list(cursor)
    assert result == [(55.0,)], "The average waiting list count should be 55.0."


def test_get_max_waiting_list(setup_test_database):
    """
    Test the maximum waiting list count.
    """
    conn, cursor = setup_test_database

    # Test maximum waiting list
    result = get_max_waiting_list(cursor)
    assert result == [('A2', 2021, 80)], "The area with the max waiting list should be ('A2', 2021, 80)."


def test_get_min_waiting_list(setup_test_database):
    """
    Test the minimum waiting list count.
    """
    conn, cursor = setup_test_database

    # Test minimum waiting list
    result = get_min_waiting_list(cursor)
    assert result == [('A2', 2020, 30)], "The area with the min waiting list should be ('A2', 2020, 30)."


def test_get_housing_units_statistics(setup_test_database):
    """
    Test the housing units statistics.
    """
    conn, cursor = setup_test_database

    # Test housing units statistics
    result = get_housing_units_statistics(cursor)
    expected = [(700, 175.0, 100, 250)]
    assert result == expected, f"The housing units statistics should be {expected}."
