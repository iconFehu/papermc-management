import asyncio
import os
import sys
from lxml import etree
from tools.tqdm_progress import aiohttp_progress
from tools.spigotmcTool import get_aiohttp_client

PluginsOSPath = "C:/PaperMC/plugins/"
host = "www.spigotmc.org"


async def download_file(plugin, session):
    global host
    response = await session.get(f"https://{host}/resources/{plugin[0]}/")
    # print(response.status)
    if response.status == 200:
        selector = etree.HTML(await response.text())
        content = selector.xpath(
            '//*[@id="content"]/div/div/div[2]/div/div/div[1]/ul/li/label/a/@href')
        if len(content):
            download_url = f"https://{host}/{content[0]}"
            print(download_url)
            response, content = await aiohttp_progress(session.get(download_url))
            if response.status == 200:
                file_name = response.headers['content-disposition'].split("=")[1].replace('"', "")
                plugin_name = file_name.split("-")[0]
                print(plugin_name)
                # if not os.path.exists(file_name):
                for root, dirs, files in os.walk("."):
                    for name in files:
                        if name.startswith(plugin_name):
                            os.remove(name)
                    break
                with open(file_name, "wb") as file:
                    file.write(content)

    print(f"{plugin}更新完成")


async def main():
    async with await get_aiohttp_client('https://www.spigotmc.org/', 'Minecraft') as client:
        with open("spigotmc/plugin_list", "r") as plugin_list:
            ls = [line.split(' ') for line in plugin_list.read().split("\n")]
            os.chdir(PluginsOSPath)
            await asyncio.gather(*[download_file(plugin, client) for plugin in ls])


if __name__ == '__main__':
    # Only preform check if your code will run on non-windows environments.
    if sys.platform == 'win32':
        # Set the policy to prevent "Event loop is closed" error on Windows - https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
