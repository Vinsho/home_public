from functools import wraps
from time import sleep
from typing import Dict

import pandas as pd
import requests


def authenticated(func):
    """
    Decorator to check if token has expired.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.token_expiration_time <= pd.Timestamp.utcnow().timestamp():
            self.login()
        return func(*args, **kwargs)

    return wrapper


class Client:
    def __init__(
            self,
            user_name: str,
            system_code: str,
            max_retry: int = 10,
            base_url: str = "https://eu5.fusionsolar.huawei.com/thirdData"
    ):
        self.user_name = user_name
        self.system_code = system_code
        self.max_retry = max_retry
        self.base_url = base_url

        self.session = requests.session()
        self.session.headers.update(
            {'Connection': 'keep-alive', 'Content-Type': 'application/json'})

        self.token_expiration_time = 0

    def __enter__(self):
        self.login()
        return self

    def login(self):
        url = f'{self.base_url}/login'
        body = {
            'userName': self.user_name,
            'systemCode': self.system_code
        }
        self.session.cookies.clear()
        r = self.session.post(url=url, json=body)
        self.session.headers.update(
            {'XSRF-TOKEN': r.cookies.get(name='XSRF-TOKEN')})
        self.token_expiration_time = pd.Timestamp.utcnow().timestamp() + 1200

    @authenticated
    def _request(self, function: str, data=None) -> Dict:
        if data is None:
            data = {}
        url = f'{self.base_url}/{function}'
        r = self.session.post(url=url, json=data)
        return r.json()

    def get_dev_list(self, station_code) -> Dict:
        return self._request("getDevList", {'stationCodes': station_code})

    def get_dev_kpi_real(self, dev_id: str, dev_type_id: int) -> Dict:
        return self._request("getDevRealKpi",
                             {'devIds': dev_id, 'devTypeId': dev_type_id})
