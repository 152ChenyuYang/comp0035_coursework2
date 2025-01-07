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
    cursor.execute('PRAGMA foreign_keys = ON;')
    conn.commit()
    return conn, cursor


# Step 3: Execute DELETE queries
def execute_delete_query(cursor, sql, params=None):
    """
    Execute a DELETE query and commit changes.
    :param cursor: SQLite cursor
    :param sql: The SQL query string
    :param params: Parameters for the SQL query (optional)
    """
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        cursor.connection.commit()
        print("Deletion successful.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


# Step 4: Define DELETE query functions

# 1. Delete a specific area
def delete_area(cursor, area_code):
    sql = "DELETE FROM Area WHERE area_code = ?;"
    execute_delete_query(cursor, sql, params=(area_code,))


# 2. Delete data for a specific year
def delete_year(cursor, year):
    sql = "DELETE FROM Year WHERE year = ?;"
    execute_delete_query(cursor, sql, params=(year,))


# 3. Delete housing data for a specific area
def delete_housing_data_by_area(cursor, area_code):
    sql = "DELETE FROM Affordable_Housing_Data WHERE area_code = ?;"
    execute_delete_query(cursor, sql, params=(area_code,))


# 4. Delete waiting list data for a specific year
def delete_waiting_list_by_year(cursor, year):
    sql = "DELETE FROM Waiting_List_Data WHERE year = ?;"
    execute_delete_query(cursor, sql, params=(year,))


# 5. Clear all data
def clear_all_data(cursor):
    tables = ["Affordable_Housing_Data", "Waiting_List_Data", "Area", "Year"]
    for table in tables:
        sql = f"DELETE FROM {table};"
        execute_delete_query(cursor, sql)
    print("All tables have been cleared.")


# Step 5: Main program execution
if __name__ == "__main__":
    if not db_path.exists():
        print(f"Database not found: {db_path}")
    else:
        conn, cursor = get_db_connection(db_path)

        try:
            # 1. Delete a specific area
            print("\nDelete a specific Area:")
            area_code = input("Enter area code to delete: ").strip()
            delete_area(cursor, area_code)

            # 2. Delete data for a specific year
            print("\nDelete data for a specific Year:")
            year = int(input("Enter year to delete: ").strip())
            delete_year(cursor, year)

            # 3. Delete housing data for a specific area
            print("\nDelete housing data for a specific Area:")
            area_code = input("Enter area code for housing data to delete: ").strip()
            delete_housing_data_by_area(cursor, area_code)

            # 4. Delete waiting list data for a specific year
            print("\nDelete waiting list data for a specific Year:")
            year = int(input("Enter year for waiting list data to delete: ").strip())
            delete_waiting_list_by_year(cursor, year)

            # 5. Clear all data
            confirm = input("\nDo you want to clear all data from all tables? (yes/no): ").strip().lower()
            if confirm == "yes":
                clear_all_data(cursor)

        except ValueError as e:
            print(f"Invalid input: {e}")
        finally:
            # Close the connection
            conn.close()
