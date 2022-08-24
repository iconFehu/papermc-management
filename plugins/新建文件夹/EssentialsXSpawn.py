import os

import requests
from lxml import etree

session = requests.session()
session.trust_env = False
# session.proxies = {
#     'http': "http://127.0.0.1:10809",
#     'https': "http://127.0.0.1:10809",
# }
# session.headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
#     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"'
# }
PluginsOSPath = "C:/PaperMC/plugins/"
plugin_name = "EssentialsXSpawn"
host = "github.com"
if __name__ == '__main__':
    os.chdir(PluginsOSPath)
    response = session.get(f"https://{host}/EssentialsX/Essentials/releases")
    print(response.status_code)
    if response.status_code == 200:
        selector = etree.HTML(response.text)
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
                response = session.get(download_url)
                with open(file_name, "wb") as file:
                    file.write(response.content)

    print(f"{plugin_name}更新完成")
