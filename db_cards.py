from firebase_setup import get_database
import hashlib

db = get_database()

def hash_pin(pin):
    return hashlib.sha256(pin.encode('utf-8')).hexdigest()

def create_card(email, IBAN, bank, card_holder_name, initial_sum, PIN, card_name, card_number, expiration_date):
    card_ref = db.collection("accounts").document(email).collection("cards").document(IBAN)

    if card_ref.get().exists:
        print("Card already exists for this user")
        return False
    
    card_ref.set({
        "IBAN" : IBAN,
        "bank" : bank,
        "card_holder_name" : card_holder_name,
        "sum" : initial_sum,
        "PIN" : hash_pin(PIN),
        "card_name": card_name,
        "card_number": card_number,
        "expiration_date": expiration_date
    })
    return True

def get_user_cards(email):
    cards_ref = db.collection("accounts").document(email).collection("cards")
    docs = cards_ref.stream()
    
    cards_list = []
    for doc in docs:
        cards_list.append(doc.to_dict())
        
    return cards_list

def delete_card(email, IBAN):
    card_ref = db.collection("accounts").document(email).collection("cards").document(IBAN)
    
    if card_ref.get().exists:
        card_ref.delete()
        return True
    return False

def get_card_details(email, IBAN):
    card_ref = db.collection("accounts").document(email).collection("cards").document(IBAN)
    doc = card_ref.get()
    
    if doc.exists:
        return doc.to_dict()
    return None