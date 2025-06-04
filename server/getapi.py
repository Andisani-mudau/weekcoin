import os
import json
import time
from flask_cors import CORS
from flask import Flask, jsonify, render_template
import requests
from dotenv import load_dotenv

app = Flask(__name__, template_folder='../views', static_folder='../static')
CORS(app)

load_dotenv()
api_key = os.getenv("API_KEY")

MEMECOINS_FILE = 'server/memecoins.json'
CACHE_LIFETIME = 7 * 24 * 60 * 60  # 7 days in seconds

with open('server/sponsored.txt', 'r') as file:
    sponsored_addresses = [line.strip() for line in file if line.strip()]

headers = {
    'accept': 'application/json',
    'X-API-Key': api_key
}

def fetch_token_metadata(addresses):
    tokens_data = []
    for address in addresses:
        metadata_url = f'https://solana-gateway.moralis.io/token/mainnet/{address}/metadata'
        response = requests.get(metadata_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            name = data.get('name', 'Unknown')
            symbol = data.get('symbol', 'N/A')
            logo = data.get('logo', '')
        else:
            name = 'Unknown'
            symbol = 'N/A'
            logo = ''

        tokens_data.append({
            'name': name,
            'symbol': symbol,
            'address': address,
            'logo': logo,
        })
    return tokens_data

def is_cache_valid(path):
    if not os.path.exists(path):
        return False
    file_age = time.time() - os.path.getmtime(path)
    return file_age < CACHE_LIFETIME

@app.route('/tokens', methods=['GET'])
def get_tokens_data():
    use_cache = False

    if is_cache_valid(MEMECOINS_FILE):
        try:
            with open(MEMECOINS_FILE, 'r') as f:
                cached_data = json.load(f)
                # Only use if data exists and has 'sponsored'
                if cached_data and 'sponsored' in cached_data and len(cached_data['sponsored']) > 0:
                    use_cache = True
        except (json.JSONDecodeError, FileNotFoundError):
            pass  # If the file is corrupt or unreadable, skip cache

    if use_cache:
        print("✅ Returning valid cached data.")
        return jsonify(cached_data)

    print("🔄 Cache invalid or empty — fetching from API.")
    sponsored = fetch_token_metadata(sponsored_addresses)
    result = {'sponsored': sponsored}

    with open(MEMECOINS_FILE, 'w') as f:
        json.dump(result, f)

    return jsonify(result)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
