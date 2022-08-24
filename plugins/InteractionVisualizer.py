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
plugin_name = "InteractionVisualizer"
host = "ci.loohpjames.com"
if __name__ == '__main__':
    os.chdir(PluginsOSPath)
    download_url = "https://ci.loohpjames.com/job/InteractionVisualizer/"
    response = session.get(download_url)
    if response.status_code == 200:
        selector = etree.HTML(response.text)
        content = selector.xpath(
            '//*[@id="main-panel"]/table/tr[3]/td[2]/table/tr/td[2]/a/@href')
        print(content)
        if len(content):
            # https://ci.loohpjames.com/job/InteractionVisualizer/lastSuccessfulBuild/artifact/target/InteractionVisualizer-1.17.0.6.jar
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
