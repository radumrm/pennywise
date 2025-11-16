# PennyWise --- Project Specification

## Introduction

PennyWise is a web application developed in Python with Flask, designed
to help users track their card expenses and visualize transactions
clearly. Each user can create an account, add cards, and manually enter
transactions for each card. Data is stored in Firebase, and the
application provides pages for authentication, card management, and a
dashboard with charts that group transactions by categories (food,
subscriptions, transport, etc.).

## Main Features

-   Simple web interface based on Flask + Jinja2 (HTML/CSS/Bootstrap).
-   User authentication and account management (profile, password,
    logout).
-   Main page displays the user's cards and associated transactions;
    ability to add/delete cards.
-   Manual entry of transactions: amount, date, description, category,
    and associated card.
-   Data persistence in Firebase.
-   Dashboard with category aggregation and pie chart visualizations.

## Target Audience

The application is aimed at individuals who want to track their expenses
easily and quickly, such as students or users with multiple cards. All
transactions are entered manually; the application does not integrate
directly with bank accounts.

## Technologies and Constraints

-   **Backend:** Python + Flask\
-   **Templating:** Jinja2\
-   **Frontend:** HTML, CSS, Bootstrap; charts generated server-side\
-   **Database:** Firebase, maximum 1GB of data\
-   **Hosting:** Docker container\
-   **Security:** hashed passwords

------------------------------------------------------------------------

## System Overview

### Client (Frontend)

-   Pages rendered server-side (login, main page, dashboard)
-   HTML forms for user interactions

### Server (Backend)

-   Flask exposes routes for authentication, CRUD operations on cards
    and transactions, and dashboard endpoints

### Database and External Services

-   Firebase Firestore for storing transactions, cards and user data

### Communication

-   HTTPS traffic between client and server
-   Access to Firebase via Admin SDK for secure operations

### Languages and Libraries

-   **Python:** Flask, firebase-admin, python-dotenv\
-   **Frontend:** Bootstrap\
-   **Other tools:** Docker

------------------------------------------------------------------------

## Detailed Component Design

### 1. Auth (Authentication and Account)

-   **Functionality:** registration, login, logout, view/edit profile\
-   **Endpoints:** `/register`, `/login`, `/logout`, `/account`\
-   Passwords hashed and stored in Firebase

### 2. Cards & Transactions

-   **Functionality:** add, modify, delete cards and transactions\
-   **Database structure:**
    `users/{user_id}/cards/{card_id}/transactions/{txn_id}`\
-   **Endpoints:** `/cards`, `/cards/<id>/transactions`,
    `/transactions/<id>/delete`

### 3. Dashboard

-   **Functionality:** aggregate transactions by category and display
    pie charts\
-   Charts generated server-side and displayed as static images\
-   Aggregation calculations done on the server for efficiency

### 4. Persistence and Database Access

-   Secure interactions using Firebase Admin SDK

### 5. UI & UX

-   Simple flow: login → main page → dashboard\
-   Reusable components for cards and transactions\
-   Visual feedback for successful operations or errors

------------------------------------------------------------------------

## Conclusion

PennyWise is a moderately complex project combining authentication,
CRUD, and data visualization. Critical aspects include password
security, database structure, and server-side aggregation calculations
for the dashboard. Required knowledge includes Python/Flask and
Firestore. Charts and the interface work entirely server-side.
