import requests
from tqdm import tqdm

session = requests.session()
session.trust_env = False
baseUrl = 'https://papermc.io/api/v2'
project = 'paper'

# project-controller
project_url = f"{baseUrl}/projects/{project}"

versions = session.get(project_url).json()['versions']

# version-controller
version_url = f"{baseUrl}/projects/{project}/versions/{versions[-1]}"

builds = session.get(version_url).json()['builds']

# version-build-controller
version_build_url = f"{baseUrl}/projects/{project}"

downloads = session.get(f"{baseUrl}/projects/{project}/versions/{versions[-1]}/builds/{builds[-1]}/").json()[
    'downloads']
print(downloads['application']['name'])

# download-controller
download_url = f"{baseUrl}/projects/{project}/versions/{versions[-1]}/builds/{builds[-1]}/downloads/{downloads['application']['name']}"

response = session.get(download_url, stream=True)
total_size_in_bytes = int(response.headers.get('content-length', 0))
block_size = 1024  # 1 Kibibyte
progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
with open(downloads['application']['name'], 'wb') as file:
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        file.write(data)
progress_bar.close()
if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
    print("ERROR, something went wrong")