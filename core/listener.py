# coding: utf-8
from functools import partial


class ListerHandler():
    def add_listener(self, page):
        page.on("request", partial(self.intercepted_request, page))
        page.on("requestfailed", partial(self.intercepted_requestfailed, page))
        page.on("requestfinished", partial(self.intercepted_requestfinished, page))
        page.on("response", partial(self.intercepted_response, page))

    def remove_listener(self, page):
        page.remove_listener("request", partial(self.intercepted_request, page))
        page.remove_listener("requestfailed", partial(self.intercepted_requestfailed, page))
        page.remove_listener("requestfinished", partial(self.intercepted_requestfinished, page))
        page.remove_listener("response", partial(self.intercepted_response, page))

    def intercepted_request(self, page, intercepted_request):
        url = intercepted_request.url
        print(intercepted_request.is_navigation_request())
        print(intercepted_request.method)
        print(url)

    def intercepted_requestfailed(self, page, intercepted_request):
        url = intercepted_request.url
        # print(intercepted_request.is_navigation_request())
        print(f"请求失败:{url}")

    def intercepted_requestfinished(self, page, intercepted_request):
        url = intercepted_request.url
        # print(intercepted_request.is_navigation_request())
        print(f"请求结束:{url}")

    def intercepted_response(self, page, intercepted_response):
        url = intercepted_response.url
        status_code = intercepted_response.status
        print(f"响应结束:{url},响应状态码:{status_code}")
