import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/transactions')
def display_transactions():

    # connecting to the database
    connection = sqlite3.connect("banking.db")
    connection.row_factory = dict_factory
    cursor = connection.cursor()

    # import from csv to sqlite
    with open('transactions.csv', 'r') as file:
        records = 0
        for row in file.readlines():
            cursor.execute("INSERT OR REPLACE INTO TransactionsTable VALUES (?,?,?,?,?)", row.split(","))
            connection.commit()
            records += 1

    # delete the possible first row with column names
    cursor.execute("DELETE from TransactionsTable WHERE reference='reference' ")
    connection.commit()

    # select all data from the table and fetch them into results
    cursor.execute("SELECT * FROM TransactionsTable ORDER BY timestamp DESC")
    results = cursor.fetchall()

    # close the cursor and connection
    cursor.close()
    connection.close()
    print("\n{} Records Transferred".format(records))

    # pass the results to the template
    return render_template('transactions.html', transactions=results)

if __name__ == '__main__':
    app.run()