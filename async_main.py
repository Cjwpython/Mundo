import asyncio
from functools import partial
from urllib.parse import urljoin, urlparse

from playwright.async_api import async_playwright

queue = asyncio.Queue()
cache = []
read_cache = []


def log_response(page, intercepted_response):
    if intercepted_response.request.url in read_cache:
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
    read_cache.append(intercepted_response.request.url)
    print(row)


async def is_same_netloc(base_ur, real_url):
    real_url_netloc = urlparse(real_url).netloc
    base_url_netloc = urlparse(base_ur).netloc
    if base_url_netloc != real_url_netloc:
        # print("ignore  {}:{}".format(base_url_netloc,real_url_netloc))
        return False
    return True


async def need_crawler(url):
    if url in cache:
        return False
    cache.append(url)
    return True


async def analysis_a(base_url, page):
    try:
        a = await page.query_selector_all("a")
        for i in a:
            real_url = urljoin(base_url, await i.get_attribute("href"))
            if await is_same_netloc(base_url, real_url):
                # print("add :{}".format(real_url))
                await queue.put(real_url)
    except Exception as e:
        print(e)


async def start(context, url=None):
    if url:
        url = url
    else:
        url = await queue.get()
    if not await need_crawler(url):
        return
    page = await context.new_page()
    page.on("response", partial(log_response, page))
    await page.goto(url)
    await analysis_a(url, page)
    await page.close()


async def run(playwright):
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = await chromium.launch(headless=False, executable_path="/Users/cjw/Library/Caches/ms-playwright/chromium-901522/chrome-mac/Chromium.app/Contents/MacOS/Chromium")
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        java_script_enabled=True,
        ignore_https_errors=True
    )
    await context.add_init_script('Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});')
    context.set_default_timeout(30000)  # 页面加载等待时间

    base_url = "http://testphp.vulnweb.com/"
    await queue.put(base_url)
    await start(context, base_url)
    while queue.qsize() != 0:
        await start(context)

    # other actions...
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
