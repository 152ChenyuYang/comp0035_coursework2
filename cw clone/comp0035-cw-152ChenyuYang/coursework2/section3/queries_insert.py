import sqlite3
from pathlib import Path


# Step 1: Define the database path
base_dir = Path(__file__).resolve().parent
db_path = base_dir.parents[1] / "coursework1" / "database" / "local_authority_housing.db"


# Step 2: Connect to the database
def get_db_connection(db_path):
    """Establish connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')  # Ensure foreign key constraints are enabled
    conn.commit()
    return conn, cursor


# Step 3: Execute INSERT queries
def execute_insert_query(cursor, sql, params):
    """
    Execute an INSERT query and commit changes.
    :param cursor: SQLite cursor
    :param sql: The SQL query string
    :param params: Parameters for the SQL query
    :return: Last inserted row ID
    """
    try:
        cursor.execute(sql, params)
        cursor.connection.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e}")
        raise  # Re-raise exception to ensure calling function can handle it
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        raise  # Re-raise generic SQLite errors


# Step 4: Define data insertion functions

# 1. Insert new area information
def insert_new_area(cursor, area_code, area_name):
    sql = "INSERT INTO Area (area_code, area_name) VALUES (?, ?);"
    return execute_insert_query(cursor, sql, (area_code, area_name))


# 2. Insert new year information
def insert_new_year(cursor, year):
    sql = "INSERT INTO Year (year) VALUES (?);"
    return execute_insert_query(cursor, sql, (year,))


# 3. Insert new housing data
def insert_housing_data(cursor, area_code, year, housing_units):
    sql = """
    INSERT INTO Affordable_Housing_Data (area_code, year, housing_units) 
    VALUES (?, ?, ?);
    """
    return execute_insert_query(cursor, sql, (area_code, year, housing_units))


# 4. Insert new waiting list data
def insert_waiting_list_data(cursor, area_code, year, households_count):
    sql = """
    INSERT INTO Waiting_List_Data (area_code, year, households_count) 
    VALUES (?, ?, ?);
    """
    return execute_insert_query(cursor, sql, (area_code, year, households_count))


# Step 5: Main program execution
if __name__ == "__main__":
    if not db_path.exists():
        print(f"Database not found: {db_path}")
    else:
        conn, cursor = get_db_connection(db_path)

        try:
            # 1. Insert new area information
            print("\nInsert new Area:")
            area_code = input("Enter area code: ").strip()
            area_name = input("Enter area name: ").strip()
            try:
                area_id = insert_new_area(cursor, area_code, area_name)
                print(f"Inserted new Area with code: {area_code}, name: {area_name}")
            except sqlite3.IntegrityError as e:
                print(f"Failed to insert area: {e}")

            # 2. Insert new year information
            print("\nInsert new Year:")
            year = input("Enter year: ").strip()
            try:
                year_id = insert_new_year(cursor, int(year))
                print(f"Inserted new Year: {year}")
            except (ValueError, sqlite3.IntegrityError) as e:
                print(f"Failed to insert year: {e}")

            # 3. Insert new housing data
            print("\nInsert new Affordable Housing Data:")
            area_code = input("Enter area code for housing data: ").strip()
            year = input("Enter year for housing data: ").strip()
            housing_units = input("Enter housing units: ").strip()
            try:
                housing_id = insert_housing_data(cursor, area_code, int(year), int(housing_units))
                print(f"Inserted new Housing Data for area code {area_code}, year {year}")
            except (ValueError, sqlite3.IntegrityError) as e:
                print(f"Failed to insert housing data: {e}")

            # 4. Insert new waiting list data
            print("\nInsert new Waiting List Data:")
            area_code = input("Enter area code for waiting list data: ").strip()
            year = input("Enter year for waiting list data: ").strip()
            households_count = input("Enter households count: ").strip()
            try:
                waiting_list_id = insert_waiting_list_data(cursor, area_code, int(year), int(households_count))
                print(f"Inserted new Waiting List Data for area code {area_code}, year {year}")
            except (ValueError, sqlite3.IntegrityError) as e:
                print(f"Failed to insert waiting list data: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            # Close the connection
            conn.close()
