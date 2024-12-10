import webbrowser
import random
from urllib import parse
from src.registration import get_client_registration_details, REDIRECT_URI, CLIENT_NAME


def get_encoded_url():
    data = get_client_registration_details()
    f = {
        "client_id": data["client_id"],
        "response_type": "code",
        "scope": data["scope"],
        'redirect_uris': REDIRECT_URI,
        'state': f'random-{random.randint(a=100, b=200)}'
    }
    return parse.urlencode(f)


def open_url():
    url = f"https://in-info-web20.luddy.indianapolis.iu.edu/oauth2/default/authorize?{get_encoded_url()}"
    webbrowser.open(url, new=0, autoraise=True)


if __name__ == '__main__':
    print(CLIENT_NAME)
    open_url()
