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
        if not TargetController.is_homelogy(url):
            return
        logger.info(f"请求失败:{_intercepted_request.method}:{url}")
        logger.debug_json("请求失败", {
            "method": _intercepted_request.method,
            "url": url,
            "post_data": _intercepted_request.post_data,
            "is_navigation_request": _intercepted_request.is_navigation_request()
        })

    def intercepted_requestfinished(self, _intercepted_request):
        url = _intercepted_request.url
        logger.debug(f"请求结束:{url}")

    def intercepted_response(self, _intercepted_response):
        url = _intercepted_response.url
        status_code = _intercepted_response.status
        if not TargetController.is_homelogy(url):
            return
        # 当请求结束，这个url已经处理完成
        if status_code == 301:
            logger.debug("去除重定向的请求")
            return
        RepeatHandler.request_add(url, _intercepted_response.request.method)
        logger.info(f"响应结束:{_intercepted_response.request.method}:{url}:{status_code}")
        logger.debug_json("响应结束", {
            "request": {
                "method": _intercepted_response.request.method,
                "url": url,
                "post_data": _intercepted_response.request.post_data,
                "headers": _intercepted_response.request.headers
            },
            "response": {
                "status_code": status_code,
                # "text": _intercepted_response.text(),
                "headers": _intercepted_response.headers
            }
        })

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
        # RepeatHandler.add_cache(url)

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
