import pytest
import sqlite3
from coursework2.section3.queries_join import get_filtered_area_and_year

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
    CREATE TABLE Area (
        area_code TEXT PRIMARY KEY,
        area_name TEXT
    );

    CREATE TABLE Year (
        year INTEGER PRIMARY KEY
    );

    INSERT INTO Area (area_code, area_name) VALUES 
        ('A1', 'Test Area 1'),
        ('A2', 'Test Area 2');

    INSERT INTO Year (year) VALUES 
        (2020), 
        (2021);
    """)

    yield conn, cursor
    conn.close()


def test_get_filtered_area_and_year_no_filters(setup_test_database):
    """
    Test querying all areas and years without any filters.
    """
    conn, cursor = setup_test_database

    # Query without filters
    results = get_filtered_area_and_year(cursor)

    # Verify results
    expected = [
        ('Test Area 1', 2020),
        ('Test Area 1', 2021),
        ('Test Area 2', 2020),
        ('Test Area 2', 2021)
    ]
    assert results == expected, f"Expected {expected}, but got {results}"


def test_get_filtered_area_and_year_with_area_filter(setup_test_database):
    """
    Test querying with area name filter.
    """
    conn, cursor = setup_test_database

    # Query with area_name filter
    results = get_filtered_area_and_year(cursor, area_name="Test Area 1")

    # Verify results
    expected = [
        ('Test Area 1', 2020),
        ('Test Area 1', 2021)
    ]
    assert results == expected, f"Expected {expected}, but got {results}"


def test_get_filtered_area_and_year_with_year_filter(setup_test_database):
    """
    Test querying with year filter.
    """
    conn, cursor = setup_test_database

    # Query with year filter
    results = get_filtered_area_and_year(cursor, year=2020)

    # Verify results
    expected = [
        ('Test Area 1', 2020),
        ('Test Area 2', 2020)
    ]
    assert results == expected, f"Expected {expected}, but got {results}"


def test_get_filtered_area_and_year_with_area_and_year_filter(setup_test_database):
    """
    Test querying with both area name and year filters.
    """
    conn, cursor = setup_test_database

    # Query with both filters
    results = get_filtered_area_and_year(cursor, area_name="Test Area 1", year=2020)

    # Verify results
    expected = [
        ('Test Area 1', 2020)
    ]
    assert results == expected, f"Expected {expected}, but got {results}"


def test_get_filtered_area_and_year_no_results(setup_test_database):
    """
    Test querying with filters that yield no results.
    """
    conn, cursor = setup_test_database

    # Query with a non-matching filter
    results = get_filtered_area_and_year(cursor, area_name="Nonexistent Area", year=1999)

    # Verify results
    assert results == [], f"Expected no results, but got {results}"
