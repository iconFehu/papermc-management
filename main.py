import os.path
import sys
import threading
from subprocess import Popen
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED
from subprocess import Popen, PIPE, call

import requests
from tqdm import tqdm

session = requests.session()
session.trust_env = False
PaperMCOSPath = "C:/PaperMC/"
FrpOSPath = "C:/frp_0.39.1_windows_amd64/"


class RestartThread(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        time.sleep(3600 * 12)
        print("重启服务器")
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        # print_time(self.name, self.delay, 5)


def restart():
    # time.sleep(3600 * 12)
    time.sleep(30)
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)


if __name__ == '__main__':
    # executor = ThreadPoolExecutor(max_workers=20)
    all_task = []
    print("create task processing: ")
    # all_task = [executor.submit(nmap_ip_list, (i)) for i in range(256)]
    # all_result = [future.result() for future in as_completed(all_task)]
    # Popen("update_dns.bat")
    # executor.submit(call, f"update_dns.bat")
    os.chdir("plugins")
    print("=============================================")
    for root, dirs, files in os.walk("."):
        for name in tqdm(files):
            print(name)
            # executor.submit(call, f"{name}", shell=True)
            call(name, shell=True)
            # Popen(f"python {name}")
        break
    print("=============================================")
    # with tqdm(total=100) as pbar:
    #     pbar.set_description('all task processing: ')
    #     for future in as_completed(all_task):
    #         print('pbar.update(1)')
    #         pbar.update(1)
            # data = future.result()
    # time.sleep(5)
    # wait(all_task, return_when=ALL_COMPLETED)
    # executor.submit(restart)
    print('wait end')

    # os.chdir(FrpOSPath)
    # Popen("25565.bat")
    os.chdir(PaperMCOSPath)

    version_group = '1.19'
    response = session.get(f"https://papermc.io/api/v2/projects/paper/version_group/{version_group}/builds")
    version_group = response.json()['builds']
    latest_version = version_group[-1]
    file_name = latest_version['downloads']['application']['name']
    print(file_name)
    if not os.path.exists(f"{PaperMCOSPath}{file_name}"):
        # https://papermc.io/api/v2/projects/paper/versions/1.18.1/builds/73/downloads/paper-1.18.1-73.jar
        print(f"正在下载PaperMC新版本: {file_name}")
        file_url = f"https://papermc.io/api/v2/projects/paper/versions/{latest_version['version']}/builds/{latest_version['build']}/downloads/{file_name}"
        print(file_url)

        response = session.get(file_url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(file_name, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")
        # response = session.get(file_url)
        #         # if response.status_code == 200:
        #         #     with open(f"{PaperMCOSPath}{file_name}", 'wb') as file:
        #         #         file.write(response.content)

    # Popen(f"java -Xms2G -Xmx8G -jar {file_name}")
    # Popen(f"java -Xms12G -Xmx12G -jar {file_name} --nogui")
    eula_file = open(f"{PaperMCOSPath}eula.txt", "r")
    eula_file_read = eula_file.read()
    if not eula_file_read.find("true"):
        eula_content = eula_file.read().replace("false", "true")
        with open(f"{PaperMCOSPath}eula.txt", "w") as eula_file_write:
            eula_file_write.write(eula_content)
    os.system(f"java -jar {PaperMCOSPath}{file_name}")
