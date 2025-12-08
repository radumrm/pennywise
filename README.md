# PennyWise

PennyWise is a modern and intuitive web application for managing and tracking personal financial transactions. The application allows users to monitor expenses and income, manage multiple bank cards, and analyze financial patterns through interactive charts and detailed reports.

## Features

### Authentication and Security
- **Complete authentication system** with login and registration
- **Secure session management** with Flask-Login
- **Password hashing** using SHA-256 for maximum security

### Card Management
- **Add multiple personal cards** with complete information (IBAN, card number, expiration date)
- **Automatic bank detection** based on IBAN code (Banca Transilvania, BCR, Raiffeisen, ING, Revolut, BRD)
- **Set initial balance** for each card
- **View and delete** existing cards

### Transaction Management
- **Manual transaction entry** (income and expenses)
- **Transaction categorization** (shopping, grocery, utilities, entertainment, etc.)
- **Assign transactions** to specific cards
- **Automatic balance update** for cards after each transaction
- **Complete history** of all transactions with filtering and sorting

### Analysis and Reports
- **Interactive charts** for expenses and income
- **Pie charts** for category distribution
- **Period filtering** (15, 30, 90 days and 1 year)
- **Card filtering** or aggregated view
- **Detailed reports** by expense categories

---

## Technologies Used

### Backend
- **Flask** - Python web framework for backend
- **Flask-Login** - Authentication and session management
- **Python** - Programming language

### Database
- **Firebase Firestore** - NoSQL cloud database for storing users, cards, and transactions
- **Firebase Admin SDK** - Firebase integration and management

### Frontend
- **HTML** - Page structure
- **CSS** - Styling
- **Bootstrap** - CSS framework for responsive design
- **Chart.js** - Library for generating charts and pie charts

---

## Project Structure

```
pennywise/
│
├── app_server.py              # Main Flask application
├── firebase_setup.py          # Firebase configuration and initialization
├── db_user.py                 # User management functions
├── db_cards.py                # Card management functions
├── db_transactions.py         # Transaction management functions
├── db_reports.py              # Report and chart generation functions
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
│
├── templates/                 # HTML templates
│   ├── index.html            # Main dashboard
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── cards.html            # Card list
│   ├── add_card.html         # Add card form
│   ├── history.html          # Transaction history
│   ├── add_transaction.html  # Add transaction form
│   └── 404.html              # 404 error page
│
└── static/                   # Static resources
```

---

## Running the Application

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**
   ```bash
   python app_server.py
   ```

3. **Access the application**
   - Open your browser at: `http://localhost:5000`
   - First time you'll need to register by creating a new account

---

## Usage

### 1. Create Account

1. Access the application in your browser
2. Click on "Register" or navigate to `/register`
3. Fill out the form:
   - First Name
   - Last Name
   - Email
   - Password
   - Repeat Password
4. Click "Register" to create the account

### 2. Login

1. Enter your email and password
2. Click "Login"
3. You will be automatically redirected to the dashboard

### 3. Add Card

1. From the sidebar, navigate to **Cards & Wallets** → **Add Card**
2. Fill in the information:
   - **Card Name** (e.g., "Main Card")
   - **IBAN** (24 characters, RO format...)
   - **Card Number** (16 digits)
   - **Expiration Date** (MM/YY)
   - **Card Holder Name**
   - **Initial Sum** (current available balance)
   - **PIN** (optional, for reference)
3. Click "Add Card"
4. The card will be added and appear in the card list

### 4. Add Transaction

1. From the sidebar, navigate to **Transactions** → **Add Transaction**
2. Select the type: **Income** or **Expense**
3. Fill in the details:
   - **Amount** (the amount)
   - **Date** (transaction date)
   - **Card** (select the card from dropdown)
   - **Category** (select the corresponding category)
   - **Description** (optional description)
4. Click "Add Transaction"
5. The card balance will be automatically updated

### 5. View Dashboard and Charts

1. The main dashboard (`/dashboard`) displays:
   - Charts for expenses/income over periods
   - Pie charts for category distribution
2. You can filter the data:
   - **Range**: Select the period (15, 30, 90 days and 1 year)
   - **Card**: Select a specific card or "All Cards"
   - **Type**: Select "Expense" or "Income"
3. Charts update automatically based on filters

### 6. View Transaction History

1. Navigate to **Transactions** → **History**
2. See all your transactions sorted chronologically
3. Each transaction displays: amount, type, category, card, date, description

### 7. Manage Cards

1. Navigate to **Cards & Wallets** → **View Cards**
2. See the list of all your cards with:
   - Card name
   - IBAN
   - Automatically detected bank
   - Current balance
3. You can delete cards using the "Delete" button

### 8. Logout

1. Click on your name or the logout button
2. You will be logged out and redirected to the login page
