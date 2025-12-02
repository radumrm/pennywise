from firebase_setup import get_database
from google.cloud.firestore_v1 import ArrayUnion
from db_user import hash

db = get_database()

# create a card for a user
def create_card(email, title, bank):
    user_doc = db.collection("accounts").document(email)
    if not user_doc.get().exists:
        print("Account doesn't exist")
        return None

    card_ref = user_doc.collection("cards").document()
    card_id = card_ref.id
    
    card_ref.set({
        "id": card_id,
        "title": title,
        "bank": bank,
    })
    return card_id


# list all cards for a user (returns list of dicts)
def get_cards(email):
    user_doc = db.collection("accounts").document(email)
    if not user_doc.get().exists:
        print("Account doesn't exist")
        return None

    cards_col = user_doc.collection("cards").stream()
    cards = [c.to_dict() for c in cards_col]
    return cards


# get one card by id
def get_card(email, card_id):
    card_doc = db.collection("accounts").document(email).collection("cards").document(card_id).get()
    if not card_doc.exists:
        print("Card not found")
        return None
    return card_doc.to_dict()


# update card fields (title/bank)
def update_card(email, card_id, title=None, bank=None):
    card_ref = db.collection("accounts").document(email).collection("cards").document(card_id)
    if not card_ref.get().exists:
        print("Card not found")
        return False

    update_data = {}
    if title is not None:
        update_data["title"] = title
    if bank is not None:  # Changed from 'content' to 'bank'
        update_data["bank"] = bank

    if not update_data:
        return False

    card_ref.update(update_data)
    return True


# delete a single card
def delete_card(email, card_id):
    card_ref = db.collection("accounts").document(email).collection("cards").document(card_id)
    if not card_ref.get().exists:
        print("Card not found")
        return False
    card_ref.delete()
    return True