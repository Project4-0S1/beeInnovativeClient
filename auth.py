import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN_FILE = 'token.json'

def save_token(token, expires_in):
    with open(TOKEN_FILE, 'w') as f:
        json.dump({
            'access_token': token,
            'expires_at': time.time() + expires_in
        }, f)

def load_token():
    if os.path.exists(TOKEN_FILE) and os.path.getsize(TOKEN_FILE) > 0:
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    return None

def is_token_valid(token_info):
    if token_info and 'expires_at' in token_info:
        return token_info['expires_at'] > time.time()
    return False

def get_access_token():
    token_info = load_token()

    if is_token_valid(token_info):
        return token_info['access_token']

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    auth_url = os.getenv("AUTH_URL")

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": "https://beeinnovative.azurewebsites.net/",
        "grant_type": "client_credentials"
    }

    response = requests.post(auth_url, json=data)

    if response.status_code == 200:
        response_json = response.json()
        access_token = response_json.get("access_token")
        expires_in = response_json.get("expires_in")
        save_token(access_token, expires_in)
        return access_token
    else:
        print(f"Failed to fetch access token: {response.status_code}")
        print(response.text)
        return None

