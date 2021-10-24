# coding: utf-8
import time

from playwright.sync_api import sync_playwright


def core(playwright, mundo):
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = chromium.launch(headless=False, executable_path="/Users/cjw/Library/Caches/ms-playwright/chromium-901522/chrome-mac/Chromium.app/Contents/MacOS/Chromium")
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
    time.sleep(10)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    url = "http://bh4ars.riskivy.xyz/"
    mundo = Mundo(url)
    core(playwright, mundo)
