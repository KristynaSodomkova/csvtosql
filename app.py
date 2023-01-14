import sqlite3
from flask import Flask, request, render_template
import csv

app = Flask(__name__)

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

        # read the csv file and insert the data into the database
        records = 0
        reader = csv.reader(file)
        for row in reader:
            cursor.execute("INSERT OR REPLACE INTO TransactionsTable VALUES (?,?,?,?,?)", row)
            connection.commit()
            records += 1

        # delete the possible first row with column names
        cursor.execute("DELETE from TransactionsTable WHERE reference='reference' ")
        connection.commit()

        # close the cursor and connection
        cursor.close()
        connection.close()

        #return a response indicating that the file has been successfully uploaded
        print("\n{} Records Transferred".format(records))

    else:
        # select all data from the table and fetch them into results
        connection = sqlite3.connect("banking.db")
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM TransactionsTable ORDER BY timestamp DESC")
        results = cursor.fetchall()

        # close the cursor and connection
        cursor.close()
        connection.close()

        # pass the results to the template
        return render_template('transactions.html', transactions=results)

if __name__ == '__main__':
    app.run()