import requests
import csv

# Replace these with your actual BigCommerce API credentials
CLIENT_ID = 'Replace'
ACCESS_TOKEN = 'Replace'
STORE_HASH = 'replace'

# BigCommerce API URL for fetching gift cards, without the page and limit parameters
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
        writer.writerow(['ID', 'Code', 'To Name', 'To Email', 'From Name', 'From Email', 'Amount', 'Balance', 'Status'])
        
        for card in gift_cards:
            writer.writerow([
                card.get('id'), card.get('code'), card.get('to_name'), card.get('to_email'), 
                card.get('from_name'), card.get('from_email'), card.get('amount'), 
                card.get('balance'), card.get('status')
            ])

def main():
    gift_cards = fetch_gift_cards()
    if gift_cards:
        save_to_csv(gift_cards)
        print(f"Gift cards have been saved to 'gift_cards.csv'. Total records: {len(gift_cards)}")
    else:
        print("No gift cards to save.")

if __name__ == "__main__":
    main()
