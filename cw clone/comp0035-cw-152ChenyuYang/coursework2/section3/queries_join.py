import sqlite3
from pathlib import Path

# Define the database path
base_dir = Path(__file__).resolve().parent
db_path = base_dir.parents[1] / "coursework1" / "database" / "local_authority_housing.db"

# Connect to the database
def get_db_connection(db_path):
    """Establish a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Failed to connect to the database: {e}")
        return None, None

# Execute SELECT queries
def execute_select_query(cursor, sql, params=None):
    """
    Execute a SELECT query and return the results.
    :param cursor: SQLite cursor
    :param sql: SQL query string
    :param params: Query parameters
    :return: Query results
    """
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Query failed: {e}")
        return None

# Dynamic query function
def get_filtered_area_and_year(cursor, area_name=None, year=None):
    """
    Query dynamically based on area name and year.
    If a parameter is not provided, it will not filter that field.
    """
    base_sql = """
    SELECT Area.area_name, Year.year
    FROM Area
    CROSS JOIN Year
    """
    filters = []
    params = []

    # Dynamically add filter conditions
    if area_name:
        filters.append("LOWER(Area.area_name) = LOWER(?)")  # Case-insensitive
        params.append(area_name)
    if year:
        filters.append("Year.year = ?")
        params.append(year)

    # If there are filters, append them to the SQL statement
    if filters:
        base_sql += " WHERE " + " AND ".join(filters)

    base_sql += " ORDER BY Area.area_name, Year.year;"

    # Debugging information
    print("Executing SQL:", base_sql)
    print("With Parameters:", params)

    return execute_select_query(cursor, base_sql, params=params)

# Main program
if __name__ == "__main__":
    if not db_path.exists():
        print(f"Database file not found: {db_path}")
    else:
        conn, cursor = get_db_connection(db_path)
        if conn is None or cursor is None:
            print("Failed to connect to the database. Program terminated.")
        else:
            try:
                # Dynamically input area name and year
                print("Please enter the area name (leave blank for no filter):")
                area_name = input("Area name: ").strip()
                area_name = area_name if area_name else None

                print("Please enter the year (leave blank for no filter):")
                year_input = input("Year: ").strip()
                year = int(year_input) if year_input else None

                # Execute the query
                results = get_filtered_area_and_year(cursor, area_name, year)

                # Output the results
                if results:
                    print("\nQuery Results:")
                    for row in results:
                        print(row)
                else:
                    print("\nNo matching data found.")

            except ValueError as e:
                print(f"Input error: {e}")
            finally:
                # Close the database connection
                conn.close()
