import argparse
import sqlite3
import csv
import os

def create_test_db(db_file):
    """Creates a sample SQLite test database with Customers, Items, and Sales data."""
    if os.path.exists(db_file):
        os.remove(db_file)  # Start fresh

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE Customers (
        CustomerID INTEGER PRIMARY KEY,
        Age INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE Items (
        ItemID INTEGER PRIMARY KEY,
        ItemName TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE Sales (
        SaleID INTEGER PRIMARY KEY,
        CustomerID INTEGER,
        ItemID INTEGER,
        Quantity INTEGER,
        FOREIGN KEY(CustomerID) REFERENCES Customers(CustomerID),
        FOREIGN KEY(ItemID) REFERENCES Items(ItemID)
    )
    """)

    # Insert sample data
    customers = [(1, 21), (2, 23), (3, 35), (4, 40)]
    cursor.executemany("INSERT INTO Customers VALUES (?, ?)", customers)

    items = [(1, 'x'), (2, 'y'), (3, 'z')]
    cursor.executemany("INSERT INTO Items VALUES (?, ?)", items)

    sales = [
        (1, 1, 1, 5),  # Customer 1 buys 5 x
        (2, 1, 1, 5),  # Customer 1 buys 5 x again
        (3, 2, 1, 1),  # Customer 2 buys 1 x
        (4, 2, 2, 1),  # Customer 2 buys 1 y
        (5, 2, 3, 1),  # Customer 2 buys 1 z
        (6, 3, 3, 1),  # Customer 3 buys 1 z
        (7, 3, 3, 1),  # Customer 3 buys 1 z again
        (8, 4, 1, 10)  # Customer 4 is outside age range
    ]
    cursor.executemany("INSERT INTO Sales VALUES (?, ?, ?, ?)", sales)

    conn.commit()
    conn.close()
    print(f"Test database '{db_file}' created successfully.")

def run_sql_query(db_file, out_file):
    """Runs the SQL query and outputs to CSV."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    query = """
    SELECT c.CustomerID AS Customer,
           c.Age,
           i.ItemName AS Item,
           SUM(s.Quantity) AS Quantity
    FROM Customers c
    JOIN Sales s ON c.CustomerID = s.CustomerID
    JOIN Items i ON s.ItemID = i.ItemID
    WHERE c.Age BETWEEN 18 AND 35
      AND s.Quantity IS NOT NULL
    GROUP BY c.CustomerID, c.Age, i.ItemName
    HAVING SUM(s.Quantity) > 0
    ORDER BY c.CustomerID;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    with open(out_file, "w", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Customer", "Age", "Item", "Quantity"])
        for row in rows:
            writer.writerow(row)

    conn.close()
    print(f"Results written to '{out_file}'.")

def main():
    p = argparse.ArgumentParser(description="SQL-based solution for total quantities of items purchased by customers aged 18-35.")
    p.add_argument("--db", required=True, help="SQLite database file")
    p.add_argument("--out", default="output_sql.csv", help="Output CSV file")
    p.add_argument("--create-test-db", action="store_true", help="Create a test database with sample data")
    args = p.parse_args()

    if args.create_test_db:
        create_test_db(args.db)
    else:
        run_sql_query(args.db, args.out)

if __name__ == "__main__":
    main()

