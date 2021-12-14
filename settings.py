# coding: utf-8

# 浏览器设置
browser_configs = {
    "headless": False,
    "executable_path": "/Users/cjw/Documents/ms-playwright/chromium-939194/chrome-mac/Chromium.app/Contents/MacOS/Chromium"
}

# 上下文设置
context_configs = {
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "java_script_enabled": True,
    "ignore_https_errors": True
}
# 上下文请求默认超时时间
context_default_timeout = 30000

context_init_js = [
    "'Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});'",
]

# 日志等级
logging_level = "DEBUG"
