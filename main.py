from flask import Flask, request, jsonify
import requests
import os
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# 키를 환경변수에서 가져오기 (깃허브에는 노출 안 됨)
CLIENT_ID = os.getenv('FATSECRET_CLIENT_ID')
CLIENT_SECRET = os.getenv('FATSECRET_CLIENT_SECRET')

def get_access_token():
    url = 'https://oauth.fatsecret.com/connect/token'
    data = {'grant_type': 'client_credentials', 'scope': 'basic'}
    response = requests.post(url, data=data, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    return response.json().get('access_token')

@app.route('/search_food', methods=['GET'])
def search_food():
    query = request.args.get('query')
    token = get_access_token()
    search_url = 'https://platform.fatsecret.com/rest/server.api'
    params = {
        'method': 'foods.search',
        'search_expression': query,
        'format': 'json'
    }
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(search_url, headers=headers, params=params)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
