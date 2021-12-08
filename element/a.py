# coding: utf-8
import time

from core.repeat import RepeatHandler

t = """
e => {
        // 让 a 标签都在当前标签页面打开, 减少新标签页面打开的消耗(加载额外的资源文件)
        e.target = '';
        e.scrollIntoView({
            behavior: 'smooth'
        });
        e.click();
    }
"""


def handle_a(page):
    all_a = page.query_selector_all("a")
    for a in all_a:
        text = a.inner_text().strip()
        print(f"{text} is_hidden:{a.is_hidden()} is_visible:{a.is_visible()} is_enable:{a.is_enabled()} is_editable:{a.is_editable()} is_disable:{a.is_disabled()}")
        if RepeatHandler.click_in(page, a):
            print(f"跳过点击过的元素:{text}")
            continue
        print(f"开始点击:{text}")
        if a.is_hidden():
            print(f"元素不可见:{text}")
            RepeatHandler.click_add(page, a)
            continue
        if not text:
            RepeatHandler.click_add(page, a)
            continue

        try:
            # a.hover()
            # time.sleep(1)
            page.evaluate(t, a)  # js点击速度快
            time.sleep(3)
            # a.click()  # 原生点击速度慢
        except Exception as e:
            print(f"元素点击失败:{text}")
        finally:
            RepeatHandler.click_add(page, a)
