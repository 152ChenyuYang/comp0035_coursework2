import sqlite3
from pathlib import Path

# Step 1: Define the database path
base_dir = Path(__file__).resolve().parent  # Current script directory (section3)
db_path = base_dir.parents[1] / "coursework1" / "database" / "local_authority_housing.db"

# Step 2: Connect to the database
def get_db_connection(db_path):
    """Establish connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor

# Step 3: Execute SELECT queries
def execute_select_query(cursor, sql, params=None):
    """
    Execute a SELECT query and return results.
    :param cursor: SQLite cursor
    :param sql: The SQL query string
    :param params: Parameters for the SQL query (optional)
    :return: Query results
    """
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

# Step 4: Define SELECT query functions

# 1. Query all area names
def get_all_areas(cursor):
    sql = "SELECT DISTINCT area_name FROM Area ORDER BY area_name ASC;"
    return execute_select_query(cursor, sql)

# 2. Query waiting list data for a specific year
def get_waiting_list_by_year(cursor, year):
    sql = "SELECT area_code, households_count FROM Waiting_List_Data WHERE year = ?;"
    return execute_select_query(cursor, sql, params=(year,))

# 3. Query housing data for a specific area
def get_housing_data_by_area(cursor, area_code):
    sql = """
    SELECT year, housing_units 
    FROM Affordable_Housing_Data 
    WHERE area_code = ? 
    ORDER BY year ASC;
    """
    return execute_select_query(cursor, sql, params=(area_code,))

# 4. Query detailed data for a specific area and year
def get_area_details_by_year(cursor, area_code, year):
    sql = """
    SELECT 
        Area.area_name, 
        Affordable_Housing_Data.housing_units, 
        Waiting_List_Data.households_count 
    FROM Area
    LEFT JOIN Affordable_Housing_Data ON Area.area_code = Affordable_Housing_Data.area_code
    LEFT JOIN Waiting_List_Data ON Area.area_code = Waiting_List_Data.area_code
    WHERE Area.area_code = ? AND Affordable_Housing_Data.year = ? AND Waiting_List_Data.year = ?;
    """
    return execute_select_query(cursor, sql, params=(area_code, year, year))

# 5. Query all unique years
def get_unique_years(cursor):
    sql = "SELECT DISTINCT year FROM Year ORDER BY year ASC;"
    return execute_select_query(cursor, sql)

# 6. Query areas with waiting list data exceeding a specified number
def get_areas_with_large_waiting_lists(cursor, min_households):
    sql = """
    SELECT area_code, year, households_count 
    FROM Waiting_List_Data 
    WHERE households_count > ? 
    ORDER BY households_count DESC;
    """
    return execute_select_query(cursor, sql, params=(min_households,))

# Step 5: Main program execution
if __name__ == "__main__":
    if not db_path.exists():
        print(f"Database not found: {db_path}")
    else:
        conn, cursor = get_db_connection(db_path)

        while True:
            print("\nSelect an option:")
            print("1. Query all areas")
            print("2. Query waiting list data by year")
            print("3. Query housing data by area")
            print("4. Query detailed data by area and year")
            print("5. Query all unique years")
            print("6. Query areas with large waiting lists")
            print("0. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                print("\nAll Areas:")
                areas = get_all_areas(cursor)
                for area in areas:
                    print(area[0])

            elif choice == "2":
                year = input("Enter the year: ").strip()
                print(f"\nWaiting List Data for Year {year}:")
                waiting_list = get_waiting_list_by_year(cursor, year)
                for row in waiting_list:
                    print(row)

            elif choice == "3":
                area_code = input("Enter the area code: ").strip()
                print(f"\nHousing Data for Area Code {area_code}:")
                housing_data = get_housing_data_by_area(cursor, area_code)
                for row in housing_data:
                    print(row)

            elif choice == "4":
                area_code = input("Enter the area code: ").strip()
                year = input("Enter the year: ").strip()
                print(f"\nDetails for Area {area_code} in Year {year}:")
                details = get_area_details_by_year(cursor, area_code, year)
                for row in details:
                    print(row)

            elif choice == "5":
                print("\nUnique Years:")
                unique_years = get_unique_years(cursor)
                for year in unique_years:
                    print(year[0])

            elif choice == "6":
                min_households = input("Enter the minimum number of households: ").strip()
                print(f"\nAreas with Waiting Lists Greater than {min_households} Households:")
                large_waiting_lists = get_areas_with_large_waiting_lists(cursor, min_households)
                for row in large_waiting_lists:
                    print(row)

            elif choice == "0":
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please try again.")

        # Close the connection
        conn.close()
