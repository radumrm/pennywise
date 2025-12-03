from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from db_user import login, get_user_by_email, create_account # Importam functiile tale
from db_cards import get_user_cards

app = Flask(__name__)
app.secret_key = "cheie_secreta_pennywise" # Schimba asta cu ceva random

# --- CONFIGURARE FLASK-LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_route' # Daca nu e logat, il trimite aici

# Clasa User (Ambalajul)
class User(UserMixin):
    def __init__(self, email, name):
        self.id = email
        self.name = name

@login_manager.user_loader
def load_user(user_email):
    # Aceasta functie ruleaza la fiecare click pentru a mentine userul logat
    user_data = get_user_by_email(user_email)
    if user_data:
        return User(email=user_data['email'], name=user_data['name'])
    return None

# --- RUTE ---

@app.route('/')
def home():
    # Daca intra pe prima pagina si e logat, il ducem la dashboard
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
        
        # Aici apelam functia ta din db_user.py
        user_data = login(email, password)
        
        if user_data:
            user_obj = User(email=user_data['email'], name=user_data['name'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash("Email sau parolă incorectă!", "danger") # Mesaj de eroare
            
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
            flash("Passwords don't match!", "danger")
            return redirect(url_for('register_route'))
        
        success = create_account(email, name, password)
        
        if success:
            flash("Account created successfully! You can log in now.", "success")
            return redirect(url_for('login_route'))
        else:
            flash("Error creating account. The email may already exist.", "danger")
            
    return render_template('register.html')

@app.route('/dashboard')
@login_required # <--- Protejeaza pagina
def dashboard():
    user_cards = get_user_cards(current_user.id)

    return render_template('index.html', name=current_user.name, cards=user_cards)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_route'))

if __name__ == '__main__':
    app.run(debug=True)
    