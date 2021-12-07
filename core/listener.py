# coding: utf-8
from functools import partial

from core.repeat import RepeatHandler


class ListerHandler():
    def add_listener(self, page):
        page.on("request", partial(self.intercepted_request, page))
        page.on("requestfailed", partial(self.intercepted_requestfailed, page))
        page.on("requestfinished", partial(self.intercepted_requestfinished, page))
        page.on("response", partial(self.intercepted_response, page))
        page.on("popup", partial(self.intercepted_popup, page))  # 打开了一个新的页面

    def remove_listener(self, page):
        page.remove_listener("request", partial(self.intercepted_request, page))
        page.remove_listener("requestfailed", partial(self.intercepted_requestfailed, page))
        page.remove_listener("requestfinished", partial(self.intercepted_requestfinished, page))
        page.remove_listener("response", partial(self.intercepted_response, page))

    def intercepted_request(self, page, _intercepted_request):
        url = _intercepted_request.url
        is_navigation_request = _intercepted_request.is_navigation_request()
        method = _intercepted_request.method
        print(f"开始请求：{method} {url} {is_navigation_request}")

    def intercepted_requestfailed(self, page, _intercepted_request):
        url = _intercepted_request.url
        print(f"请求失败:{url}")
        # RepeatHandler.add_cache(url)

    def intercepted_requestfinished(self, page, _intercepted_request):
        url = _intercepted_request.url
        print(f"请求结束:{url}")

    def intercepted_response(self, page, _intercepted_response):
        url = _intercepted_response.url
        status_code = _intercepted_response.status
        print(f"响应结束:{url},响应状态码:{status_code}")

        # 当请求结束，这个url已经处理完成
        RepeatHandler.request_add(url)

    def intercepted_popup(self, page, intercepted_fream):
        url = intercepted_fream.url
        if not self.is_homelogy(url):
            intercepted_fream.close()
            return
        # print(f"新的页面打开:{url}")
        self.task_queue.put_nowait(url)
        intercepted_fream.close()
