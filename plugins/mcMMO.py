import os

import requests

session = requests.session()
session.trust_env = False
PluginsOSPath = "C:/PaperMC/plugins/"
if __name__ == '__main__':
    os.chdir(PluginsOSPath)
    download_url = "https://popicraft.net/jenkins/job/mcMMO/lastSuccessfulBuild/artifact/target/mcMMO.jar"
    response = session.get(download_url)
    with open("mcMMO.jar", "wb") as file:
        file.write(response.content)
    print("mcMMO更新完成")
