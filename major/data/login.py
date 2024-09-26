import requests
from .user import headers


def get_token(data, proxies=None):
    url = "https://major.bot/api/auth/tg/"
    payload = {"init_data": data}

    try:
        response = requests.post(
            url=url, headers=headers(), json=payload, proxies=proxies, timeout=20
        )
        data = response.json()
        token = data["access_token"]
        return token
    except:
        return None
