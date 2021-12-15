# coding: utf-8
from core.repeat import RepeatHandler
from utils.log import setup_logger

logger = setup_logger(__name__)
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
        # 标签没有内容
        if not text:
            RepeatHandler.click_add(page, a)
            continue
        # 标签点击过了
        if RepeatHandler.click_in(page, a):
            logger.debug(f"跳过点击过的元素:{text}")
            continue
        # 标签被隐藏了
        if a.is_hidden():
            logger.debug(f"元素不可见:{text}")
            RepeatHandler.click_add(page, a)
            continue

        # mailto 的情况
        if a.get_attribute("href"):
            href = a.get_attribute("href")
            if href.startswith("mailto"):
                logger.debug("忽略邮件的超链接")
                RepeatHandler.click_add(page, a)
                continue
        logger.debug(f"开始点击:{text}")
        logger.debug_json(f"{text}的属性", {
            "is_hidden": a.is_hidden(),
            "is_visible": a.is_visible(),
            "is_enable": a.is_enabled(),
            "is_editable": a.is_editable(),
            "is_disable": a.is_disabled()
        })

        try:
            # a.hover()
            # time.sleep(1)
            page.evaluate(t, a)  # js点击速度快
            # time.sleep(3)
            # a.click()  # 原生点击速度慢
        except Exception as e:
            logger.error(f"元素点击失败:{text}")
        finally:
            RepeatHandler.click_add(page, a)
