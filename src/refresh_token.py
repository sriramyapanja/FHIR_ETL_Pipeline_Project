from pathlib import Path
import json
import requests
from src.registration import get_client_id_from_file, data_dir, TOKEN_URL


def get_refresh_token_from_file():
    file_path = Path(data_dir / "access_token.json")
    if not file_path.exists():
        print("Error: access_token.json file not found.")
        return None
    try:
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
            access_token = json_data.get('refresh_token')
        return access_token
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error reading refresh token from file: {e}")
        return None


def get_payload():
    try:
        payload = {
            'client_id': get_client_id_from_file(),
            'grant_type': 'refresh_token',
            'refresh_token': get_refresh_token_from_file()
        }
        return payload
    except ValueError as e:
        print(f'ValueError - Error when generating payload: {e}')


def get_headers():
    try:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'content-type': 'application/x-www-form-urlencoded'
        }
        return headers
    except ValueError as e:
        print(f'ValueError - Error when generating headers: {e}')


def renew_access_token():
    response = requests.request(method="POST", url=TOKEN_URL, data=get_payload(), headers=get_headers())
    if response.status_code == 200:
        access_token_path = Path(data_dir / "access_token.json")
        access_token_path.touch(exist_ok=True)
        with open(access_token_path, 'w') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        print(f"access_token:{response.json().get('access_token')}")
    else:
        print(f"Error when trying to generate access token: {response.status_code}")
        print(f"Error: {response.json()}")


if __name__ == '__main__':
    renew_access_token()
