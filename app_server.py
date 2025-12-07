from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import date

from db_user import login, get_user_by_email, create_account
from db_cards import create_card, get_user_cards, delete_card
from db_transactions import add_transaction, get_user_transactions
from db_reports import get_chart_data, get_category_spending

app = Flask(__name__)
app.secret_key = "cheie_secreta_pennywise"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_route'

class User(UserMixin):
    def __init__(self, email, name):
        self.id = email
        self.name = name

@login_manager.user_loader
def load_user(user_email):
    user_data = get_user_by_email(user_email)
    if user_data:
        return User(email=user_data['email'], name=user_data['name'])
    return None

def detect_bank_from_iban(iban):
    clean_iban = iban.replace(" ", "").upper()
    if len(clean_iban) < 8:
        return "Unknown Bank"
    bank_code = clean_iban[4:8]
    banks = {
        "BTRL": "Banca Transilvania", "RNCB": "BCR", "RZBR": "Raiffeisen Bank",
        "INGB": "ING Bank", "REVO": "Revolut", "BRDE": "BRD",
        "UGBI": "Garanti Bank", "BACX": "UniCredit Bank", "TREZ": "State Treasury"
    }
    return banks.get(bank_code, "Other Bank (" + bank_code + ")")

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_route'))

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = login(email, password)
        if user_data:
            user_obj = User(email=user_data['email'], name=user_data['name'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect Email or Password!", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeatPassword')
        name = f"{first_name} {last_name}"
        if password != repeat_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register_route'))
        success = create_account(email, name, password)
        if success:
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for('login_route'))
        else:
            flash("Error creating account. Email might already exist.", "danger")
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        user_cards = get_user_cards(current_user.id)
    except:
        user_cards = []
    
    # Existing range filter
    days_range = request.args.get('range', '30')
    try:
        days_range = int(days_range)
    except ValueError:
        days_range = 30
        
    # NEW: Get the card filter from URL, default to 'all'
    selected_card = request.args.get('card', 'all')
        
    try:
        # Pass selected_card to the database functions
        chart_labels, chart_values = get_chart_data(current_user.id, days_range, selected_card)
        cat_labels, cat_values = get_category_spending(current_user.id, selected_card)
    except Exception as e:
        raise e
    
    return render_template('index.html', 
                           name=current_user.name, 
                           cards=user_cards,
                           chart_labels=chart_labels,
                           chart_values=chart_values,
                           cat_labels=cat_labels,
                           cat_values=cat_values,
                           current_range=days_range,
                           selected_card=selected_card) # Pass this to template to show active state

@app.route('/cards')
@login_required
def view_cards_route():
    user_cards = get_user_cards(current_user.id)
    return render_template('cards.html', name=current_user.name, cards=user_cards)

@app.route('/add_card', methods=['GET', 'POST'])
@login_required
def add_card_route():
    if request.method == 'POST':
        iban = request.form.get('iban').strip().upper()
        if len(iban) != 24:
            flash("Invalid IBAN! It must be exactly 24 characters.", "danger")
            return render_template('add_card.html')
        
        bank = detect_bank_from_iban(iban)
        card_name = request.form.get('card_name')
        card_number = request.form.get('card_number').replace(" ", "")
        expiration_date = request.form.get('expiration_date')
        
        if len(card_number) != 16 or not card_number.isdigit():
             flash("Invalid Card Number! It must be 16 digits.", "danger")
             return render_template('add_card.html')

        holder = request.form.get('card_holder_name')
        try:
            initial_sum = float(request.form.get('initial_sum'))
        except ValueError:
            flash("Invalid amount entered!", "danger")
            return render_template('add_card.html')
            
        pin = request.form.get('pin')
        success = create_card(current_user.id, iban, bank, holder, initial_sum, pin, card_name, card_number, expiration_date)

        if success:
            flash(f"{card_name} added successfully!", "success")
            return redirect(url_for('view_cards_route')) 
        else:
            flash("Error: This IBAN already exists!", "danger")

    return render_template('add_card.html')

@app.route('/delete_card/<string:iban>')
@login_required
def delete_card_route(iban):
    success = delete_card(current_user.id, iban)
    if success:
        flash(f"Card {iban} deleted successfully.", "success")
    else:
        flash("Error deleting card.", "danger")
    return redirect(url_for('view_cards_route'))

@app.route('/transactions')
@login_required
def history_route():
    transactions = get_user_transactions(current_user.id)
    return render_template('history.html', name=current_user.name, transactions=transactions)

@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction_route():
    if request.method == 'POST':
        amount = request.form.get('amount')
        trans_type = request.form.get('type')
        date_val = request.form.get('date')
        card_iban = request.form.get('card_iban')
        description = request.form.get('description')
        
        if trans_type == "income":
            category = request.form.get('category_income')
        else:
            category = request.form.get('category_expense')

        if not category:
            flash("Please select a category!", "danger")
            return redirect(url_for('add_transaction_route'))

        success = add_transaction(current_user.id, amount, trans_type, category, date_val, card_iban, description)
        
        if success:
            flash("Transaction added and balance updated!", "success")
            return redirect(url_for('history_route'))
        else:
            flash("Error adding transaction.", "danger")

    user_cards = get_user_cards(current_user.id)
    return render_template('add_transaction.html', name=current_user.name, cards=user_cards, today=date.today())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_route'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)