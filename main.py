from flask import Flask, request, jsonify
import requests
import os
import base64

app = Flask(__name__)

# 환경변수에서 클라이언트 정보 가져오기
CLIENT_ID = os.getenv("FATSECRET_CLIENT_ID")
CLIENT_SECRET = os.getenv("FATSECRET_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("❌ 환경변수에서 FATSECRET_CLIENT_ID 또는 FATSECRET_CLIENT_SECRET를 찾을 수 없습니다!")

# FatSecret 인증 토큰 가져오는 함수
def get_access_token():
    url = "https://oauth.fatsecret.com/connect/token"
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "basic"
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # 에러 발생 시 바로 예외 발생

    return response.json().get("access_token")

# 루트 경로 - 기본 페이지 처리 (404 방지)
@app.route('/')
def home():
    return "FatSecret API Proxy is running! 🥩", 200

# 음식 검색 엔드포인트
@app.route('/search_food', methods=['GET'])
def search_food():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    token = get_access_token()
    search_url = "https://platform.fatsecret.com/rest/server.api"

    params = {
        "method": "foods.search",
        "search_expression": query,
        "format": "json"
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(search_url, headers=headers, params=params)

    try:
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# 포트설정 - Render에서 자동으로 잡아주는 PORT 사용
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # 기본 포트는 5000, Render는 PORT 환경변수로 지정
    app.run(host='0.0.0.0', port=port)
