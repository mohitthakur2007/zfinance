from flask import Flask, render_template, request, redirect, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # You may want to handle password more securely
        session['username'] = username
        return redirect('/add-expense')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # You may want to handle password more securely
        session['username'] = username
        # Create user files
        with open(f"data/expenses_{username}.txt", 'w') as f, \
             open(f"data/budgets_{username}.txt", 'w') as f2, \
             open(f"data/reminders_{username}.txt", 'w') as f3:
            pass  # Create empty files for new user
        return redirect('/add-expense')

    return render_template('signup.html')

@app.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    if 'username' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        category = request.form['category']
        amount = request.form['amount']
        date = request.form['date']
        description = request.form['description']
        payment_method = request.form['payment_method']
        recurring = 'recurring' in request.form
        frequency = request.form.get('frequency', 'None')

        with open(f"data/expenses_{session['username']}.txt", 'a') as f:
            f.write(f"{category},{amount},{date},{description},{payment_method},{recurring},{frequency}\n")
        flash("Expense added successfully")
        return redirect('/add-expense')
    
    return render_template('add_expense.html')

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if 'username' not in session:
        return redirect('/login')

    budgets = {}
    spending = {}

    if request.method == 'POST':
        category = request.form['category']
        budget_amount = request.form['budget_amount']

        with open(f"data/budgets_{session['username']}.txt", 'a') as f:
            f.write(f"{category},{budget_amount}\n")
        flash("Budget set successfully")
        return redirect('/budget')

    # Load budgets
    try:
        with open(f"data/budgets_{session['username']}.txt", 'r') as f:
            for line in f:
                cat, amount = line.strip().split(',')
                budgets[cat] = float(amount)
    except FileNotFoundError:
        pass

    # Calculate spending
    try:
        with open(f"data/expenses_{session['username']}.txt", 'r') as f:
            for line in f:
                cat, amount, *_ = line.strip().split(',')
                if cat in spending:
                    spending[cat] += float(amount)
                else:
                    spending[cat] = float(amount)
    except FileNotFoundError:
        pass

    return render_template('budget.html', budgets=budgets, spending=spending)

@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    if 'username' not in session:
        return redirect('/login')

    reminders = []

    if request.method == 'POST':
        reminder_type = request.form['reminder_type']
        message = request.form['message']
        date = request.form['date']

        with open(f"data/reminders_{session['username']}.txt", 'a') as f:
            f.write(f"{reminder_type},{message},{date}\n")
        flash("Reminder set successfully")
        return redirect('/notifications')

    try:
        with open(f"data/reminders_{session['username']}.txt", 'r') as f:
            for line in f:
                reminder_type, message, date = line.strip().split(',')
                reminders.append((reminder_type, message, date))
    except FileNotFoundError:
        pass

    return render_template('notifications.html', reminders=reminders)

@app.route('/delete-reminder/<int:reminder_id>')
def delete_reminder(reminder_id):
    if 'username' not in session:
        return redirect('/login')

    # Load reminders
    reminders = []
    with open(f"data/reminders_{session['username']}.txt", 'r') as f:
        reminders = f.readlines()

    # Remove the selected reminder
    if 0 <= reminder_id < len(reminders):
        del reminders[reminder_id]

    # Save back the modified reminders
    with open(f"data/reminders_{session['username']}.txt", 'w') as f:
        f.writelines(reminders)

    flash("Reminder deleted successfully")
    return redirect('/notifications')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)  # Create data directory if it doesn't exist
    app.run(debug=True)
