import os
from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# 환경변수에서 Client ID랑 Secret 가져오기
CLIENT_ID = os.getenv('FATSECRET_CLIENT_ID')
CLIENT_SECRET = os.getenv('FATSECRET_CLIENT_SECRET')

def get_access_token():
    url = 'https://oauth.fatsecret.com/connect/token'
    data = {'grant_type': 'client_credentials', 'scope': 'basic'}
    response = requests.post(url, data=data, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    response.raise_for_status()
    return response.json().get('access_token')

@app.route('/')
def home():
    return "FatSecret API Proxy is running. Use /search_food?query=삼겹살 to search foods."

@app.route('/search_food', methods=['GET'])
def search_food():
    query = request.args.get('query')
    token = get_access_token()
    search_url = 'https://platform.fatsecret.com/rest/server.api'

    params = {
        'method': 'foods.search',
        'search_expression': query,
        'format': 'json',
        'language': 'ko'  # 한국어 응답 설정
    }

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    return jsonify(response.json())

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))  # Render 기본 포트 맞추기
    app.run(host='0.0.0.0', port=port, debug=False)
