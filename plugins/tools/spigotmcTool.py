import functools
import os
import pathlib
import shutil

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

p = os.popen(r"""
"C:\Users\fehu\AppData\Local\Google\Chrome\Application\chrome" https://www.spigotmc.org/ --remote-debugging-port=4444 --user-data-dir="C:\Users\fehu\AppData\Local\Google\Chrome\User Data 1"
""".replace("\n", ""))
# print(p.read())

options = webdriver.ChromeOptions()
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("debuggerAddress", "127.0.0.1:4444")
driver = webdriver.Chrome('C:\\WebDriver\\chromedriver.exe', options=options)

print(driver.title)
WebDriverWait(driver, 11).until(
    lambda d: "Minecraft" in d.title
)

cookie = '; '.join([f"{_.get('name')}={_.get('value')}"
                    for _ in driver.get_cookies() if (_.get('domain').endswith('.spigotmc.org'))])

print(cookie)

session = requests.session()
session.trust_env = False
# session.proxies = {
#     'http': "http://127.0.0.1:10809",
#     'https': "http://127.0.0.1:10809",
# }

userAgent = requests.get('http://127.0.0.1:4444/json/version').json().get('User-Agent')

print(userAgent)
session.headers = {
    "user-agent": userAgent,
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'cookie': cookie
}


def get_session():
    return session


def session_download(url, filename=None):
    r = session.get(url, stream=True, allow_redirects=True)
    if r.status_code != 200:
        r.raise_for_status()  # Will only raise for 4xx codes, so...
        raise RuntimeError(f"Request to {url} returned status code {r.status_code}")
    file_size = int(r.headers.get('Content-Length', 0))

    filename = filename if filename else r.headers['content-disposition'].split("=")[1].replace('"', "")
    path = pathlib.Path(filename).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    desc = "(Unknown total file size)" if file_size == 0 else ""
    r.raw.read = functools.partial(r.raw.read, decode_content=True)  # Decompress if needed
    with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
        with path.open("wb") as f:
            shutil.copyfileobj(r_raw, f)

    return path


driver.close()
os.popen("taskkill /f /im chromedriver.exe")
