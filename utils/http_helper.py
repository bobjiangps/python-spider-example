import requests


class HttpHelper:

    default_headers = {"Content-type": "text/html; charset=UTF-8"}
    proxies = {'https': '106.122.168.244:9999',
               'http': '46.105.51.183:80'
               }

    @classmethod
    def get_response_by_url(cls, url, data={}, headers={}, verify_ssl=None):
        headers = dict(cls.default_headers, **headers)
        if verify_ssl is not None:
            result = requests.get(url, headers=headers, params=data, verify=verify_ssl)
        else:
            # result = requests.get(url, headers=headers, proxies=cls.proxies)
            result = requests.get(url, headers=headers, params=data)
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
