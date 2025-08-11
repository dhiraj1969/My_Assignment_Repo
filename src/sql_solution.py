import argparse
import sqlite3
import csv

def main():
    # Argument parsing
    p = argparse.ArgumentParser(description="SQL-based solution for total quantities of items purchased by customers aged 18-35.")
    p.add_argument("--db", required=True, help="SQLite database file")
    p.add_argument("--out", default="output_sql.csv", help="Output CSV file")
    args = p.parse_args()

    # Connect to the database
    conn = sqlite3.connect(args.db)
    cursor = conn.cursor()

    # SQL query to get total quantities for customers aged 18-35
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

    # Execute query and fetch results
    cursor.execute(query)
    rows = cursor.fetchall()

    # Write to CSV file
    with open(args.out, "w", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Customer", "Age", "Item", "Quantity"])
        for row in rows:
            writer.writerow(row)

    # Close the connection
    conn.close()

if _name_ == "_main_":
    main()
