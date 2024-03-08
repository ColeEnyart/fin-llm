import sqlite3
from datetime import datetime

conn = sqlite3.connect('compliance.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY,
        document_name TEXT NOT NULL,
        date DATETIME NOT NULL
    )
''')
conn.commit()

first_quarter = datetime(2023, 3, 31)
second_quarter = datetime(2023, 6, 30)
third_quarter = datetime(2023, 9, 30)
fourth_quarter = datetime(2023, 12, 31)

documents_data = [
    ('Promissory Note', first_quarter),
    ('Deed of Trust', first_quarter),
    ('Regulatory Agreement', first_quarter),
    ('Financing Statement', first_quarter),
    ('Promissory Note', second_quarter),
    ('Deed of Trust', second_quarter),
    ('Regulatory Agreement', second_quarter),
    ('Financing Statement', second_quarter),
    ('Promissory Note', third_quarter),
    ('Deed of Trust', third_quarter),
    ('Regulatory Agreement', third_quarter),
    ('Financing Statement', third_quarter),
    ('Promissory Note', fourth_quarter),
    ('Deed of Trust', fourth_quarter),
    ('Regulatory Agreement', fourth_quarter),
    ('Financing Statement', fourth_quarter),
]

cursor.executemany("INSERT INTO documents (document_name, date) VALUES (?, ?)", documents_data)
conn.commit()

cursor.execute("SELECT * FROM documents")
rows = cursor.fetchall()
print(rows)
conn.close()