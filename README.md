# My_Assignment_Repo
# Eastvantage - Assignment solution

This repository contains a Python script that solves the assignment:
- Connects to a provided SQLite3 DB
- Extracts total quantities of each item bought by customers aged 18-35
- Produces a CSV with semicolon delimiter and no decimal quantities
- Two solutions included: SQL-only and Pandas

Files
- assignment_solution.py : main script

Usage
1. (Optional) create test DB:
   python assignment_solution.py --create-test-db test.db

2. Run SQL-only solution:
   python assignment_solution.py --db test.db --out result_sql.csv --method sql

3. Run Pandas solution:
   python assignment_solution.py --db test.db --out result_pandas.csv --method pandas

Output CSV columns:
Customer;Age;Item;Quantity

Notes
- Script attempts to auto-detect schema:
  - **Wide schema** (sales table with qty_x, qty_y, qty_z columns)
  - **Normalized schema** (order_items table with item + quantity rows)
- If your DB schema differs, minor adaptation of column/table names in the script may be required.

