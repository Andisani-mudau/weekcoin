import os
from flask_cors import CORS
from flask import Flask, jsonify, render_template
import requests
from dotenv import load_dotenv

app = Flask(__name__, template_folder='../views')
CORS(app)

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("API_KEY")


# Read token addresses from sponsored.txt and recommended.txt
with open('server/sponsored.txt', 'r') as file:
    sponsored_addresses = [line.strip() for line in file if line.strip()]

#with open('server/recommended.txt', 'r') as file:
#    recommended_addresses = [line.strip() for line in file if line.strip()]

# Set up headers with the API key
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

@app.route('/tokens', methods=['GET'])
def get_tokens_data():
    sponsored = fetch_token_metadata(sponsored_addresses)
#    recommended = fetch_token_metadata(recommended_addresses)
    
    return jsonify({
        'sponsored': sponsored,
       # 'recommended': recommended
    })
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get PORT from environment or use 5000
    app.run(host='0.0.0.0', port=port)
