import requests
import base64
import json
from pathlib import Path
from src.registration import REDIRECT_URI, get_client_id_from_file, get_client_secret_from_file, data_dir, TOKEN_URL


def get_url_from_file():
    file_path = Path(data_dir / "url_from_browser.txt")
    if not file_path.exists():
        raise FileNotFoundError("Error: url_from_browser.txt file not found.")
    try:
        with open(file_path, 'r') as f:
            url_from_browser = f.readline().strip()
            if len(url_from_browser.strip()) == 0:
                raise ValueError("No URL found in url_from_browser.txt")
            else:
                return url_from_browser
    except Exception as e:
        print(f"An error occurred while reading the URL: {e}")
        return None


def get_code_from_url():
    try:
        url_from_browser = get_url_from_file()
        url_part = url_from_browser.split('?')[1]
        code_part = url_part.split('&')[0]
        code_value = code_part.split('=')[1]
        return code_value
    except ValueError as e:
        print(f'ValueError - unable to code from URL: {e}')


def get_encoded_credentials():
    try:
        client_id = get_client_id_from_file()
        client_secret = get_client_secret_from_file()
        credentials = f"{client_id}:{client_secret}"
        # Encode the credentials string to bytes
        credentials_bytes = credentials.encode('ascii')
        # Convert the bytes to base64
        encoded_credentials = base64.b64encode(credentials_bytes)
        return encoded_credentials
    except ValueError as e:
        print(f"ValueError - Unable to get encoded credentials: {e}")


def get_payload():
    try:
        payload = {
            'client_id': get_client_id_from_file(),
            'grant_type': 'authorization_code',
            'code': get_code_from_url(),
            'redirect_url': REDIRECT_URI,
        }
        return payload
    except ValueError as e:
        print(f'ValueError - Error when generating payload: {e}')


def get_headers():
    try:
        headers = {
            'Authorization': f"Basic {get_encoded_credentials()}",
            'Content-Type': 'application/x-www-form-urlencoded',
            'content-type': 'application/x-www-form-urlencoded'
        }
        return headers
    except ValueError as e:
        print(f'ValueError - Error when generating headers: {e}')


def get_access_token():
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
    get_access_token()
