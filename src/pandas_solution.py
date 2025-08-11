import argparse
import sqlite3
import pandas as pd
import os

def create_test_db(db_file):
    """Creates a sample SQLite test database with Customers, Items, and Sales data."""
    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

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

    customers = [(1, 21), (2, 23), (3, 35), (4, 40)]
    cursor.executemany("INSERT INTO Customers VALUES (?, ?)", customers)

    items = [(1, 'x'), (2, 'y'), (3, 'z')]
    cursor.executemany("INSERT INTO Items VALUES (?, ?)", items)

    sales = [
        (1, 1, 1, 5),
        (2, 1, 1, 5),
        (3, 2, 1, 1),
        (4, 2, 2, 1),
        (5, 2, 3, 1),
        (6, 3, 3, 1),
        (7, 3, 3, 1),
        (8, 4, 1, 10)
    ]
    cursor.executemany("INSERT INTO Sales VALUES (?, ?, ?, ?)", sales)

    conn.commit()
    conn.close()
    print(f"Test database '{db_file}' created successfully.")

def run_pandas_solution(db_file, out_file):
    """Runs the Pandas-based query and writes to CSV."""
    conn = sqlite3.connect(db_file)

    customers = pd.read_sql("SELECT * FROM Customers", conn)
    sales = pd.read_sql("SELECT * FROM Sales", conn)
    items = pd.read_sql("SELECT * FROM Items", conn)

    df = sales.merge(customers, on="CustomerID").merge(items, on="ItemID")
    df = df[(df["Age"].between(18, 35)) & (df["Quantity"].notna())]

    df_grouped = df.groupby(["CustomerID", "Age", "ItemName"], as_index=False)["Quantity"].sum()
    df_grouped = df_grouped[df_grouped["Quantity"] > 0]

    df_grouped.rename(columns={"CustomerID": "Customer", "ItemName": "Item"}, inplace=True)
    df_grouped.to_csv(out_file, sep=";", index=False)

    conn.close()
    print(f"Results written to '{out_file}'.")

def main():
    p = argparse.ArgumentParser(description="Pandas-based solution for total quantities of items purchased by customers aged 18-35.")
    p.add_argument("--db", required=True, help="SQLite database file")
    p.add_argument("--out", default="output_pandas.csv", help="Output CSV file")
    p.add_argument("--create-test-db", action="store_true", help="Create a test database with sample data")
    args = p.parse_args()

    if args.create_test_db:
        create_test_db(args.db)
    else:
        run_pandas_solution(args.db, args.out)

if __name__ == "__main__":
    main()

