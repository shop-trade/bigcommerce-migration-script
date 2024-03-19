import requests
import csv

# Replace these with your actual BigCommerce API credentials
CLIENT_ID = 'replace'
ACCESS_TOKEN = 'replace'
STORE_HASH = 'replace'

# Corrected BigCommerce API URL for fetching gift cards
BASE_API_URL = f'https://api.bigcommerce.com/stores/{STORE_HASH}/v2/gift_certificates'

# Set up the headers with our API credentials
headers = {
    'X-Auth-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def fetch_gift_cards():
    gift_cards = []
    page = 1
    limit = 50  # Adjust based on what the API supports
    while True:
        url = f'{BASE_API_URL}?page={page}&limit={limit}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if not data:
                # No more data to fetch
                break
            gift_cards.extend(data)
            page += 1
        else:
            print(f"Failed to fetch gift cards: {response.status_code}")
            break
    return gift_cards

def save_to_csv(gift_cards):
    with open('gift_cards.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'ID', 'Code', 'Amount', 'Status', 'Balance', 'To Name', 
            'Order ID', 'Template', 'Message', 'To Email', 'From Name', 
            'From Email', 'Customer ID', 'Expiry Date', 'Purchase Date', 
            'Currency Code'
        ])
        
        for card in gift_cards:
            writer.writerow([
                card.get('id'), card.get('code'), card.get('amount'), card.get('status'), 
                card.get('balance'), card.get('to_name'), card.get('order_id'), 
                card.get('template'), card.get('message'), card.get('to_email'), 
                card.get('from_name'), card.get('from_email'), card.get('customer_id'), 
                card.get('expiry_date'), card.get('purchase_date'), card.get('currency_code')
            ])

def main():
    gift_cards = fetch_gift_cards()
    if gift_cards:
        save_to_csv(gift_cards)
        print("Gift cards have been successfully saved to 'gift_cards.csv'")
    else:
        print("No gift cards to save or failed to fetch gift cards.")

if __name__ == "__main__":
    main()
