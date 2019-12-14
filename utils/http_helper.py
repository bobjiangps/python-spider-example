import requests


class HttpHelper:

    default_headers = {"Content-type": "text/html; charset=UTF-8"}

    @classmethod
    def get_response_by_url(cls, url, data=None, headers={}):
        headers = dict(cls.default_headers, **headers)
        if data:
            result = requests.get(url, headers=headers, params=data)
        else:
            result = requests.get(url, headers=headers)
        return result

    @classmethod
    def post_data_to_url(cls, url, data, headers={}):
        headers = dict(cls.default_headers, **headers)
        result = requests.post(url, headers=headers, json=data)
        return result

    @classmethod
    def put_data_to_url(cls, url, data, headers={}):
        headers = dict(cls.default_headers, **headers)
        result = requests.put(url, headers=headers, data=data)
        return result

    @classmethod
    def delete_to_url(cls, url, headers={}):
        headers = dict(cls.default_headers, **headers)
        result = requests.post(url, headers=headers)
        return result
