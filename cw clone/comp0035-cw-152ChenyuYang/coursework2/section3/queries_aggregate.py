import sqlite3
from pathlib import Path


# Step 1: Define the database path
base_dir = Path(__file__).resolve().parent
db_path = base_dir.parents[1] / "coursework1" / "database" / "local_authority_housing.db"


# Step 2: Connect to the database
def get_db_connection(db_path):
    """Establish connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        return conn, cursor
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None, None


# Step 3: Execute aggregate queries
def execute_aggregate_query(cursor, sql, params=None):
    """
    Execute an aggregate query and return the result.
    :param cursor: SQLite cursor
    :param sql: The SQL query string
    :param params: Parameters for the SQL query (optional)
    :return: Query result
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


# Step 4: Define aggregate query functions

# 1. Get the total housing supply for a specific year
def get_total_housing_units_by_year(cursor, year):
    sql = """
    SELECT SUM(housing_units) 
    FROM Affordable_Housing_Data 
    WHERE year = ?;
    """
    return execute_aggregate_query(cursor, sql, params=(year,))


# 2. Get the average waiting list count across all areas
def get_avg_waiting_list(cursor):
    sql = "SELECT AVG(households_count) FROM Waiting_List_Data;"
    return execute_aggregate_query(cursor, sql)


# 3. Get the area and year with the highest waiting list count
def get_max_waiting_list(cursor):
    sql = """
    SELECT area_code, year, MAX(households_count) 
    FROM Waiting_List_Data;
    """
    return execute_aggregate_query(cursor, sql)


# 4. Get the area and year with the lowest waiting list count
def get_min_waiting_list(cursor):
    sql = """
    SELECT area_code, year, MIN(households_count) 
    FROM Waiting_List_Data;
    """
    return execute_aggregate_query(cursor, sql)


# 5. Get statistics for housing supply: total, minimum, maximum, and average
def get_housing_units_statistics(cursor):
    sql = """
    SELECT 
        SUM(housing_units) AS total_units, 
        AVG(housing_units) AS avg_units, 
        MIN(housing_units) AS min_units, 
        MAX(housing_units) AS max_units 
    FROM Affordable_Housing_Data;
    """
    return execute_aggregate_query(cursor, sql)


# Step 5: Main program execution
if __name__ == "__main__":
    if not db_path.exists():
        print(f"Database not found: {db_path}")
    else:
        conn, cursor = get_db_connection(db_path)

        try:
            # 1. Get the total housing supply for a specific year
            year = int(input("Enter year to calculate total housing units: ").strip())
            total_units = get_total_housing_units_by_year(cursor, year)
            print(f"\nTotal housing units for the year {year}: {total_units[0][0]}")

            # 2. Get the average waiting list count across all areas
            avg_waiting_list = get_avg_waiting_list(cursor)
            print(f"\nAverage waiting list count: {avg_waiting_list[0][0]:.2f}")

            # 3. Get the area and year with the highest waiting list count
            max_waiting_list = get_max_waiting_list(cursor)
            print("\nArea with the highest waiting list:")
            print(f"Area Code: {max_waiting_list[0][0]}, Year: {max_waiting_list[0][1]}, Households: {max_waiting_list[0][2]}")

            # 4. Get the area and year with the lowest waiting list count
            min_waiting_list = get_min_waiting_list(cursor)
            print("\nArea with the lowest waiting list:")
            print(f"Area Code: {min_waiting_list[0][0]}, Year: {min_waiting_list[0][1]}, Households: {min_waiting_list[0][2]}")

            # 5. Get housing supply statistics
            housing_stats = get_housing_units_statistics(cursor)
            print("\nHousing Units Statistics:")
            print(f"Total Units: {housing_stats[0][0]}, Average Units: {housing_stats[0][1]:.2f}, "
                  f"Min Units: {housing_stats[0][2]}, Max Units: {housing_stats[0][3]}")

        except ValueError as e:
            print(f"Invalid input: {e}")
        finally:
            # Close the connection
            conn.close()
