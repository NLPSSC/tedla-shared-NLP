import sqlite3

db_path = r"Z:\_\active\nlpssc\Tedla - VUMC\nlp_Tdla\output\imported_output\results\results_20260325_155054\results_0.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(results);")
columns = cursor.fetchall()
columns.append("Description")
conn.close()

# Print markdown table header (fixed widths)
col_width = 40
type_width = 12
description_width = 60

header = f"| {'Column'.ljust(col_width)} | {'Type'.ljust(type_width)} | {'Description'.ljust(description_width)} |"
separator = f"|{'-' * (col_width + 2)}|{'-' * (type_width + 2)}|{'-' * (description_width + 2)}|"

print("\"results\" table schema:")
print()
print(header)
print(separator)
for col in columns:
    name = str(col[1]).ljust(col_width)
    ctype = str(col[2]).ljust(type_width)
    desc = ""
    print(f"| {name} | {ctype} | {desc.ljust(description_width)} |")
