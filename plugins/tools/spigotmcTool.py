import asyncio
import os
import time

import aiohttp
import requests
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

p = os.popen(r"""
"C:\Users\fehu\AppData\Local\Google\Chrome\Application\chrome" --remote-debugging-port=4444 --user-data-dir="C:\Users\fehu\AppData\Local\Google\Chrome\User Data 381"
""".replace("\n", ""))
# print(p.read())

options = webdriver.ChromeOptions()
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("debuggerAddress", "127.0.0.1:4444")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# print(os.getcwd())
# # 读取文件
# with open('../../stealth.min.js', 'r') as f:
#     js = f.read()
#     print(js)
# # 调用函数在页面加载前执行脚本
# driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})

# session = requests.session()
# session.trust_env = False
# session.proxies = {
#     'http': "http://127.0.0.1:10809",
#     'https': "http://127.0.0.1:10809",
# }

userAgent = requests.get('http://127.0.0.1:4444/json/version').json().get('User-Agent')

print(userAgent)


# def get_session():
#     return session


async def get_aiohttp_client(url, title):
    global driver, userAgent
    driver.get(url)

    try:
        print(driver.title)
        WebDriverWait(driver, 2).until(
            lambda d: title in d.title
        )
    except TimeoutException:
        print('TimeoutException')
        handle = driver.current_window_handle
        driver.service.stop()
        await asyncio.sleep(6)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.switch_to.window(handle)

        print(driver.title)
        WebDriverWait(driver, 11).until(
            lambda d: title in d.title
        )
    cookie = '; '.join([f"{_.get('name')}={_.get('value')}"
                        for _ in driver.get_cookies() if (_.get('domain').endswith('.spigotmc.org'))])
    print(cookie)
    headers = {
        "user-agent": userAgent,
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'cookie': cookie
    }
    driver.close()
    return aiohttp.ClientSession(trust_env=False, headers=headers)


# def session_download(url, filename=None):
#     r = session.get(url, stream=True, allow_redirects=True)
#     if r.status_code != 200:
#         r.raise_for_status()  # Will only raise for 4xx codes, so...
#         raise RuntimeError(f"Request to {url} returned status code {r.status_code}")
#     file_size = int(r.headers.get('Content-Length', 0))
#
#     filename = filename if filename else r.headers['content-disposition'].split("=")[1].replace('"', "")
#     path = pathlib.Path(filename).expanduser().resolve()
#     path.parent.mkdir(parents=True, exist_ok=True)
#
#     desc = "(Unknown total file size)" if file_size == 0 else ""
#     r.raw.read = functools.partial(r.raw.read, decode_content=True)  # Decompress if needed
#     with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
#         with path.open("wb") as f:
#             shutil.copyfileobj(r_raw, f)
#
#     return path


async def main():
    # spigotmc_client = await get_aiohttp_client('https://www.spigotmc.org/', 'Minecraft')
    # github_client = await get_aiohttp_client('https://github.com/', 'GitHub')
    # print(spigotmc_client)
    # print(github_client)
    result = await asyncio.gather(*[
        get_aiohttp_client('https://www.spigotmc.org/', 'Minecraft'),
        # get_aiohttp_client('https://github.com/', 'GitHub')
    ])
    # for client in result:
    #     print(client.cookie_jar)
    print(result)
    return result


if __name__ == '__main__':
    # asyncio.run(main())
    # print(f'asyncio.run(main()) {asyncio.run(main())}')
    f = asyncio.run(get_aiohttp_client('https://www.spigotmc.org/', 'Minecraft'))
    print(f)
    f.close()

# driver.close()
# os.popen("taskkill /f /im chromedriver.exe")
