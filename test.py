# coding: utf-8
from main import Mundo

mundo = Mundo()

# login_configs = {
#     "login_url": "http://10.0.83.6/login",
#     "login_select_type": "custom",
#     "username_selector": "#username",
#     "password_selector": "#password",
#     "submit_selector": "#components-form-demo-normal-login > div:nth-child(3) > div > div > span > button",
#     "username_input": "admin",
#     "password_input": "123123",
#     "login_error_raise": False
# }
# mundo.login(login_configs)
url = "http://bh4ars.riskivy.xyz"
mundo.add_target(url)
mundo.run()
