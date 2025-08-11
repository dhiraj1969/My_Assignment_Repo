import argparse
import sqlite3
import pandas as pd

def main():
    # Argument parsing
    p = argparse.ArgumentParser(description="Pandas-based solution for total quantities of items purchased by customers aged 18-35.")
    p.add_argument("--db", required=True, help="SQLite database file")
    p.add_argument("--out", default="output_pandas.csv", help="Output CSV file")
    args = p.parse_args()

    # Connect to the database
    conn = sqlite3.connect(args.db)

    # Load tables into pandas DataFrames
    customers = pd.read_sql("SELECT * FROM Customers", conn)
    sales = pd.read_sql("SELECT * FROM Sales", conn)
    items = pd.read_sql("SELECT * FROM Items", conn)

    # Merge DataFrames
    df = sales.merge(customers, on="CustomerID").merge(items, on="ItemID")

    # Filter data for customers aged 18-35 and non-null quantities
    df = df[(df["Age"].between(18, 35)) & (df["Quantity"].notna())]

    # Group by customer, item and sum quantities
    df_grouped = df.groupby(["CustomerID", "Age", "ItemName"], as_index=False)["Quantity"].sum()

    # Exclude zero quantities
    df_grouped = df_grouped[df_grouped["Quantity"] > 0]

    # Save to CSV
    df_grouped.rename(columns={"CustomerID": "Customer", "ItemName": "Item"}, inplace=True)
    df_grouped.to_csv(args.out, sep=";", index=False)

    # Close the connection
    conn.close()

if _name_ == "_main_":
    main()
