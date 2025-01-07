import sqlite3
from pathlib import Path


# Step 1: Define the database path
base_dir = Path(__file__).resolve().parent
db_path = base_dir.parents[1] / "coursework1" / "database" / "local_authority_housing.db"


# Step 2: Connecting to a database
def get_db_connection(db_path):
    """Establish connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        conn.commit()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None, None


# Step 3: Executing UPDATE queries
def execute_update_query(cursor, sql, params=None):
    """
    Execute an UPDATE query and commit changes.
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
        print("Update successful.")
    except sqlite3.Error as e:
        print(f"An error occurred during the update: {e}")


# Step 4:UPDATE query function definition

# 1. 更新地区名称
def update_area_name(cursor):
    try:
        area_code = input("Enter area code to update: ").strip()
        new_name = input("Enter new area name: ").strip()
        sql = "UPDATE Area SET area_name = ? WHERE area_code = ?;"
        execute_update_query(cursor, sql, params=(new_name, area_code))
    except ValueError as e:
        print(f"Invalid input: {e}")


# 2. Update waiting list data for a specified year
def update_waiting_list_by_year(cursor):
    try:
        year = int(input("Enter year: ").strip())
        area_code = input("Enter area code: ").strip()
        new_count = int(input("Enter new household count: ").strip())
        sql = "UPDATE Waiting_List_Data SET households_count = ? WHERE year = ? AND area_code = ?;"
        execute_update_query(cursor, sql, params=(new_count, year, area_code))
    except ValueError as e:
        print(f"Invalid input: {e}")


# 3. Update housing data for a specified area
def update_housing_data(cursor):
    try:
        area_code = input("Enter area code: ").strip()
        year = int(input("Enter year: ").strip())
        new_units = int(input("Enter new housing units: ").strip())
        sql = "UPDATE Affordable_Housing_Data SET housing_units = ? WHERE area_code = ? AND year = ?;"
        execute_update_query(cursor, sql, params=(new_units, area_code, year))
    except ValueError as e:
        print(f"Invalid input: {e}")


# 4. Bulk update of waiting list data
def update_all_waiting_lists(cursor):
    try:
        increment_by = int(input("Enter the number to increment household counts by: ").strip())
        sql = "UPDATE Waiting_List_Data SET households_count = households_count + ?;"
        execute_update_query(cursor, sql, params=(increment_by,))
    except ValueError as e:
        print(f"Invalid input: {e}")


# Step 5: Main program 
if __name__ == "__main__":
    if not db_path.exists():
        print(f"Database not found: {db_path}")
    else:
        conn, cursor = get_db_connection(db_path)

        try:
            print("\nChoose an operation:")
            print("1. Update Area Name")
            print("2. Update Waiting List Data for a Specific Year")
            print("3. Update Housing Data for a Specific Area and Year")
            print("4. Batch Update Waiting List Counts")

            choice = int(input("Enter your choice (1-4): ").strip())

            if choice == 1:
                update_area_name(cursor)
            elif choice == 2:
                update_waiting_list_by_year(cursor)
            elif choice == 3:
                update_housing_data(cursor)
            elif choice == 4:
                update_all_waiting_lists(cursor)
            else:
                print("Invalid choice. Please select a number between 1 and 4.")

        except ValueError as e:
            print(f"Invalid input: {e}")
        finally:
            # close
            conn.close()
