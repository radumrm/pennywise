from firebase_setup import get_database
from datetime import datetime, timedelta

db = get_database()

def get_chart_data(email, days_range, card_filter=None, trans_type='expense', selected_categories=None):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_range)
    
    transactions_ref = db.collection("transactions")
    start_str = start_date.strftime("%Y-%m-%d")
    
    query = transactions_ref.where("user_email", "==", email).where("type", "==", trans_type)
    
    if card_filter and card_filter != 'all':
        query = query.where("card_iban", "==", card_filter)

    if selected_categories:
        query = query.where("category", "in", selected_categories)

    query = query.where("date", ">=", start_str)
                            
    results = query.stream()
    
    data_map = {}
    
    group_by_month = (days_range == 365)
    group_by_week = (days_range == 90)

    for doc in results:
        data = doc.to_dict()
        amount = float(data.get("amount", 0.0))
        date_str = data.get("date")
        
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            
            if group_by_month:
                key = dt.month - 1
                data_map[key] = data_map.get(key, 0) + amount
            elif group_by_week:
                start_of_week = dt - timedelta(days=dt.weekday())
                week_key = start_of_week.strftime("%Y-%m-%d")
                data_map[week_key] = data_map.get(week_key, 0) + amount
            else:
                full_key = date_str
                data_map[full_key] = data_map.get(full_key, 0) + amount

        except ValueError:
            continue

    labels = []
    values = []
    
    if group_by_month:
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for i in range(12):
            labels.append(months[i])
            values.append(data_map.get(i, 0.0))
            
    elif group_by_week:
        current_pointer = start_date - timedelta(days=start_date.weekday())
        
        while current_pointer <= end_date + timedelta(days=6):
            week_key = current_pointer.strftime("%Y-%m-%d")
            
            week_end = current_pointer + timedelta(days=6)
            label_str = f"{current_pointer.strftime('%d %b')} - {week_end.strftime('%d %b')}"
            
            labels.append(label_str)
            values.append(data_map.get(week_key, 0.0))
            
            current_pointer += timedelta(days=7)
            
    else:
        delta = end_date - start_date
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")
            label_str = day.strftime("%d %b")
            
            labels.append(label_str)
            values.append(data_map.get(day_str, 0.0))

    return labels, values

def get_category_spending(email, days_range, card_filter=None, trans_type='expense', selected_categories=None):
    transactions_ref = db.collection("transactions")
    
    # CALCULAM DATA DE START
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_range)
    start_str = start_date.strftime("%Y-%m-%d")

    query = transactions_ref.where("user_email", "==", email).where("type", "==", trans_type)

    if card_filter and card_filter != 'all':
        query = query.where("card_iban", "==", card_filter)
        
    if selected_categories:
        query = query.where("category", "in", selected_categories)
        
    # FILTRARE NOUA DUPA DATA
    query = query.where("date", ">=", start_str)

    results = query.stream()
    
    categories = {}
    for doc in results:
        data = doc.to_dict()
        category = data.get("category", "Other")
        amount = float(data.get("amount", 0.0))
        categories[category] = categories.get(category, 0) + amount
    
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    
    if not sorted_categories:
        return [], []
    
    labels = [cat[0] for cat in sorted_categories]
    values = [cat[1] for cat in sorted_categories]
            
    return labels, values