import os

from lxml import etree

from tools.spigotmcTool import get_session

session = get_session()
PluginsOSPath = "C:/PaperMC/plugins/"
host = "www.spigotmc.org"


def download_file(plugin_id):
    global host
    response = session.get(f"https://{host}/resources/{plugin_id}/")
    # print(response.status_code)
    if response.status_code == 200:
        selector = etree.HTML(response.text)
        content = selector.xpath(
            '//*[@id="content"]/div/div/div[2]/div/div/div[1]/ul/li/label/a/@href')
        print(content)
        if len(content):
            download_url = f"https://{host}/{content[0]}"
            print(download_url)
            response = session.get(download_url)
            print(response.status_code)
            if response.status_code == 200:
                file_name = response.headers['content-disposition'].split("=")[1].replace('"', "")
                # print(f"文件大小: {len(response.content)}")
                plugin_name = file_name.split("-")[0]
                print(plugin_name)
                # if not os.path.exists(file_name):
                for root, dirs, files in os.walk("."):
                    for name in files:
                        # print(name)
                        if name.startswith(plugin_name):
                            os.remove(name)
                    break
                print(f"正在保存{plugin_id} 新版本: {file_name} 文件大小: {len(response.content) / 1024}KB")
                with open(file_name, "wb") as file:
                    # print(len(response.content))
                    file.write(response.content)

    print(f"{plugin_id}更新完成")


if __name__ == '__main__':
    with open("spigotmc/plugin_list", "r") as plugin_list:
        ls = plugin_list.read().split("\n")
        os.chdir(PluginsOSPath)
        for plugin_id in ls:
            print(plugin_id)
            download_file(plugin_id)

