import os

import requests
from lxml import etree

session = requests.session()
session.trust_env = False
# session.proxies = {
#     'http': "http://127.0.0.1:10809",
#     'https': "http://127.0.0.1:10809",
# }
PluginsOSPath = "C:/PaperMC/plugins/"
plugin_name = "LuckPerms"
host = "ci.lucko.me"
if __name__ == '__main__':
    os.chdir(PluginsOSPath)
    download_url = "https://ci.lucko.me/job/LuckPerms/"
    response = session.get(download_url)
    if response.status_code == 200:
        selector = etree.HTML(response.text)
        content = selector.xpath(
            '//*[@id="main-panel"]/table/tr[1]/td[2]/table/tr[1]/td[2]/a/@href')
        print(content)
        if len(content):
            download_url = f"https://{host}/job/InteractionVisualizer/{content[0]}"
            print(download_url)
            file_name = download_url.split("/")[-1]
            if not os.path.exists(file_name):
                print(f"正在下载{plugin_name}新版本: {file_name}")
                response = session.get(download_url)
                if response.status_code == 200:
                    for root, dirs, files in os.walk("."):
                        for name in files:
                            if name.startswith(plugin_name):
                                os.remove(name)
                        break
                    with open(file_name, "wb") as file:
                        file.write(response.content)

    print(f"{plugin_name}更新完成")
