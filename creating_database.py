import sqlite3

conn = sqlite3.connect("banking.db")
cur = conn.cursor()

sql = """
    CREATE TABLE TransactionsTable(
        reference TEXT,
        timestamp TEXT,
        amount INTEGER,
        currency TEXT,
        description TEXT,
        primary key(reference)
    )"""

cur.execute(sql)
print("TransactionTable has been created.")

conn.commit()
conn.close()