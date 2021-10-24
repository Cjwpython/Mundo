# coding: utf-8
from utils.target import is_same_netloc


class Listener():
    def __init__(self, base_target):
        self.base_target = base_target

    def log_response(self, page, intercepted_response):
        if not is_same_netloc(self.base_target, intercepted_response.request.url):
            return
        row = {
            intercepted_response.request.url: {
                "request": {
                    "method": intercepted_response.request.method,
                    "headers": intercepted_response.request.headers,
                    "resource_type": intercepted_response.request.resource_type,
                    "request_post_data": intercepted_response.request.post_data if intercepted_response.request.method != "GET" else None,
                    "request_post_data_json": intercepted_response.request.post_data_json if intercepted_response.request.method != "GET" else None
                },
                "response": {
                    "status_code": intercepted_response.status,
                    "headers": intercepted_response.headers
                }
            }}

        print(row)
