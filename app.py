from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
DATA_DIR = 'data'

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# User management functions
def save_user(username, password):
    with open(os.path.join(DATA_DIR, 'users.txt'), 'a') as file:
        file.write(f"{username},{password}\n")

def load_users():
    if not os.path.exists(os.path.join(DATA_DIR, 'users.txt')):
        return {}
    users = {}
    with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as file:
        for line in file:
            user, password = line.strip().split(',')
            users[user] = password
    return users

# Expense management functions
def save_expense(username, category, amount, date):
    with open(os.path.join(DATA_DIR, 'expenses.txt'), 'a') as file:
        file.write(f"{username},{category},{amount},{date}\n")

def load_expenses(username):
    if not os.path.exists(os.path.join(DATA_DIR, 'expenses.txt')):
        return []
    expenses = []
    with open(os.path.join(DATA_DIR, 'expenses.txt'), 'r') as file:
        for line in file:
            user, category, amount, date = line.strip().split(',')
            if user == username:
                expenses.append((category, float(amount), date))
    return expenses

# Budget management functions
def save_budget(username, category, budget_amount):
    with open(os.path.join(DATA_DIR, 'budgets.txt'), 'a') as file:
        file.write(f"{username},{category},{budget_amount}\n")

def load_budgets(username):
    if not os.path.exists(os.path.join(DATA_DIR, 'budgets.txt')):
        return {}
    budgets = {}
    with open(os.path.join(DATA_DIR, 'budgets.txt'), 'r') as file:
        for line in file:
            user, category, budget_amount = line.strip().split(',')
            if user == username:
                budgets[category] = float(budget_amount)
    return budgets

# Reminder management functions
def save_reminder(username, reminder_type, message, date):
    with open(os.path.join(DATA_DIR, 'reminders.txt'), 'a') as file:
        file.write(f"{username},{reminder_type},{message},{date}\n")

def load_reminders(username):
    if not os.path.exists(os.path.join(DATA_DIR, 'reminders.txt')):
        return []
    reminders = []
    with open(os.path.join(DATA_DIR, 'reminders.txt'), 'r') as file:
        for line in file:
            user, reminder_type, message, date = line.strip().split(',')
            if user == username:
                reminders.append((reminder_type, message, date))
    return reminders

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            flash('Username already exists!')
            return redirect(url_for('signup'))
        save_user(username, password)
        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if users.get(username) == password:
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        category = request.form['category']
        amount = request.form['amount']
        date = request.form['date']
        save_expense(session['username'], category, amount, date)
        flash('Expense added successfully!')
        return redirect(url_for('add_expense'))
    
    return render_template('add_expense.html')

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        category = request.form['category']
        budget_amount = request.form['budget_amount']
        save_budget(session['username'], category, budget_amount)
        flash('Budget set successfully!')
        return redirect(url_for('budget'))
    
    budgets = load_budgets(session['username'])
    return render_template('budget.html', budgets=budgets)

@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        reminder_type = request.form['reminder_type']
        message = request.form['message']
        date = request.form['date']
        save_reminder(session['username'], reminder_type, message, date)
        flash('Reminder set successfully!')
        return redirect(url_for('notifications'))
    
    reminders = load_reminders(session['username'])
    return render_template('notifications.html', reminders=reminders)

if __name__ == '__main__':
    app.run(debug=True)
