from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages


# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('crm.db')
    conn.row_factory = sqlite3.Row  # Allows dictionary-like access to columns
    return conn


# Homepage - Display customers
@app.route('/')
def index():
    try:
        with get_db_connection() as conn:
            customers = conn.execute("SELECT * FROM customers").fetchall()
        return render_template('project.html', customers=customers)
    except Exception as e:
        flash(f"Error loading data: {str(e)}", "danger")
        return render_template('project.html', customers=[])


# Route to add a new customer
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            # Get form data
            date = request.form['date']
            name = request.form['name']
            phone_number = request.form['phone_number']
            appointment = request.form['appointment']
            project_area = request.form['project_area']
            description = request.form['description']

            # Validate input (Basic check: Ensure fields are not empty)
            if not (date and name and phone_number and appointment and project_area and description):
                flash("All fields are required!", "warning")
                return redirect(url_for('add'))

            # Insert into database
            with get_db_connection() as conn:
                conn.execute('''
                    INSERT INTO customers (date, name, phone_number, appointment, project_area, description) 
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (date, name, phone_number, appointment, project_area, description))
                conn.commit()

            flash("Customer added successfully!", "success")
            return redirect(url_for('index'))

        except Exception as e:
            flash(f"Error adding customer: {str(e)}", "danger")
            return redirect(url_for('add'))

    return render_template('add.html')


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


