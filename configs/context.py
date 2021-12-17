# coding: utf-8
from settings import context_configs


class ContextController():
    context_default_timeout = context_configs.get("context_default_timeout", 3000)
    user_agent = context_configs.get("user_agent")
    java_script_enabled = context_configs.get("java_script_enabled")
    ignore_https_errors = context_configs.get("ignore_https_errors")
    context_init_js = context_configs.get("context_init_js", [])

    @classmethod
    def set_context_default_timeout(cls, timeout: int):
        cls.context_default_timeout = timeout

    @classmethod
    def set_user_agent(cls, user_agent: str):
        cls.user_agent = user_agent

    @classmethod
    def set_java_script_enabled(cls, java_script_enabled: bool):
        cls.java_script_enabled = java_script_enabled

    @classmethod
    def add_context_init_js(cls, js: str):
        cls.context_init_js.append(js)

    @classmethod
    def set_ignore_https_errors(cls, ignore_https_errors: bool):
        cls.ignore_https_errors = ignore_https_errors

    @classmethod
    def context_configs(cls):
        return {
            "user_agent": cls.user_agent,
            "java_script_enabled": cls.java_script_enabled,
            "ignore_https_errors": cls.ignore_https_errors
        }
