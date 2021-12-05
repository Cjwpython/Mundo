# coding: utf-8'
from functools import partial
from urllib.parse import urlparse


class RouteHandler():
    def add_route(self, page, base_url):
        page.route("**/*", partial(self.handle, base_url))

    def handle(self, base_url, route, request):
        request_url = request.url
        if not self.is_homelogy(request_url):
            route.abort("aborted")
            print("拒绝非同源的请求")
            return

        if request.is_navigation_request():
            print("页面发生重定向")
            print(request_url)
            route.abort("aborted")
            self.task_queue.put_nowait((request_url, request))
            return
        print(request.method)
        print(request.url)
        print(request.headers)

        route.continue_()

    def is_homelogy(self, url):
        url_netloc = urlparse(url).netloc
        if url_netloc != self.base_target:
            return False
        return True

    def other_handler(self, route, request):
        headers = {
            **request.headers}
        postData = request.post_data
        method = request.method
        print(method)
        print(123)
        print(headers)
        route.continue_(headers=headers, postData=postData, method=method)
