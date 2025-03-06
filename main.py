import os
import requests
from flask import Flask, request, jsonify
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# 환경변수에서 FatSecret 키 읽어오기
CLIENT_ID = os.getenv('FATSECRET_CLIENT_ID')
CLIENT_SECRET = os.getenv('FATSECRET_CLIENT_SECRET')

def get_access_token():
    url = 'https://oauth.fatsecret.com/connect/token'
    data = {'grant_type': 'client_credentials', 'scope': 'basic'}
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

    response = requests.post(url, data=data, auth=auth)
    response.raise_for_status()  # 에러 발생 시 예외 발생
    return response.json().get('access_token')

@app.route('/')
def home():
    return "FatSecret API Proxy Server is running! Use /search_food?query=음식명"

@app.route('/search_food', methods=['GET'])
def search_food():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'query 파라미터를 입력하세요'}), 400

    try:
        token = get_access_token()
        search_url = 'https://platform.fatsecret.com/rest/server.api'
        params = {
            'method': 'foods.search',
            'search_expression': query,
            'format': 'json',
            'language': 'ko-kr'  # 언어 한국어로 지정
        }
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(search_url, headers=headers, params=params)

        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'FatSecret API 요청 실패', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
