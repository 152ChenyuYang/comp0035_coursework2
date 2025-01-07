import sys
from pathlib import Path
import pytest


# Add the parent directory of coursework2 to the module search path
base_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(base_dir))

from coursework2.section3.queries_select import (
    get_all_areas,
    get_waiting_list_by_year,
    get_housing_data_by_area,
    get_area_details_by_year,
    get_unique_years,
    get_areas_with_large_waiting_lists,
    get_db_connection,
)

# Define the database path
db_path = base_dir / "coursework1" / "database" / "local_authority_housing.db"

# Check if the database path exists
assert db_path.exists(), f"Database file not found at: {db_path}"


@pytest.fixture(scope="module")
def db_cursor():
    """
    Set up the database connection and cursor, and close the connection after tests.
    """
    try:
        conn, cursor = get_db_connection(db_path)
        yield cursor
    except Exception as e:
        raise RuntimeError(f"Failed to connect to the database: {e}")
    finally:
        conn.close()


def test_get_all_areas(db_cursor):
    """
    GIVEN the database contains area names
    WHEN calling `get_all_areas`
    THEN the returned results should not be empty, and all area names should be strings.
    """
    results = get_all_areas(db_cursor)
    assert results is not None, "The result should not be None"
    assert len(results) > 0, "The area list should not be empty"
    assert all(isinstance(area[0], str) for area in results), "Each area name should be a string"


def test_get_waiting_list_by_year(db_cursor):
    """
    GIVEN a specific year exists in the database
    WHEN calling `get_waiting_list_by_year`
    THEN the results should include valid area codes and integer waiting list counts.
    """
    year = 2020
    results = get_waiting_list_by_year(db_cursor, year)
    assert results is not None, "The result should not be None"
    assert len(results) > 0, f"There should be waiting list data for the year {year}"
    assert all(isinstance(row[1], int) for row in results), "The waiting list count should be an integer"


def test_get_housing_data_by_area(db_cursor):
    """
    GIVEN a specific area code exists in the database
    WHEN calling `get_housing_data_by_area`
    THEN the results should include years and integer housing unit counts.
    """
    area_code = "E09000001"
    results = get_housing_data_by_area(db_cursor, area_code)
    assert results is not None, "The result should not be None"
    assert len(results) > 0, f"There should be housing data for area code {area_code}"
    assert all(isinstance(row[1], int) for row in results), "The housing unit count should be an integer"


def test_get_area_details_by_year(db_cursor):
    """
    GIVEN a specific area code and year exist in the database
    WHEN calling `get_area_details_by_year`
    THEN the result should include area name, integer housing units, and waiting list counts.
    """
    area_code = "E09000001"
    year = 2020
    results = get_area_details_by_year(db_cursor, area_code, year)
    assert results is not None, "The result should not be None"
    if len(results) == 0:
        assert results == [], "Results should be an empty list when no data is found"
    else:
        assert isinstance(results[0][0], str), "The area name should be a string"
        assert isinstance(results[0][1], int), "The housing unit count should be an integer"
        assert isinstance(results[0][2], int), "The waiting list count should be an integer"


def test_get_unique_years(db_cursor):
    """
    GIVEN the database contains unique years
    WHEN calling `get_unique_years`
    THEN the result should include integer years in ascending order.
    """
    results = get_unique_years(db_cursor)
    assert results is not None, "The result should not be None"
    assert len(results) > 0, "The year list should not be empty"
    assert all(isinstance(year[0], int) for year in results), "Each year should be an integer"


def test_get_areas_with_large_waiting_lists(db_cursor):
    """
    GIVEN a minimum household count threshold
    WHEN calling `get_areas_with_large_waiting_lists`
    THEN the result should include areas and years with waiting lists above the threshold.
    """
    min_households = 500
    results = get_areas_with_large_waiting_lists(db_cursor, min_households)
    assert results is not None, "The result should not be None"
    assert len(results) > 0, f"There should be records with waiting list counts greater than {min_households}"
    assert all(row[2] > min_households for row in results), "The waiting list count should be greater than the minimum threshold"
