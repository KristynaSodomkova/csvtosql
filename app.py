import sqlite3
from flask import Flask, request, render_template
import csv

app = Flask(__name__)


app.config['DEBUG'] = True
# make the data from tuple into dict
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# display the data on page
@app.route('/transactions', methods=['GET', 'POST'])
def display_transactions():
    if request.method == 'POST':
        file = request.files['file']

        # connect to the database
        connection = sqlite3.connect("banking.db")
        connection.row_factory = dict_factory
        cursor = connection.cursor()

        # read the csv file and insert the data into the database, print how many records were added
        records = 0
        reader = file.readlines()
        for row in reader:
            row = row.decode("utf-8").split(',')
            cursor.execute("INSERT OR REPLACE INTO TransactionsTable VALUES (?,?,?,?,?)", row)
            connection.commit()
            records += 1

        # delete the possible first row with column names
        cursor.execute("DELETE from TransactionsTable WHERE reference='reference' ")
        connection.commit()

        # fetch the results
        results = cursor.fetchall()


        # close the cursor and connection
        cursor.close()
        connection.close()

        # return a response indicating that the file has been successfully uploaded
        print("\n{} Records Transferred".format(records))
        return render_template('transactions.html', transactions=results)

    # select all data from the table and fetch them into results
    connection = sqlite3.connect("banking.db")
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM TransactionsTable ORDER BY timestamp DESC")
    results = cursor.fetchall()

    # select the max amount
    max_amount = cursor.execute("SELECT MAX(amount) FROM TransactionsTable").fetchone()
    max_amount = max_amount['MAX(amount)']

    # close the cursor and connection
    cursor.close()
    connection.close()

    # pass the results to the template
    return render_template('transactions.html', transactions=results, max_amount=max_amount)


if __name__ == '__main__':
    app.run()
