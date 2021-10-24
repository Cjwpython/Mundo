# coding: utf-8
import os.path
import time
from playwright.sync_api import sync_playwright
from core.entry import Mundo
base_dir = os.path.abspath(__file__)

def core(playwright, mundo):
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = chromium.launch(headless=False, executable_path=os.path.join(os.path.dirname(__file__),"bin/Chromium.app/Contents/MacOS/Chromium"))
    mundo.set_browser(browser)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        java_script_enabled=True,
        ignore_https_errors=True
    )
    context.add_init_script('Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});')
    context.set_default_timeout(30000)  # 页面加载等待时间
    mundo.set_context(context)
    mundo.start()
    context.close()
    browser.close()


def main(entrypoint):
    with sync_playwright() as playwright:
        mundo = Mundo(entrypoint)
        core(playwright, mundo)


if __name__ == '__main__':
    entrypoint = "http://testphp.vulnweb.com/"
    main(entrypoint)
