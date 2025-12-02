import firebase_admin
from firebase_admin import credentials

from db_user import create_account, delete_account, login, change_name, change_password, change_email
from db_cards import create_card, get_card, get_cards


# -------------------------------------
# 1. CREATE TWO ACCOUNTS
# -------------------------------------

print("Creating accounts...")

create_account("user1@test.com", "User One", "pass123")
create_account("user2@test.com", "User Two", "pass456")

print("Accounts created.\n")


# -------------------------------------
# 2. LOGIN TEST
# -------------------------------------

print("Logging in users...")

u1 = login("user1@test.com", "pass123")
u2 = login("user2@test.com", "pass456")

print("User1:", u1)
print("User2:", u2, "\n")


# -------------------------------------
# 3. CREATE CARDS FOR EACH USER
# -------------------------------------

print("Creating cards...")

create_card("user1@test.com", "Card 1 - U1", "This is the first card of user 1")
create_card("user1@test.com", "Card 2 - U1", "This is the second card of user 1")

create_card("user2@test.com", "Card 1 - U2", "This is the first card of user 2")
create_card("user2@test.com", "Card 2 - U2", "This is the second card of user 2")

print("Cards created.\n")


# -------------------------------------
# 4. READ BACK CARDS
# -------------------------------------

print("Reading cards...")

cards_u1 = get_cards("user1@test.com")
cards_u2 = get_cards("user2@test.com")

print("\nUser 1 Cards:")
for c in cards_u1:
    print(c)

print("\nUser 2 Cards:")
for c in cards_u2:
    print(c)


# -------------------------------------
# 5. OPTIONAL CLEANUP (UNCOMMENT IF NEEDED)
# -------------------------------------
"""
delete_account("user1@test.com", "pass123")
delete_account("user2@test.com", "pass456")
"""
