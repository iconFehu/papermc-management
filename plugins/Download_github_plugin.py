import asyncio
import os
import sys

import aiohttp
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# p = os.popen(r"""
# "C:\Users\fehu\AppData\Local\Google\Chrome\Application\chrome" https://github.com/ --remote-debugging-port=4444 --user-data-dir="C:\Users\fehu\AppData\Local\Google\Chrome\User Data 1"
# """.replace("\n", ""))
# print(p.read())

options = webdriver.ChromeOptions()
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("debuggerAddress", "127.0.0.1:4444")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print(driver.title)
WebDriverWait(driver, 11).until(
    lambda d: "GitHub" in d.title
)

cookie = '; '.join([f"{_.get('name')}={_.get('value')}"
                    for _ in driver.get_cookies() if (_.get('domain').endswith('.spigotmc.org'))])
# session = requests.session()
# session.trust_env = False
# userAgent = requests.get('http://127.0.0.1:4444/json/version').json().get('User-Agent')
# print(userAgent)
# session.headers = {
#     "user-agent": userAgent,
#     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
#     'cookie': cookie
# }
PluginsOSPath = "C:/PaperMC/plugins/"
host = "github.com"


async def download_file(plugin, session):
    global host
    response = await session.get(f"https://{host}/{plugin[0]}/releases")
    plugin_name = plugin[1]

    # print(response.status_code)
    # response
    if response.status == 200:
        selector = etree.HTML(await response.text())
        content = selector.xpath(
            '//div[@class="Box-footer"]//a/@href')
        content = list(filter(lambda link: plugin_name in link, content))
        if len(content):
            download_url = f"https://{host}/{content[0]}"
            print(download_url)
            file_name = download_url.split("/")[-1]
            if not os.path.exists(file_name):
                for root, dirs, files in os.walk(".."):
                    for name in files:
                        if name.startswith(plugin_name):
                            os.remove(name)
                    break
                print(f"正在下载{plugin_name}新版本: {file_name}")
                response = await session.get(download_url)
                with open(file_name, "wb") as file:
                    file.write(response.content)

    print(f"{plugin}更新完成")
    return True


async def main():
    async with aiohttp.ClientSession() as client:
        with open("github/plugin_list", "r") as plugin_list:
            ls = [line.split(' ') for line in plugin_list.read().split("\n")]
            os.chdir(PluginsOSPath)
            await asyncio.gather(*[download_file(plugin, client) for plugin in ls])


if __name__ == '__main__':
    # Only preform check if your code will run on non-windows environments.
    if sys.platform == 'win32':
        # Set the policy to prevent "Event loop is closed" error on Windows - https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
