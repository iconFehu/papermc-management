import os

import requests

session = requests.session()
session.trust_env = False
PluginsOSPath = "C:/PaperMC/plugins/"
if __name__ == '__main__':
    os.chdir(PluginsOSPath)
    download_url = "https://ci.dmulloy2.net/job/ProtocolLib/lastSuccessfulBuild/artifact/target/ProtocolLib.jar"
    response = session.get(download_url)
    with open("ProtocolLib.jar", "wb") as file:
        file.write(response.content)
    print("ProtocolLib更新完成")
