from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import configs
from key import API_KEY

from anticaptchaofficial.recaptchav2proxyless import *
import time

# Chrome
servico = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Headless mode
# chrome_options.add_argument(rf'--user-data-dir={configs.path_chrome}')
# chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument(f"user-agent={configs.user_agent}")  # Agent
chrome_options.add_argument("−−incognito")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
navegador = webdriver.Chrome(service=servico, options=chrome_options)

link = "https://www.google.com/recaptcha/api2/demo"
navegador.get(link)

# Website_key
website_captcha_key = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
    (By.ID, "recaptcha-demo"))).get_attribute("data-sitekey")

print(f'website_captcha_key = {website_captcha_key}')

# anti-captcha.com
solver = recaptchaV2Proxyless()
solver.set_verbose(1)
solver.set_key(API_KEY)
solver.set_website_url(link)
solver.set_website_key(website_captcha_key)

resposta = solver.solve_and_return_solution()

if resposta != 0:
    print(resposta)
    navegador.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{resposta}'")  # javascript
    navegador.find_element(By.ID, 'recaptcha-demo-submit').click()

else:
    print(solver.err_string)
