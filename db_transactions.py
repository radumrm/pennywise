from firebase_setup import get_database
from google.cloud import firestore

db = get_database()

def add_transaction(email, amount, trans_type, category, date, card_iban):
    transaction_ref = db.collection("transactions").document()
    transaction_ref.set({
        "user_email": email,
        "amount": float(amount),
        "type": trans_type,
        "category": category,
        "date": date,
        "card_iban": card_iban
    })

    card_ref = db.collection("accounts").document(email).collection("cards").document(card_iban)
    card_doc = card_ref.get()
    
    if card_doc.exists:
        current_sum = float(card_doc.to_dict().get("sum", 0.0))
        
        if trans_type == "income":
            new_sum = current_sum + float(amount)
        else:
            new_sum = current_sum - float(amount)
            
        new_sum = round(new_sum, 2)
        
        card_ref.update({"sum": new_sum})
        return True
    return False

def get_user_transactions(email):
    transactions_ref = db.collection("transactions")
    query = transactions_ref.where("user_email", "==", email).order_by("date", direction=firestore.Query.DESCENDING)
    results = query.stream()
    
    trans_list = []
    for doc in results:
        data = doc.to_dict()
        data['id'] = doc.id
        trans_list.append(data)
        
    return trans_list