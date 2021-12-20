# coding: utf-8
from core.repeat import RepeatHandler
from functools import partial
from utils.log import setup_logger

logger = setup_logger(__name__)
from core.target import TargetController


class Listener():
    """
    页面请求监听
    """

    def common_listener(self, page):
        page.on("request", self.intercepted_request)
        page.on("requestfailed", self.intercepted_requestfailed)
        page.on("requestfinished", self.intercepted_requestfinished)
        page.on("response", self.intercepted_response)
        page.on("popup", self.intercepted_popup)  # 打开了一个新的页面

    def remove_listener(self, page):
        page.remove_listener("request", self.intercepted_request)
        page.remove_listener("requestfailed", self.intercepted_requestfailed)
        page.remove_listener("requestfinished", self.intercepted_requestfinished)
        page.remove_listener("response", self.intercepted_response)

    def intercepted_request(self, _intercepted_request):
        url = _intercepted_request.url
        is_navigation_request = _intercepted_request.is_navigation_request()
        method = _intercepted_request.method
        post_data = _intercepted_request.post_data
        if not (url):
            return
        logger.debug(f"开始请求：M:{method} U:{url} PD:{post_data} INR:{is_navigation_request}")

    def intercepted_requestfailed(self, _intercepted_request):

        url = _intercepted_request.url
        method = _intercepted_request.method
        if not TargetController.is_homelogy(url):
            return

        if RepeatHandler.request_in(url, method):  # 重复的请求不再打印
            return
        logger.info(f"请求失败:{_intercepted_request.method}:{url}")
        logger.debug_json("请求失败", {
            "request": {
                "method": _intercepted_request.method,
                "url": url,
                "post_data": _intercepted_request.post_data,
                "headers": _intercepted_request.headers
            },
            "response": {
                "status_code": _intercepted_request.response.status,
                # "text": _intercepted_response.text(),
                "headers": _intercepted_request.response.headers
            }
        })

    def intercepted_requestfinished(self, _intercepted_request):
        url = _intercepted_request.url
        status_code = _intercepted_request.response().status
        logger.debug(f"请求结束:{url}")

        # 专门处理跳转、转发的页面
        if status_code in [301, 302]:
            # response_text = None
            response_headers = None
        else:
            # response_text = _intercepted_request.response().text()
            response_headers = _intercepted_request.response().headers

        logger.debug_json("响应结束", {
            "request": {
                "method": _intercepted_request.method,
                "url": url,
                "post_data": _intercepted_request.post_data,
                "headers": _intercepted_request.headers
            },
            "response": {
                "status_code": status_code,
                # "text": response_text,
                "headers": response_headers
            }
        })

    def intercepted_response(self, _intercepted_response):
        url = _intercepted_response.url
        status_code = _intercepted_response.status
        if not TargetController.is_homelogy(url):
            return
        RepeatHandler.request_add(url, _intercepted_response.request.method)
        logger.debug(f"响应结束:{_intercepted_response.request.method}:{url}:{status_code}")

    def intercepted_popup(self, intercepted_fream):
        url = intercepted_fream.url
        if not TargetController.is_homelogy(url):
            intercepted_fream.close()
            return
        logger.debug(f"新的页面打开:{url}")
        TargetController.task_queue.put_nowait((url, ""))
        intercepted_fream.close()

    def forword_listener(self, page, request):
        page.on("request", partial(self.forword_request, request))
        page.on("requestfailed", partial(self.forword_requestfailed, request))
        page.on("requestfinished", partial(self.forword_requestfinished, request))
        page.on("response", partial(self.forword_response, request))

    def forword_request(self, real_request, request):
        url = real_request.url
        is_navigation_request = real_request.is_navigation_request()
        method = real_request.method
        post_data = real_request.post_data
        if not TargetController.is_homelogy(url):
            return
        logger.debug(f"开始请求：M:{method} U:{url} PD:{post_data} INR:{is_navigation_request}")

    def forword_requestfailed(self, real_request, request):
        url = real_request.url
        logger.debug(request.response().status)
        # RepeatHandler.add_cache(url)
        logger.info(f"转发请求失败:{real_request.method}:{url}")
        logger.debug_json("转发请求失败", {
            "method": real_request.method,
            "url": url,
            "post_data": real_request.post_data,
            "is_navigation_request": real_request.is_navigation_request()
        })

    def forword_requestfinished(self, real_request, request):
        url = real_request.url
        logger.debug(request.response().status)
        logger.debug(f"转发请求结束:{url}")
        logger.debug_json("响应结束", {
            "request": {
                "method": real_request.method,
                "url": url,
                "post_data": real_request.post_data,
                "headers": real_request.headers
            },
            "response": {
                "status_code": request.response.status,
                # "text": _intercepted_response.text(),
                "headers": request.response.headers
            }
        })

    def forword_response(self, real_request, response):
        url = real_request.url
        status_code = response.status
        # 当请求结束，这个url已经处理完成
        RepeatHandler.request_add(url, real_request.method)
        logger.info(f"转发响应结束:{real_request.method}:{url}:{status_code}")

        logger.debug_json("转发响应结束", {
            "request": {
                "method": real_request.method,
                "url": url,
                "post_data": real_request.post_data,
                "headers": real_request.headers
            },
            "response": {
                "status_code": status_code,
                # "text": _intercepted_response.text(),
                "headers": response.headers
            }
        })
