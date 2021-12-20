# coding: utf-8
from settings import static_configs


class StaticConfigs():
    static_repeat = static_configs.get("repeat", False)  # 默认不去重。页面完整加载
    static_suffix = static_configs.get("suffix", [])  # 静态资源的后缀

    @classmethod
    def set_repeat(cls, repeat: bool):
        cls.static_repeat = repeat

    @classmethod
    def add_suffix(cls, suffix):
        """
        添加后缀
        """
        if isinstance(suffix, str):
            if suffix not in cls.static_suffix:
                cls.static_suffix.append(suffix)
        if isinstance(suffix, list):
            for _suffix in suffix:
                if _suffix not in cls.static_suffix:
                    cls.static_suffix.append(_suffix)
